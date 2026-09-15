# SAE-3.02
# Planning et Répartition des Tâches — SAÉ 3.02

**Projet :** Application de régulation du trafic pour véhicules prioritaires (Maquette)  
**Équipe :** Bucher Lucas, Deiber Benjamin, Altinok Quentin  
**Enseignant / Tuteur :** `fdrouhin-uha`  

---

## 1. Vue d'ensemble du projet

Ce projet a pour objectif de réaliser la **maquette d'une application** permettant aux véhicules prioritaires (ambulances, pompiers, police) de se déplacer le plus rapidement et le plus sûrement possible d'un point A à un point B en fonction de la densité du trafic.

---

## 2. Planning Prévisionnel (Septembre – Novembre 2026)

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│ PHASE 1 : Cadrage & Spécifications (09/09 - 25/09)                              │
│  ├─ Rédaction du Cahier des charges & QQOQCP finalisé                             │
│  └─ Architecture logicielle & choix des modules Python                           │
├──────────────────────────────────────────────────────────────────────────────────┤
│ PHASE 2 : Développement de la Maquette (26/09 - 25/10)                           │
│  ├─ Module 1 : Simulation de trafic & Algorithmique (Point A -> Point B)         │
│  ├─ Module 2 : Logique V2I / V2V & Gestion des priorités aux carrefours           │
│  └─ Module 3 : Scripts d'autorisation / Administration (PowerShell & BDD)        │
├──────────────────────────────────────────────────────────────────────────────────┤
│ PHASE 3 : Intégration, Tests & Rédaction Docs (26/10 - 08/11)                     │
│  ├─ Tests d'intégration de la maquette                                           │
│  ├─ Rédaction des documentations (Installation, Usage, Réponses, README)         │
│  └─ Préparation du dépôt GitHub structuré                                        │
├──────────────────────────────────────────────────────────────────────────────────┤
│ PHASE 4 : Finalisation & Soutenance (09/11 - 26/11)                              │
│  ├─ 15 Novembre : Remise finale du livrable intermédiaire / GitHub               │
│  ├─ 20 Novembre : Évaluation RZ Séance 1 (1h15)                                  │
│  └─ 26 Novembre : Évaluation RZ Séance 2 (03h30) & Préparation soutenance        │
└──────────────────────────────────────────────────────────────────────────────────┘
```

---

## 👥 Répartition des Rôles

| Membre | Périmètre principal | Composants gérés |
| :--- | :--- | :--- |
| **Lucas** | Moteur & Logique métier | `models/`, `simulation.py`, `main.py` |
| **Quentin** | Réseau & Mathématiques GPS | `network/`, `utils/` |
| **Benjamin** | Interface Graphique, BDD & Automation | `gui/`, `database/`, `setup_vm1_server.sh`, `setup_vm2_client.sh` |

---

## 📁 Structure du Projet

```text
projet_simulation/
├── models/                     # [Lucas] Modèles objets (1 classe par fichier)
│   ├── __init__.py             # Exporte les classes pour simplifier les imports
│   ├── voiture.py              # Classe de base (position XY/GPS, vitesse, identifiant)
│   ├── voiture_autonome.py     # Hérite de Voiture, gère les distances de sécurité
│   ├── vehicule_urgence.py     # Hérite de Voiture, intègre l'itinéraire et la priorité
│   └── feu_carrefour.py        # Gestion des états (vert/orange/rouge) et cycles des feux
│
├── database/                   # [Benjamin] Persistance des données (MariaDB)
│   ├── __init__.py             # Package Python
│   ├── schema.sql              # Script SQL de création de la BDD et des tables
│   └── stats_db.py             # Interface Python MariaDB (connexion, requêtes, logs)
│
├── network/                    # [Quentin] Communication inter-VM par Sockets TCP
│   ├── __init__.py             # Package Python
│   ├── socket_server.py        # Serveur TCP sur VM 1 (port 5000), diffusion de l'état en JSON
│   └── socket_client.py        # Client TCP sur VM 2 (thread dédié pour l'IHM)
│
├── gui/                        # [Benjamin] Interface graphique utilisateur
│   ├── __init__.py             # Package Python
│   ├── map_canvas.py           # Composant de rendu (carte, véhicules, feux, trajets GPS)
│   ├── stats_panel.py          # Panneau d'indicateurs (KPIs et graphiques de fluidité)
│   └── main_window.py          # Fenêtre principale assemblant la carte et les statistiques
│
├── utils/                      # [Quentin] Fonctions utilitaires
│   ├── __init__.py             # Package Python
│   └── gps_utils.py            # Calculs mathématiques (conversion GPS <-> Pixels, formule de Haversine)
│
├── simulation.py               # [Lucas] Moteur algorithmique principal & boucle de physique
├── main.py                     # [Lucas] Point d'entrée de l'application
├── setup_vm1_server.sh         # [Benjamin] Script Bash d'installation et de lancement (VM 1)
└── setup_vm2_client.sh         # [Benjamin] Script Bash d'installation et de lancement (VM 2)

📜 Rôle Détaillé Fichier par Fichier
🔹 Racines & Scripts

    main.py : Point d'entrée de l'application. Initialise les composants selon le rôle sélectionné (--role server ou --role client).

    simulation.py : Boucle physique principale. Calcule les déplacements des véhicules, vérifie la règle des 50 mètres du véhicule d'urgence et ordonne le forçage des feux.

    setup_vm1_server.sh : Automatise sur la VM 1 la configuration de MariaDB, l'exécution du script database/schema.sql, l'ouverture du pare-feu (ufw), la création du venv et le lancement du moteur.

    setup_vm2_client.sh : Automatise sur la VM 2 l'installation des dépendances graphiques, la création du venv et la connexion au serveur via son adresse IP.

🔹 Dossier models/

    models/voiture.py : Définit les attributs de base de tout véhicule (coordonnées, vitesse, cap).

    models/voiture_autonome.py : Ajoute la conduite adaptative pour maintenir une distance de sécurité avec le véhicule précédent.

    models/vehicule_urgence.py : Contient la logique d'itinéraire prioritaire et calcule sa distance en temps réel par rapport aux intersections.

    models/feu_carrefour.py : Modélise les feux de circulation (couleur, temps de cycle, forçage prioritaire).

🔹 Dossier database/

    database/schema.sql : Fichier DDL contenant les requêtes SQL de création de la base de données (simu_db) et des tables (evenements_urgence, metriques_trafic).

    database/stats_db.py : Module Python d'interaction avec MariaDB via mysql-connector-python. Exécute les requêtes d'insertion d'événements et extrait les KPI pour l'interface graphique.

🔹 Dossier network/

    network/socket_server.py : Écoute sur la VM 1 (port 5000). Sérialise l'état complet du réseau routier au format JSON et l'envoie en continu aux clients connectés.

    network/socket_client.py : Tourne en arrière-plan dans un thread sur la VM 2. Reçoit le flux JSON et met à jour l'IHM en temps réel sans bloquer l'affichage.

🔹 Dossier gui/

    gui/map_canvas.py : Zone de dessin dynamique (canvas) pour représenter visuellement les routes, les voitures et l'état des feux.

    gui/stats_panel.py : Panneau d'affichage contenant les compteurs d'urgence et les graphiques de temps d'attente évité.

    gui/main_window.py : Fenêtre Tkinter (ou CustomTkinter) qui intègre le canevas de simulation et le panneau latéral de statistiques.

🔹 Dossier utils/

    utils/gps_utils.py : Fournit la formule de Haversine pour calculer la distance réelle en mètres entre deux points GPS et convertir ces positions sur le plan en pixels de l'écran.
