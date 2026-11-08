# SAÉ 3.02 — Développer une application communicante

**Groupe :** Zero Trust
**Membres :**

| Nom | Prénom | Rôle principal |
| :--- | :--- | :--- |
| BUCHER | Lucas | Moteur de simulation et modèles objets (`models/`, `simulation.py`) |
| DEIBER | Benjamin | Base de données, interface graphique, scripts de déploiement (`database/`, `gui/`, `setup_*.sh`) |
| ALTINOK | Quentin | Réseau TCP et calculs GPS (`network/`, `utils/`) |

**Enseignant :** `fdrouhin-uha`

---

## 1. Présentation

Maquette d'un **carrefour connecté** : quand un véhicule d'urgence (pompiers, ambulance) arrive à moins de **50 m** de la ligne d'arrêt, le feu de son axe passe automatiquement au **vert** et l'axe perpendiculaire au **rouge**, jusqu'à ce qu'il ait traversé le carrefour.

L'application est **distribuée sur deux machines virtuelles Debian** :

```
┌──────────────── VM 1 : serveur ────────────────┐          ┌──────────── VM 2 : client ────────────┐
│  simulation.py  ──►  socket_server.py  ────────┼── TCP ──►│  socket_client.py (QThread)           │
│  (physique, feux,     (port 5000, 1 ligne JSON  │  5000    │        │ signal state_received        │
│   règle des 50 m)      par état, 10 fois/s)     │          │        ▼                              │
│        │                                        │          │  main_window.py                       │
│        ▼                                        │          │   ├─ map_canvas.py  (carte GPS)       │
│  stats_db.py ──► MariaDB (simu_db)              │          │   └─ stats_panel.py (tableau de bord) │
└─────────────────────────────────────────────────┘          └───────────────────────────────────────┘
```

---

## 2. Arborescence

```text
SAE-3.02/
├── README.md                 # ce fichier
├── requirements.txt          # dépendances Python
├── Bilan_Projet.pdf          # bilan fonctionnel, technique et planning
├── IAGraphie.pdf             # usage des IA génératives
├── livrables/                # cahier des charges et comptes rendus hebdomadaires
└── projet_simulation/
    ├── main.py               # point d'entrée : --role server | client
    ├── simulation.py         # moteur : classe Simulation (step, etat, est_terminee)
    ├── models/               # Voiture, vehicule_urgence, feuDeCirculation
    ├── database/             # schema.sql + StatsDB (MariaDB)
    ├── network/              # socket_server.py (VM 1), socket_client.py (VM 2)
    ├── gui/                  # MainWindow, MapCanvas, StatsPanel (PyQt6)
    ├── utils/                # gps_utils.py : Haversine, mètres <-> GPS <-> pixels
    ├── setup_vm1_server.sh   # installation + lancement automatiques de la VM 1
    └── setup_vm2_client.sh   # installation + lancement automatiques de la VM 2
```

---

## 3. Installation

### Prérequis

- Deux VM **Debian 12** , sur le **même réseau**.
  Avec VirtualBox : carte réseau 1 en «NAT» et carte réseau 2 en « Accès par pont » sur les deux VM
- La VM 2 doit avoir un **bureau graphique** (l'interface s'ouvre dans une fenêtre).
- Python **3.11 ou plus récent**, Git, et un accès Internet pour installer les paquets.

### Méthode recommandée : scripts automatiques

Les scripts installent tout (paquets, base de données, pare-feu, environnement virtuel) puis lancent l'application. Ils demandent le mot de passe root une seule fois si `sudo` n'est pas configuré, et peuvent être relancés sans risque.

**Sur la VM 1 (en premier) :**

```bash
su -
apt install git
git clone https://github.com/debenji68/SAE-3.02.git
cd SAE-3.02
bash projet_simulation/setup_vm1_server.sh
```

Le script installe MariaDB, crée la base `simu_db` et l'utilisateur `simu_user` (`database/schema.sql`), ouvre le port 5000 dans le pare-feu `ufw`, crée le venv, vérifie la connexion à la base puis lance le serveur. Il affiche l'adresse IP de la VM à la fin.

**Sur la VM 2, depuis le terminal du bureau (pas en SSH) :**

```bash
su - 
apt install git
exit
git clone https://github.com/debenji68/SAE-3.02.git
cd SAE-3.02
bash projet_simulation/setup_vm2_client.sh
```

Le script installe PyQt6, **cherche tout seul la VM 1** sur le réseau local (port 5000) puis ouvre l'interface. Si la recherche échoue, donner l'IP : `bash projet_simulation/setup_vm2_client.sh 192.168.56.10`.

**Si il y a un problème lors de l'utilisation du script bash a cause d'un processus, il faut kill ce dernier :**
    A faire
    ```bash
    su -
    kill <N°processus>
    ```
    Exemple :
        [INFO] Installation des paquets système (MariaDB, Python, ufw)...
        E: Impossible d'obtenir le verrou /var/lib/apt/lists/lock. Il est occupé par le processus 1647 (packagekitd)
        E: Impossible de verrouiller le répertoire /var/lib/apt/lists/
        root@vbox:~/SAE-3.02# kill 1647

### Méthode manuelle (pas à pas)

**1. Cloner le dépôt**

```bash
git clone https://github.com/debenji68/SAE-3.02.git
cd SAE-3.02
```

**2. Créer et activer l'environnement virtuel**

```bash
python3 -m venv venv
source venv/bin/activate          # Linux / macOS
# venv\Scripts\Activate.ps1       # Windows PowerShell
```

**3. Installer les dépendances**

```bash
pip install -r requirements.txt
```

**4. Créer la base de données (VM 1 uniquement)**

```bash
sudo apt install mariadb-server
sudo systemctl enable --now mariadb
sudo mariadb < projet_simulation/database/schema.sql
```

**5. Ouvrir le port du serveur (VM 1 uniquement)**

```bash
sudo ufw allow 22/tcp      # SSH d'abord, pour ne pas perdre l'accès
sudo ufw allow 5000/tcp
sudo ufw enable
```

---

## 4. Utilisation

Toutes les commandes se lancent **depuis la racine du dépôt** (le dossier qui contient `projet_simulation/`), venv activé.

### Lancer l'application

| Machine | Commande |
| :--- | :--- |
| VM 1 — serveur | `python3 -m projet_simulation.main --role server` |
| VM 2 — interface | `python3 -m projet_simulation.main --role client --host <IP_VM1>` |

Options : `--port <N>` pour changer le port (5000 par défaut).

> ⚠️ Lancer avec `python3 -m projet_simulation.main` et non `python3 projet_simulation/main.py`, sinon les imports du paquet `projet_simulation` échouent.

### Exemples

**Test sur une seule machine** (deux terminaux, MariaDB installée ; la simulation démarre quand l'interface se connecte) :

```bash
# Terminal 1
python3 -m projet_simulation.main --role server
# Terminal 2
python3 -m projet_simulation.main --role client --host 127.0.0.1
```

**Tester la simulation seule, sans réseau ni interface :**

```bash
python3 -m projet_simulation.simulation
```

Exemple de sortie :

```
=== Démarrage de la simulation du carrefour ===
  >> Passage prioritaire : Pompier1 à 40.0 m du feu
  >> Passage prioritaire : Ambulance1 à 40.0 m du feu
[1.0s] Feu X : vert | Feu Y : rouge
  Pompier (X)   : pos = -36.1, v = 50.0 km/h
  Ambulance (Y) : pos = -36.1, v = 50.0 km/h
...
=== Fin de la simulation à 24.0s ===
```

**Vérifier la réception réseau sans interface** (affiche les états reçus pendant 15 s) :

```bash
python3 -m projet_simulation.network.socket_client <IP_VM1>
```

**Consulter les statistiques enregistrées (VM 1) :**

```bash
sudo mariadb -e "SELECT * FROM simu_db.evenement;"
sudo mariadb -e "SELECT * FROM simu_db.info_traffic ORDER BY id DESC LIMIT 5;"
```

### Ce qu'on voit dans l'interface

- **Onglet Simulation** : le carrefour, les feux (rouge / orange / vert), les voitures en **bleu** et les véhicules d'urgence en **jaune**, chacun sur la voie de droite de son sens de circulation.
- **Onglet Statistique** : temps simulé, nombre de passages prioritaires, vitesse moyenne et nombre de véhicules dans la zone.

### Configuration

| Paramètre | Fichier | Valeur par défaut |
| :--- | :--- | :--- |
| Coordonnées GPS du carrefour | `utils/gps_utils.py` (`CARREFOUR_LAT`, `CARREFOUR_LON`) | 47.7508, 7.3359 (Mulhouse) |
| Identifiants MariaDB | `database/schema.sql` et `database/stats_db.py` | `simu_user` / `simu_password` |
| Port TCP | option `--port` | 5000 |

---

## 5. Format des échanges réseau

Le serveur envoie **10 fois par seconde** l'état complet de la simulation, **une ligne JSON par message** (terminée par `\n`) :

```json
{"temps": 3.2,
 "vehicules": [{"id": "Pompier1", "x": -8.3, "y": 0.0, "lat": 47.7508, "lon": 7.33579,
                "vitesse": 50.0, "axe": "x", "sens": 1, "est_urgence": true}],
 "feux": [{"id": "feu_x", "x": -10.0, "y": -10.0, "lat": 47.75071, "lon": 7.33577,
           "etat": "vert", "force": true}],
 "kpis": {"vitesse_moyenne": 43.6, "nb_vehicule": 10, "nb_urgences": 2}}
```

Positions en mètres autour du carrefour (`x` vers l'est, `y` vers le nord) et en GPS (`lat`, `lon`).

Fonctionnement du serveur (`network/socket_server.py`) :

- **un client à la fois** : quand l'interface se ferme, le serveur attend la connexion suivante sans redémarrer ;
- **la simulation n'avance que lorsqu'un client est connecté** : sans VM 2, rien ne bouge et rien n'est enregistré en base ;
- **un nouveau scénario démarre automatiquement** quand tous les véhicules ont quitté la zone (environ 24 s) ou après 60 s.

---

## 6. Base de données (`simu_db`)

| Table | Contenu | Écrite par |
| :--- | :--- | :--- |
| `evenement` | Un passage prioritaire : véhicule, feu, distance, horodatage | `Simulation` quand un véhicule d'urgence entre dans la zone des 50 m |
| `info_traffic` | Vitesse moyenne et nombre de véhicules, horodatés | `Simulation`, une fois par seconde simulée |

---

## 7. Dépannage

| Problème | Solution |
| :--- | :--- |
| `Can't connect to MySQL server` | MariaDB est arrêtée : `sudo systemctl start mariadb`. La simulation a besoin de la base pour démarrer. |
| `ModuleNotFoundError: projet_simulation` | Lancer depuis la racine du dépôt avec `python3 -m ...` |
| La VM 2 ne trouve pas le serveur | Vérifier que le serveur tourne, que les deux VM sont sur le même réseau et que le port 5000 est ouvert (`sudo ufw status`). |
| `$'\r': command not found` en lançant un script | Le script a été enregistré avec des fins de ligne Windows : `sed -i 's/\r$//' projet_simulation/*.sh` (le `.gitattributes` l'évite normalement). |
| La fenêtre ne s'ouvre pas | Lancer depuis le bureau de la VM 2, pas en SSH. |
