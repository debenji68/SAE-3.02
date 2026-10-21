#!/usr/bin/env bash
# =============================================================================
# SAE 3.02 - VM 1 (Serveur : moteur de simulation + MariaDB)
#
# Installe TOUT ce qu'il faut puis lance le serveur :
#   bash setup_vm1_server.sh
#
# Options :
#   --ip-client <IP>   n'autorise que la VM 2 sur le port du serveur
#   --port <N>         port TCP du serveur (5000 par défaut)
#   --sans-lancement   installe seulement
#
# Fonctionne en root ou en utilisateur normal (demande le mot de passe root
# une seule fois si sudo n'est pas configuré). Relançable sans risque.
# =============================================================================
set -euo pipefail

PORT=5000
IP_CLIENT=""
LANCER=1
PHASE_ROOT=0

while [[ $# -gt 0 ]]; do
    case "$1" in
        --ip-client)      IP_CLIENT="${2:?--ip-client attend une adresse IP}"; shift 2 ;;
        --port)           PORT="${2:?--port attend un numéro}"; shift 2 ;;
        --sans-lancement) LANCER=0; shift ;;
        --phase-root)     PHASE_ROOT=1; shift ;;   # usage interne
        -h|--help)        sed -n '2,16p' "$0"; exit 0 ;;
        *) echo "Option inconnue : $1" >&2; exit 1 ;;
    esac
done

info()   { echo -e "\e[1;34m[INFO]\e[0m $*"; }
ok()     { echo -e "\e[1;32m[ OK ]\e[0m $*"; }
alerte() { echo -e "\e[1;33m[ALERTE]\e[0m $*"; }
erreur() { echo -e "\e[1;31m[ERREUR]\e[0m $*" >&2; exit 1; }

# Le script est dans projet_simulation/ ; on travaille depuis le dossier parent
DOSSIER_PROJET="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DOSSIER_PARENT="$(dirname "$DOSSIER_PROJET")"
PAQUET="$(basename "$DOSSIER_PROJET")"
VENV="$DOSSIER_PARENT/venv"
SCHEMA="$DOSSIER_PROJET/database/schema.sql"

[[ -f "$SCHEMA" ]] || erreur "database/schema.sql introuvable dans $DOSSIER_PROJET"

# =============================================================================
# PHASE ROOT : paquets, MariaDB, pare-feu
# =============================================================================
phase_root() {
    info "Installation des paquets système (MariaDB, Python, ufw)..."
    export DEBIAN_FRONTEND=noninteractive
    apt-get update -qq
    apt-get install -y -qq mariadb-server python3 python3-venv python3-pip ufw >/dev/null
    ok "Paquets installés"

    info "Démarrage de MariaDB..."
    systemctl enable --now mariadb >/dev/null 2>&1
    systemctl is-active --quiet mariadb || erreur "MariaDB ne démarre pas (journalctl -u mariadb)"
    ok "MariaDB actif"

    info "Création de la base, de l'utilisateur et des tables..."
    local client_sql
    client_sql="$(command -v mariadb || command -v mysql)"
    # Sous Debian, root se connecte par socket Unix : aucun mot de passe nécessaire
    "$client_sql" < "$SCHEMA"
    local tables
    tables="$("$client_sql" -N -e "SHOW TABLES FROM simu_db;" | tr '\n' ' ')"
    [[ -n "${tables// /}" ]] || erreur "Aucune table créée dans simu_db"
    ok "Base simu_db prête (tables : $tables)"

    info "Configuration du pare-feu..."
    ufw allow 22/tcp >/dev/null            # SSH d'abord, sinon on se coupe l'accès
    if [[ -n "$IP_CLIENT" ]]; then
        ufw allow from "$IP_CLIENT" to any port "$PORT" proto tcp >/dev/null
        ok "Port $PORT ouvert uniquement pour $IP_CLIENT"
    else
        ufw allow "$PORT"/tcp >/dev/null
        ok "Port $PORT ouvert"
    fi
    # Port 3306 volontairement fermé : seule la VM 1 utilise la base
    ufw --force enable >/dev/null
    ok "Pare-feu actif"
}

if [[ $PHASE_ROOT -eq 1 ]]; then
    [[ $EUID -eq 0 ]] || erreur "La phase root doit tourner en root"
    phase_root
    exit 0
fi

# Lance la phase root avec un seul mot de passe : root direct, sudo, ou su
ARGS_ROOT=(--phase-root --port "$PORT")
[[ -n "$IP_CLIENT" ]] && ARGS_ROOT+=(--ip-client "$IP_CLIENT")
if [[ $EUID -eq 0 ]]; then
    phase_root
elif command -v sudo >/dev/null 2>&1 && id -nG | grep -qwE "sudo|wheel"; then
    sudo bash "$0" "${ARGS_ROOT[@]}"
else
    info "Mot de passe root nécessaire pour installer les paquets :"
    su root -c "bash $(printf '%q ' "$0" "${ARGS_ROOT[@]}")"
fi

# =============================================================================
# PHASE UTILISATEUR : environnement Python + lancement
# =============================================================================
info "Préparation de l'environnement Python ($VENV)..."
[[ -d "$VENV" ]] || python3 -m venv "$VENV"
if ! "$VENV/bin/python" -c "import mysql.connector" 2>/dev/null; then
    "$VENV/bin/pip" install -q --upgrade pip
    "$VENV/bin/pip" install -q mysql-connector-python
fi
ok "Dépendances Python installées"

info "Test de la connexion Python -> MariaDB..."
cd "$DOSSIER_PARENT"
"$VENV/bin/python" -c "
from $PAQUET.database.stats_db import StatsDB
StatsDB().get_connection().close()
" || erreur "Connexion à simu_db impossible avec simu_user (voir schema.sql et stats_db.py)"
ok "Connexion à la base OK"

IPS="$(hostname -I 2>/dev/null | xargs || true)"
echo
ok "VM 1 prête. Adresse(s) IP : ${IPS:-inconnue}"
echo "    Sur la VM 2 : bash projet_simulation/setup_vm2_client.sh"
echo

# Choix du point d'entrée selon l'avancement du projet
if grep -q -- "--role" "$DOSSIER_PROJET/main.py" 2>/dev/null; then
    COMMANDE=("$VENV/bin/python" -m "$PAQUET.main" --role server --port "$PORT")
elif grep -qE "\.(bind|listen)\(" "$DOSSIER_PROJET/network/socket_server.py" 2>/dev/null; then
    # Uniquement si c'est un vrai serveur (bind/listen), pas un client qui se connecte
    COMMANDE=("$VENV/bin/python" -m "$PAQUET.network.socket_server")
else
    alerte "Pas encore de serveur réseau (main.py --role / socket_server.py) :"
    alerte "lancement de la simulation seule, sans envoi vers la VM 2."
    COMMANDE=("$VENV/bin/python" -m "$PAQUET.simulation")
fi

if [[ $LANCER -eq 1 ]]; then
    info "Lancement : ${COMMANDE[*]}  (Ctrl+C pour arrêter)"
    exec "${COMMANDE[@]}"
else
    echo "Pour lancer : cd $DOSSIER_PARENT && ${COMMANDE[*]}"
fi