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

## 3. Répartition des Rôles et des Tâches

### 👨‍💻 Lucas BUCHER — Lead Développement Python & Simulation
* **Responsabilité :** Algorithmes principaux, simulation du réseau routier et calcul d'itinéraire.
* **Tâches :**
  - [ ] Développement du moteur de simulation en Python (carrefours, densité du trafic).
  - [ ] Algorithme de calcul d'itinéraire optimal (Point A vers Point B).
  - [ ] Cartographie logicielle / Spécifications de l'IA graphie.
  - [ ] Participation à la rédaction du Cahier des charges (Partie technique).

---

### 🛠️ Benjamin DEIBER — Infrastructure, Scripts & Documentation
* **Responsabilité :** Gestion de l'environnement, scripts PowerShell, BDD et structuration documentaire.
* **Tâches :**
  - [ ] Développement des scripts **PowerShell** pour la gestion de l'autorisation d'accès.
  - [ ] Conception et interfaçage de la Base de Données (stockage des feux, accès, usagers).
  - [ ] Gestion et structuration du dépôt **GitHub**.
  - [ ] Rédaction de la **Doc d'installation** (`docs/installation.md`) et de la **Doc d'usage** (`docs/usage.md`).

---

### 📊 Quentin ALTINOK — Logique V2X, Finance & Gestion de Projet
* **Responsabilité :** Interconnexion V2I/V2V, gestion administrative et chiffrage financier.
* **Tâches :**
  - [ ] Modélisation de la logique V2I (feux tricolores) et V2V (alerte usagers).
  - [ ] Rédaction des **Comptes-Rendus Hebdomadaires** (CR 2, 3, 4 et 5).
  - [ ] Élaboration du **Livrable Finance** (chiffrage et budget du projet).
  - [ ] Rédaction de la **Doc de réponses** (`docs/reponses.md`).

---

## 4. Matrice des Livrables Obligatoires

| Livrable | Responsable Principal | Relecture / Validation | Échéance | Statut |
| :--- | :--- | :--- | :--- | :---: |
| **QQOQCP & Cahier des Charges** | Lucas BUCHER | Quentin & Benjamin | 25/09/2026 | 🟡 En cours |
| **Moteur Python & Simulation** | Lucas BUCHER | Quentin ALTINOK | 25/10/2026 | ⚪ À faire |
| **Scripts PowerShell & BDD** | Benjamin DEIBER | Lucas BUCHER | 25/10/2026 | ⚪ À faire |
| **Comptes-Rendus Hebdomadaires (CR2–CR5)** | Quentin ALTINOK | Benjamin DEIBER | Hebdomadaire | 🟡 En cours |
| **Livrable Finance** | Quentin ALTINOK | Lucas BUCHER | 15/11/2026 | ⚪ À faire |
| **Documentations (`README`, Docs)** | Benjamin DEIBER | Tous | 15/11/2026 | 🟡 En cours |
| **Dépôt GitHub partagé (`fdrouhin-uha`)** | Benjamin DEIBER | Tous | 15/11/2026 | 🟡 En cours |

---


## 🏗️ Architecture du Projet

Le projet adopte une architecture modulaire, orientée objet et multi-threadée, découpée selon la séparation des responsabilités.

```text
projet_simulation/
├── models/                     # Modèles métiers (1 fichier par classe)
│   ├── __init__.py             # Exportation des classes pour des imports simplifiés
│   ├── voiture.py              # Classe de base pour les véhicules
│   ├── voiture_autonome.py     # Logique de conduite automatisée (hérite de Voiture)
│   ├── vehicule_urgence.py     # Gestion du trajet GPS et priorité (hérite de Voiture)
│   └── feu_carrefour.py        # Gestion des états et cycles des feux de circulation
│
├── database/                   # Gestion de la persistance des données
│   ├── __init__.py
│   └── stats_db.py             # Base SQLite (historique des passages, temps d'attente, KPI)
│
├── network/                    # Couche de communication par Sockets
│   ├── __init__.py
│   ├── socket_server.py        # Serveur TCP diffusant l'état de la simulation
│   └── socket_client.py        # Client TCP (s'exécute dans un thread dédié côté GUI)
│
├── gui/                        # Interface Graphique (IHM)
│   ├── __init__.py
│   ├── map_canvas.py           # Composant de rendu visuel (carte, véhicules, feux)
│   ├── stats_panel.py          # Tableau de bord et graphiques en temps réel
│   └── main_window.py          # Fenêtre principale assemblant l'IHM
│
├── utils/                      # Fonctions utilitaires
│   ├── __init__.py
│   └── gps_utils.py            # Conversions GPS -> Pixels et calculs de distances réelles
│
├── simulation.py               # Moteur algorithmique principal & boucle de physique
├── main.py                     # Point d'entrée principal de l'application
└── setup_and_run.ps1           # Script PowerShell d'installation et de lancement
