#!/usr/bin/env bash
# =============================================================================
# SAE 3.02 - VM 2 (Client : interface graphique PyQt6)
#
# Installe TOUT ce qu'il faut puis lance l'interface :
#   bash setup_vm2_client.sh            (cherche la VM 1 tout seul sur le réseau)
#   bash setup_vm2_client.sh <IP_VM1>   (si la recherche automatique échoue)
#
# Options :
#   --port <N>         port TCP du serveur (5000 par défaut)
#   --sans-lancement   installe seulement
#
# À lancer depuis le terminal du BUREAU de la VM (pas en SSH : il faut un écran).
# Lancer d'abord le script de la VM 1. Relançable sans risque.
# =============================================================================
set -euo pipefail

PORT=5000
IP_SERVEUR=""
LANCER=1
PHASE_ROOT=0

while [[ $# -gt 0 ]]; do
    case "$1" in
        --port)           PORT="${2:?--port attend un numéro}"; shift 2 ;;
        --sans-lancement) LANCER=0; shift ;;
        --phase-root)     PHASE_ROOT=1; shift ;;   # usage interne
        -h|--help)        sed -n '2,16p' "$0"; exit 0 ;;
        -*) echo "Option inconnue : $1" >&2; exit 1 ;;
        *)  IP_SERVEUR="$1"; shift ;;
    esac
done

info()   { echo -e "\e[1;34m[INFO]\e[0m $*"; }
ok()     { echo -e "\e[1;32m[ OK ]\e[0m $*"; }
alerte() { echo -e "\e[1;33m[ALERTE]\e[0m $*"; }
erreur() { echo -e "\e[1;31m[ERREUR]\e[0m $*" >&2; exit 1; }

DOSSIER_PROJET="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DOSSIER_PARENT="$(dirname "$DOSSIER_PROJET")"
PAQUET="$(basename "$DOSSIER_PROJET")"
VENV="$DOSSIER_PARENT/venv"

[[ -f "$DOSSIER_PROJET/gui/main_window.py" ]] || erreur "gui/main_window.py introuvable dans $DOSSIER_PROJET"

# =============================================================================
# PHASE ROOT : paquets système (Python + Qt)
# =============================================================================
phase_root() {
    export DEBIAN_FRONTEND=noninteractive
    info "Installation de Python..."
    apt-get update -qq
    apt-get install -y -qq python3 python3-venv python3-pip iproute2 >/dev/null
    ok "Python installé"

    info "Installation de PyQt6..."
    # Paquet Debian en priorité : il amène aussi les bibliothèques Qt / X11
    if apt-get install -y -qq python3-pyqt6 >/dev/null 2>&1; then
        ok "PyQt6 installé par apt"
    else
        alerte "python3-pyqt6 indisponible (Debian < 12) : bibliothèques pour la version pip"
        apt-get install -y -qq libgl1 libegl1 libfontconfig1 libdbus-1-3 \
            libxkbcommon-x11-0 libxcb-cursor0 libxcb-icccm4 libxcb-image0 \
            libxcb-keysyms1 libxcb-randr0 libxcb-render-util0 libxcb-shape0 \
            libxcb-xinerama0 libxcb-xfixes0 >/dev/null
    fi
}

if [[ $PHASE_ROOT -eq 1 ]]; then
    [[ $EUID -eq 0 ]] || erreur "La phase root doit tourner en root"
    phase_root
    exit 0
fi

if [[ $EUID -eq 0 ]]; then
    phase_root
    alerte "Script lancé en root : l'interface graphique risque de ne pas s'ouvrir."
    alerte "Préférez le lancer en utilisateur normal (le mot de passe root sera demandé)."
elif command -v sudo >/dev/null 2>&1 && id -nG | grep -qwE "sudo|wheel"; then
    sudo bash "$0" --phase-root
else
    info "Mot de passe root nécessaire pour installer les paquets :"
    su root -c "bash $(printf '%q ' "$0" --phase-root)"
fi

# =============================================================================
# PHASE UTILISATEUR : environnement Python
# =============================================================================
info "Préparation de l'environnement Python ($VENV)..."
if [[ ! -d "$VENV" ]]; then
    # --system-site-packages : le venv voit le PyQt6 installé par apt
    python3 -m venv --system-site-packages "$VENV"
fi
if ! "$VENV/bin/python" -c "import PyQt6.QtWidgets" 2>/dev/null; then
    "$VENV/bin/pip" install -q --upgrade pip
    "$VENV/bin/pip" install -q PyQt6
fi
"$VENV/bin/python" -c "import PyQt6.QtWidgets" || erreur "PyQt6 ne s'importe pas"
ok "PyQt6 opérationnel"

# =============================================================================
# Recherche de la VM 1
# =============================================================================
port_ouvert() { timeout 1 bash -c "exec 3<>/dev/tcp/$1/$PORT" 2>/dev/null; }

chercher_serveur() {
    # Teste le port du serveur sur toutes les machines des réseaux locaux (/24)
    local mes_ips reseau ip resultats
    mes_ips="$(hostname -I 2>/dev/null || true)"
    resultats="$(mktemp)"
    for ip in $mes_ips; do
        [[ "$ip" =~ ^([0-9]+\.[0-9]+\.[0-9]+)\.[0-9]+$ ]] || continue
        reseau="${BASH_REMATCH[1]}"
        [[ "$reseau" == 127.* ]] && continue
        for i in $(seq 1 254); do
            [[ "$reseau.$i" == "$ip" ]] && continue
            ( timeout 0.5 bash -c "exec 3<>/dev/tcp/$reseau.$i/$PORT" 2>/dev/null \
                && echo "$reseau.$i" >> "$resultats" ) &
        done
    done
    wait
    head -n 1 "$resultats"
    rm -f "$resultats"
}

if [[ -z "$IP_SERVEUR" ]]; then
    info "Recherche de la VM 1 sur le réseau (port $PORT)..."
    IP_SERVEUR="$(chercher_serveur)"
    if [[ -n "$IP_SERVEUR" ]]; then
        ok "Serveur trouvé : $IP_SERVEUR"
    else
        alerte "Serveur introuvable automatiquement (VM 1 éteinte, serveur non lancé,"
        alerte "ou VM sur des réseaux différents : en VirtualBox, utiliser un réseau interne"
        alerte "ou « réseau privé hôte » sur les deux VM, pas le NAT)."
        if [[ -t 0 ]]; then
            read -r -p "Adresse IP de la VM 1 (Entrée pour ignorer) : " IP_SERVEUR
        fi
    fi
fi

if [[ -n "$IP_SERVEUR" ]]; then
    if port_ouvert "$IP_SERVEUR"; then
        ok "Serveur joignable sur $IP_SERVEUR:$PORT"
    else
        alerte "$IP_SERVEUR:$PORT ne répond pas pour l'instant (le client réessaiera)."
    fi
fi

# =============================================================================
# Lancement
# =============================================================================
if [[ -z "${DISPLAY:-}" && -z "${WAYLAND_DISPLAY:-}" ]]; then
    alerte "Aucun écran détecté : lancez ce script depuis le terminal du bureau de la VM."
    [[ $LANCER -eq 1 ]] && erreur "Impossible d'ouvrir la fenêtre sans affichage graphique."
fi

cd "$DOSSIER_PARENT"
if grep -q -- "--role" "$DOSSIER_PROJET/main.py" 2>/dev/null; then
    [[ -n "$IP_SERVEUR" ]] || erreur "IP de la VM 1 inconnue : bash $0 <IP_VM1>"
    COMMANDE=("$VENV/bin/python" -m "$PAQUET.main" --role client --host "$IP_SERVEUR" --port "$PORT")
else
    alerte "main.py ne gère pas encore --role client : ouverture de l'interface seule,"
    alerte "sans connexion au serveur."
    # Lancé comme fichier : les imports « from map_canvas import ... » de gui/ fonctionnent
    COMMANDE=("$VENV/bin/python" "$DOSSIER_PROJET/gui/main_window.py")
fi

echo
ok "VM 2 prête."
if [[ $LANCER -eq 1 ]]; then
    info "Lancement : ${COMMANDE[*]}"
    exec "${COMMANDE[@]}"
else
    echo "Pour lancer : cd $DOSSIER_PARENT && ${COMMANDE[*]}"
fi