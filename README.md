# SAE-3.02
# Planning et Répartition des Tâches — SAÉ 3.02

**Projet :** Application de régulation du trafic pour véhicules prioritaires (Maquette)  
**Équipe :** Bucher Lucas, Deiber Benjamin, Altinok Quentin  
**Enseignant / Tuteur :** `fdrouhin-uha`  

---

## 1. Vue d'ensemble du projet

Ce projet a pour objectif de réaliser la **maquette d'une application** permettant aux véhicules prioritaires (ambulances, pompiers, police) de se déplacer le plus rapidement et le plus sûrement possible d'un point A à un point B en fonction de la densité du trafic.

---

```
## 📅 Planning de Développement Prévisionnel

Le projet est découpé en 4 phases principales afin d'assurer un développement progressif et sans blocage sous PyCharm avant le déploiement sur les VM.

| Phase | Objectifs & Livrables | Tâches par Membre |
| :--- | :--- | :--- |
| **Phase 1 : Socle & Modèles**<br>*(Semaine 1)* | • Structure du dépôt Git.<br>• Classes POO de base.<br>• Structure BDD MariaDB.<br>• Protocole JSON de communication. | • **Lucas :** Création du dossier `models/` (`voiture.py`, `feu_carrefour.py`, etc.).<br>• **Quentin :** Implémentation des calculs GPS/Haversine dans `utils/gps_utils.py`.<br>• **Benjamin :** Création du schéma SQL `database/schema.sql` et de la classe `stats_db.py`. |
| **Phase 2 : Moteur & Réseau**<br>*(Semaine 2)* | • Boucle de simulation fonctionnelle.<br>• Règle des 50 m opérationnelle.<br>• Sockets TCP fonctionnels inter-modules. | • **Lucas :** Développement de `simulation.py` (physique, déplacements, priorité d'urgence).<br>• **Quentin :** Développement du serveur TCP (`socket_server.py`) et client (`socket_client.py`).<br>• **Benjamin :** Écriture des requêtes d'insertion et de statistiques dans `stats_db.py`. |
| **Phase 3 : Interface Graphique**<br>*(Semaine 3)* | • Rendu dynamique de la carte.<br>• Intégration du tableau de bord.<br>• Connexion GUI <-> Thread Client. | • **Lucas :** Finalisation de la logique globale et intégration avec la BDD dans `simulation.py`.<br>• **Quentin :** Tests de sérialisation JSON et gestion des reconnexions Sockets.<br>• **Benjamin :** Développement de `gui/map_canvas.py`, `stats_panel.py` et `main_window.py`. |
| **Phase 4 : Automation & VM**<br>*(Semaine 4)* | • Scripts Bash d'installation.<br>• Déploiement sur VM 1 et VM 2.<br>• Tests d'intégration réseau & BDD. | • **Lucas :** Validation du moteur de simulation sous Linux (VM 1).<br>• **Quentin :** Tests de communication réseau inter-VM (VM 1 <-> VM 2).<br>• **Benjamin :** Rédaction de `setup_vm1_server.sh` et `setup_vm2_client.sh`, tests de déploiement global. |
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
