import math
import time
from datetime import datetime
from projet_simulation.database.stats_db import StatsDB
from projet_simulation.models import feuDeCirculation, vehicule_urgence, Voiture

def trier_file_par_position(file_voitures, axe="x"):
    """Tire les véhicules d'une file selon leur sens et leur position par rapport au carrefour.

    Cela permet de s'assurer que la voiture de tête est traitée en premier.
    """
    sens_1 = []
    sens_moins_1 = []

    # Ventilation des véhicules selon leur sens de circulation
    for v in file_voitures:
        if v.sens_circulation == 1:
            sens_1.append(v)
        else:
            sens_moins_1.append(v)

    # Tri selon l'axe et le sens de progression vers l'intersection
    if axe == "x":
        sens_1.sort(key=lambda v: v.positionX, reverse=True)
        sens_moins_1.sort(key=lambda v: v.positionX)
    else:
        sens_1.sort(key=lambda v: v.positionY, reverse=True)
        sens_moins_1.sort(key=lambda v: v.positionY)

    return sens_1 + sens_moins_1

def calculer_metriques(vehicules, distance_max=100.0):
    """Renvoie (vitesse moyenne en km/h, nombre de véhicules) pour les véhicules encore dans la zone."""
    dans_zone = [v for v in vehicules if abs(v.positionX) <= distance_max and abs(v.positionY) <= distance_max]
    if not dans_zone:
        return 0.0, 0
    vitesse_moyenne = sum(v.vitesse for v in dans_zone) / len(dans_zone)
    return vitesse_moyenne, len(dans_zone)


if __name__ == "__main__":
    dt = 0.1  # Pas de temps de la simulation (100 ms)
    TEMPS_MAX = 60.0  # Durée maximale de la simulation en secondes
    DISTANCE_FIN = 100.0  # Seuil de distance au-delà duquel les véhicules ont quitté la zone

    # 1. Création des feux de circulation pour chaque axe
    feu_axe_x = feuDeCirculation("vert")
    feu_axe_y = feuDeCirculation("rouge")

    # 2. Création des véhicules d'urgence prioritaires
    pompier_x = vehicule_urgence("Pompier1", -50.0, 0.0, 50.0, sens_circulation=1)
    ambulance_y = vehicule_urgence("Ambulance1", 0.0, -50.0, 50.0, sens_circulation=1)

    # 3. Constitution des files de véhicules sur l'axe X et l'axe Y
    files_voitures_x = [
        pompier_x,
        Voiture("V2", -65.0, 0.0, 50.0, sens_circulation=1),
        Voiture("V3", -80.0, 0.0, 50.0, sens_circulation=1),
        Voiture("V6", 65.0, 0.0, 50.0, sens_circulation=-1),
        Voiture("V7", 80.0, 0.0, 50.0, sens_circulation=-1),
    ]

    files_voitures_y = [
        ambulance_y,
        Voiture("V4", 0.0, -65.0, 50.0, sens_circulation=1),
        Voiture("V5", 0.0, -80.0, 50.0, sens_circulation=1),
        Voiture("V8", 0.0, 65.0, 50.0, sens_circulation=-1),
        Voiture("V9", 0.0, 80.0, 50.0, sens_circulation=-1),
    ]

    # Initialisation des attributs liés aux virages pour tous les véhicules
    tous_les_vehicules = files_voitures_x + files_voitures_y
    for v in tous_les_vehicules:
        v.en_virage = False
        v.intention_virage = None
        v.type_virage_courant = None

    # Connexion à la bdd
    db = StatsDB()
    db.get_connection().close()
    print("Connexion à MariaDB OK")


    print("=== Démarrage de la simulation du carrefour ===")
    pas = 0

    # Boucle principale de la simulation
    while True:
        pas += 1
        temps_ecoule = pas * dt

        # A. Tri des files de circulation pour chaque axe
        files_voitures_x = trier_file_par_position(files_voitures_x, axe="x")
        files_voitures_y = trier_file_par_position(files_voitures_y, axe="y")

        # B. Gestion du cycle automatique standard des feux tricolores
        feu_axe_x.verifier_changement_automatique()
        feu_axe_y.verifier_changement_automatique()

        # C. Gestion de la priorité des véhicules d'urgence (rayon de détection de 50m)
        forcage_actif = False

        # Vérification pour le véhicule d'urgence sur l'axe X
        dist_pompier = math.sqrt(pompier_x.positionX ** 2 + pompier_x.positionY ** 2)
        if dist_pompier <= 50.0 and pompier_x.positionX < 0.0:
            if feu_axe_x.etat != "vert":
                feu_axe_x.etat = "vert"
                feu_axe_y.etat = "rouge"
            forcage_actif = True

        # Vérification pour le véhicule d'urgence sur l'axe Y (uniquement si le X n'a pas déjà forcé)
        dist_ambulance = math.sqrt(ambulance_y.positionX ** 2 + ambulance_y.positionY ** 2)
        if dist_ambulance <= 50.0 and ambulance_y.positionY < 0.0 and not forcage_actif:
            if feu_axe_y.etat != "vert":
                feu_axe_y.etat = "vert"
                feu_axe_x.etat = "rouge"

        # Listes temporaires pour basculer les véhicules d'un axe à l'autre lors d'un virage
        a_transferer_vers_y = []
        a_transferer_vers_x = []

        # D. Simulation physique et comportementale - Axe X
        for i, vehicule in enumerate(files_voitures_x):
            voiture_devant = None
            if i > 0 and files_voitures_x[i - 1].sens_circulation == vehicule.sens_circulation:
                voiture_devant = files_voitures_x[i - 1]

            if vehicule.en_virage:
                # Le véhicule poursuit son virage en cours
                vehicule.tourner(vehicule.type_virage_courant, dt)
                if not vehicule.en_virage:
                    # Fin du virage : réalignement et changement d'axe
                    vehicule.realigner_apres_virage()
                    vehicule.sens_circulation = 1 if math.sin(vehicule.orientation) > 0 else -1
                    a_transferer_vers_y.append(vehicule)

            elif getattr(vehicule, "intention_virage", None) is not None and -1.0 <= vehicule.positionX <= 1.0:
                # Déclenchement du virage si le véhicule atteint la zone d'intersection
                dir_init = "+X" if vehicule.sens_circulation == 1 else "-X"
                vehicule.initialiser_virage(dir_init, vehicule.intention_virage)
                vehicule.intention_virage = None

            else:
                # Déplacement en ligne droite avec gestion des feux et distances de sécurité
                vehicule.gerer_priorite_feu_et_file(
                    feu=feu_axe_x,
                    position_ligne_arret=0.0,
                    voiture_devant=voiture_devant,
                    distance_securite=5.0,
                    axe="x",
                    dt=dt
                )

        # E. Simulation physique et comportementale - Axe Y
        for i, vehicule in enumerate(files_voitures_y):
            voiture_devant = None
            if i > 0 and files_voitures_y[i - 1].sens_circulation == vehicule.sens_circulation:
                voiture_devant = files_voitures_y[i - 1]

            if vehicule.en_virage:
                vehicule.tourner(vehicule.type_virage_courant, dt)
                if not vehicule.en_virage:
                    vehicule.realigner_apres_virage()
                    vehicule.sens_circulation = 1 if math.cos(vehicule.orientation) > 0 else -1
                    a_transferer_vers_x.append(vehicule)

            elif getattr(vehicule, "intention_virage", None) is not None and -1.0 <= vehicule.positionY <= 1.0:
                dir_init = "+Y" if vehicule.sens_circulation == 1 else "-Y"
                vehicule.initialiser_virage(dir_init, vehicule.intention_virage)
                vehicule.intention_virage = None

            else:
                vehicule.gerer_priorite_feu_et_file(
                    feu=feu_axe_y,
                    position_ligne_arret=0.0,
                    voiture_devant=voiture_devant,
                    distance_securite=5.0,
                    axe="y",
                    dt=dt
                )

        # F. Transfert effectif des véhicules entre les files (suite aux virages)
        for v in a_transferer_vers_y:
            files_voitures_x.remove(v)
            files_voitures_y.append(v)

        for v in a_transferer_vers_x:
            files_voitures_y.remove(v)
            files_voitures_x.append(v)

        # G. Affichage console de l'état de la simulation (toutes les secondes / 10 pas)
        if pas % 10 == 0:
            print(f"[{temps_ecoule:.1f}s] Feu X : {feu_axe_x.etat} | Feu Y : {feu_axe_y.etat}")
            print(f"  Pompier (X)   : pos = {pompier_x.positionX:.1f}, v = {pompier_x.vitesse:.1f} km/h")
            print(f"  Ambulance (Y) : pos = {ambulance_y.positionY:.1f}, v = {ambulance_y.vitesse:.1f} km/h")

        if db is not None and pas % 10 == 0:
            vitesse_moyenne, nb_vehicule = calculer_metriques(files_voitures_x + files_voitures_y, DISTANCE_FIN)
            db.enregistrer_metriques(vitesse_moyenne, nb_vehicule)
        # H. Conditions de fin de simulation
        tous_eloignes = all(
            abs(v.positionX) > DISTANCE_FIN or abs(v.positionY) > DISTANCE_FIN
            for v in files_voitures_x + files_voitures_y
        )

        if temps_ecoule >= TEMPS_MAX:
            print(f"\n=== Fin de la simulation (Temps maximum de {TEMPS_MAX}s atteint) ===")
            break

        if tous_eloignes:
            print(f"\n=== Fin de la simulation à {temps_ecoule:.1f}s (Tous les véhicules ont quitté la zone) ===")
            break

        # Pause pour synchroniser le pas de temps avec la simulation en temps réel
        time.sleep(dt)
