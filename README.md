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

## 5. Structure Recommandée du Dépôt GitHub

```text
SAE302-VehiculesPrioritaires/
├── README.md
├── docs/
│   ├── cahier_des_charges.md
│   ├── installation.md
│   ├── usage.md
│   ├── reponses.md
│   ├── finance.md
│   └── comptes_rendus/
│       ├── CR2.md
│       ├── CR3.md
│       ├── CR4.md
│       └── CR5.md
├── src/
│   ├── main.py
│   ├── simulation/
│   └── database/
└── scripts/
    └── auth_permissions.ps1
```
