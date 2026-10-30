import math
import time
from projet_simulation.database.stats_db import StatsDB
from projet_simulation.models import feuDeCirculation, vehicule_urgence, Voiture
from projet_simulation.utils.gps_utils import metres_vers_gps


def ligne_arret(sens):
    #les lignes d'arret sont a 10 m du centre : -10 si on arrive du cote negatif, +10 sinon
    return -10.0 * sens


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

def calculer_metriques(vehicules):
    #vitesse moyenne et nombre de vehicules encore dans la zone (100 m autour du carrefour)
    dans_zone = []
    for v in vehicules:
        if abs(v.positionX) <= 100 and abs(v.positionY) <= 100:
            dans_zone.append(v)

    if len(dans_zone) == 0:
        return 0.0, 0

    total = 0
    for v in dans_zone:
        total = total + v.vitesse
    return total / len(dans_zone), len(dans_zone)

class Simulation:
    def __init__(self, db):
        self.db = db
        self.dt = 0.1          #pas de temps (100 ms)
        self.temps_max = 60    #duree max d'un scenario en secondes
        self.pas = 0
        self.temps_ecoule = 0

        #Creation des feux
        self.feu_axe_x = feuDeCirculation("vert")
        self.feu_axe_y = feuDeCirculation("rouge")
        self.forcage_axe = None

        #Creation des vehicules d'urgence
        self.pompier_x = vehicule_urgence("Pompier1", -50.0, 0.0, 50.0, sens_circulation=1)
        self.ambulance_y = vehicule_urgence("Ambulance1", 0.0, -110.0, 50.0, sens_circulation=1)
        #Files de vehicules sur chaque axe
        self.files_voitures_x = [
            self.pompier_x,
            Voiture("V2", -65.0, 0.0, 50.0, sens_circulation=1),
            Voiture("V3", -80.0, 0.0, 50.0, sens_circulation=1),
            Voiture("V6", 65.0, 0.0, 50.0, sens_circulation=-1),
            Voiture("V7", 80.0, 0.0, 50.0, sens_circulation=-1),
        ]
        self.files_voitures_y = [
            self.ambulance_y,
            Voiture("V4", 0.0, -65.0, 50.0, sens_circulation=1),
            Voiture("V5", 0.0, -80.0, 50.0, sens_circulation=1),
            Voiture("V8", 0.0, 65.0, 50.0, sens_circulation=-1),
            Voiture("V9", 0.0, 80.0, 50.0, sens_circulation=-1),
        ]

        for v in self.tous_les_vehicules():
            v.en_virage = False
            v.intention_virage = None
            v.type_virage_courant = None

        #liste des vehicules d'urgence deja dans la zone
        self.urgences_dans_zone = []
        self.nouvelles_urgences = []

        #nombre de passages prioritaires
        self.nb_urgences = self.db.lire_kpis()["nb_urgences"]


    def tous_les_vehicules(self):
        return self.files_voitures_x + self.files_voitures_y


    def est_terminee(self):
        if self.temps_ecoule >= self.temps_max:
            return True
        #fini aussi si toutes les voitures sont sorties de la zone
        for v in self.tous_les_vehicules():
            if abs(v.positionX) <= 100 and abs(v.positionY) <= 100:
                return False
        return True


    def verifier_urgences(self, axe, file_voitures, feu_vert, feu_rouge):
        #regle des 50 m : le vehicule d'urgence met son feu au vert et l'autre au rouge
        for v in file_voitures:
            if not isinstance(v, vehicule_urgence) or v.en_virage:
                continue

            ligne = ligne_arret(v.sens_circulation)
            en_approche = v.est_dans_zone_detection(ligne, 50, axe)
            if axe == "x":
                pos = v.positionX
            else:
                pos = v.positionY
            dans_carrefour = abs(pos) <= 10

            if en_approche or dans_carrefour:
                self.nouvelles_urgences.append(v.identifiant)

                #on enregistre seulement quand il entre dans la zone
                if en_approche and v.identifiant not in self.urgences_dans_zone:
                    distance = v.distance_au_feu(ligne, axe)
                    self.nb_urgences = self.nb_urgences + 1
                    print(f"  >> Passage prioritaire : {v.identifiant} à {distance:.1f} m du feu")
                    self.db.enregistrer(v.identifiant, "feu_" + axe, distance)

                #si les 2 vehicules d'urgence arrivent en meme temps, le premier passe
                if self.forcage_axe is None:
                    feu_vert.forcer_etat("vert")
                    feu_rouge.forcer_etat("rouge")
                    self.forcage_axe = axe


    def avancer_file(self, file_voitures, feu, axe, a_transferer):
        for i in range(len(file_voitures)):
            vehicule = file_voitures[i]
            voiture_devant = None
            if i > 0 and file_voitures[i - 1].sens_circulation == vehicule.sens_circulation:
                voiture_devant = file_voitures[i - 1]

            if axe == "x":
                pos = vehicule.positionX
            else:
                pos = vehicule.positionY

            if vehicule.en_virage:
                #la voiture continue son virage
                vehicule.tourner(vehicule.type_virage_courant, self.dt)
                if not vehicule.en_virage:
                    #fin du virage : elle change d'axe
                    vehicule.realigner_apres_virage()
                    if axe == "x":
                        if math.sin(vehicule.orientation) > 0:
                            vehicule.sens_circulation = 1
                        else:
                            vehicule.sens_circulation = -1
                    else:
                        if math.cos(vehicule.orientation) > 0:
                            vehicule.sens_circulation = 1
                        else:
                            vehicule.sens_circulation = -1
                    a_transferer.append(vehicule)

            elif vehicule.intention_virage is not None and -1.0 <= pos <= 1.0:
                #la voiture arrive au centre et veut tourner
                if vehicule.sens_circulation == 1:
                    direction = "+" + axe.upper()
                else:
                    direction = "-" + axe.upper()
                vehicule.initialiser_virage(direction, vehicule.intention_virage)
                vehicule.intention_virage = None

            else:
                #ligne droite avec les feux et la distance de securite
                vehicule.gerer_priorite_feu_et_file(
                    feu=feu,
                    position_ligne_arret=ligne_arret(vehicule.sens_circulation),
                    voiture_devant=voiture_devant,
                    distance_securite=5.0,
                    axe=axe,
                    dt=self.dt,
                )


    def step(self):
        self.pas = self.pas + 1
        self.temps_ecoule = self.pas * self.dt

        #Tri des files
        self.files_voitures_x = trier_file_par_position(self.files_voitures_x, "x")
        self.files_voitures_y = trier_file_par_position(self.files_voitures_y, "y")

        #Cycle normal des feux
        self.feu_axe_x.verifier_changement_automatique()
        self.feu_axe_y.verifier_changement_automatique()

        #Priorite des vehicules d'urgence
        self.forcage_axe = None
        self.nouvelles_urgences = []
        self.verifier_urgences("x", self.files_voitures_x, self.feu_axe_x, self.feu_axe_y)
        self.verifier_urgences("y", self.files_voitures_y, self.feu_axe_y, self.feu_axe_x)
        self.urgences_dans_zone = self.nouvelles_urgences

        #Deplacement des vehicules
        vers_y = []
        vers_x = []
        self.avancer_file(self.files_voitures_x, self.feu_axe_x, "x", vers_y)
        self.avancer_file(self.files_voitures_y, self.feu_axe_y, "y", vers_x)

        #Les vehicules qui ont tourne changent de file
        for v in vers_y:
            self.files_voitures_x.remove(v)
            self.files_voitures_y.append(v)
        for v in vers_x:
            self.files_voitures_y.remove(v)
            self.files_voitures_x.append(v)

        #Enregistrement des metriques dans la bdd toutes les secondes (10 pas)
        if self.pas % 10 == 0:
            vitesse_moyenne, nb_vehicule = calculer_metriques(self.tous_les_vehicules())
            self.db.enregistrer_metriques(vitesse_moyenne, nb_vehicule)


    def vehicule_en_dict(self, v, axe):
        lat, lon = metres_vers_gps(v.positionX, v.positionY)
        return {
            "id": v.identifiant,
            "x": round(v.positionX, 2),
            "y": round(v.positionY, 2),
            "lat": round(lat, 7),
            "lon": round(lon, 7),
            "vitesse": round(v.vitesse, 1),
            "axe": axe,
            "sens": v.sens_circulation,
            "est_urgence": isinstance(v, vehicule_urgence),
        }


    def feu_en_dict(self, feu_id, feu, x, y, axe):
        lat, lon = metres_vers_gps(x, y)
        return {
            "id": feu_id,
            "x": x,
            "y": y,
            "lat": round(lat, 7),
            "lon": round(lon, 7),
            "etat": feu.etat,
            "force": self.forcage_axe == axe,
        }


    def etat(self):
        #dictionnaire envoye en JSON a la VM 2
        vehicules = []
        for v in self.files_voitures_x:
            vehicules.append(self.vehicule_en_dict(v, "x"))
        for v in self.files_voitures_y:
            vehicules.append(self.vehicule_en_dict(v, "y"))

        #un feu de chaque cote du carrefour
        feux = []
        feux.append(self.feu_en_dict("feu_x", self.feu_axe_x, -10.0, -10.0, "x"))
        feux.append(self.feu_en_dict("feu_x", self.feu_axe_x, 10.0, 10.0, "x"))
        feux.append(self.feu_en_dict("feu_y", self.feu_axe_y, 10.0, -10.0, "y"))
        feux.append(self.feu_en_dict("feu_y", self.feu_axe_y, -10.0, 10.0, "y"))

        vitesse_moyenne, nb_vehicule = calculer_metriques(self.tous_les_vehicules())
        return {
            "temps": round(self.temps_ecoule, 1),
            "vehicules": vehicules,
            "feux": feux,
            "kpis": {
                "vitesse_moyenne": round(vitesse_moyenne, 1),
                "nb_vehicule": nb_vehicule,
                "nb_urgences": self.nb_urgences,
            },
        }




if __name__ == "__main__":
    #test de la simulation seule, sans reseau (python3 -m projet_simulation.simulation)
    db = StatsDB()
    sim = Simulation(db)
    print("=== Démarrage de la simulation du carrefour ===")
    while not sim.est_terminee():
        sim.step()
        if sim.pas % 10 == 0:
            print(f"[{sim.temps_ecoule:.1f}s] Feu X : {sim.feu_axe_x.etat} | Feu Y : {sim.feu_axe_y.etat}")
            print(f"  Pompier (X)   : pos = {sim.pompier_x.positionX:.1f}, v = {sim.pompier_x.vitesse:.1f} km/h")
            print(f"  Ambulance (Y) : pos = {sim.ambulance_y.positionY:.1f}, v = {sim.ambulance_y.vitesse:.1f} km/h")
        time.sleep(sim.dt)
    print(f"\n=== Fin de la simulation à {sim.temps_ecoule:.1f}s ===")