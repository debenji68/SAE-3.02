import time
from datetime import datetime, timedelta
from .feu_carrefour import feuDeCirculation
from .voiture import Voiture


class vehicule_urgence(Voiture):
    """Représente un véhicule d'urgence (pompier, ambulance, etc.) héritant de la classe Voiture

    et capable de forcer les feux tricolores au vert lorsqu'il s'approche d'un carrefour.
    """

    def __init__(
            self,
            identifiant: str,
            positionX: float,
            positionY: float,
            vitesse: float,
            sens_circulation: int = 1,
    ):
        """Initialise le véhicule d'urgence en récupérant les attributs et méthodes

        de la classe parente Voiture grâce à super().
        """
        super().__init__(identifiant, positionX, positionY, vitesse, sens_circulation)

    def distance_au_feu(self, position_ligne_arret: float, axe: str = "x") -> float:
        """Distance (en m) qui reste à parcourir jusqu'à la ligne d'arrêt.

        Négative quand le véhicule a déjà franchi la ligne.
        """
        # Sélection de la position courante en fonction de l'axe de circulation (X ou Y)
        pos_actuelle = self.positionX if axe == "x" else self.positionY

        # Cas 1 : Circulation dans le sens positif (+1, ex: de gauche à droite ou du bas vers le haut)
        if self.sens_circulation == 1:
            return position_ligne_arret - pos_actuelle

        # Cas 2 : Circulation dans le sens négatif (-1, ex: de droite à gauche ou du haut vers le bas)
        return pos_actuelle - position_ligne_arret

    def est_dans_zone_detection(self, position_ligne_arret: float,
                                distance_detection: float = 50.0, axe: str = "x") -> bool:
        """Vrai si le véhicule est en amont de la ligne d'arrêt, à moins de distance_detection."""
        return 0 <= self.distance_au_feu(position_ligne_arret, axe) <= distance_detection

    def forcer_feu_vert_si_proche(
            self,
            feu: feuDeCirculation,
            position_ligne_arret: float,
            distance_detection: float = 50.0,
            axe: str = "x"
    ):
        """Force le feu tricolore au vert si le véhicule d'urgence entre dans la zone de détection.

        Fonctionne pour l'axe X ou Y selon le paramètre 'axe' choisi.
        """
        if self.est_dans_zone_detection(position_ligne_arret, distance_detection, axe):
            # forcer_etat annule l'orange en cours : sinon le feu repasse au rouge juste après
            feu.forcer_etat("vert")


if __name__ == "__main__":
    print("=== Démarrage des tests : Véhicules d'urgence ===")

    # =========================================================================
    # --- 1. SIMULATION AXE X AVEC VÉHICULE D'URGENCE (Sens +1) ---
    # =========================================================================
    feu_x = feuDeCirculation("rouge")
    position_feu_x = 30.0

    # Le pompier démarre en x = -50.0 et se dirige vers la ligne d'arrêt située en x = 30.0
    pompier_x = vehicule_urgence("Pompier1", -50.0, 0.0, 50.0, sens_circulation=1)

    # File de véhicules circulant sur l'axe X derrière le véhicule d'urgence
    files_voitures_x = [
        pompier_x,
        Voiture("V2", -65.0, 0.0, 50.0, sens_circulation=1),
        Voiture("V3", -80.0, 0.0, 50.0, sens_circulation=1),
    ]

    print(f"\n--- 1. Simulation Axe X (Sens +1, Feu en x = {position_feu_x}) ---")

    # Boucle de simulation sur l'axe X (200 pas de 0.1s = 20 secondes)
    for i in range(200):
        # 1. Gestion automatique classique du cycle du feu (rouge/orange/vert)
        feu_x.verifier_changement_automatique()

        # 2. Le véhicule d'urgence vérifie s'il doit forcer le feu au vert
        pompier_x.forcer_feu_vert_si_proche(
            feu=feu_x,
            position_ligne_arret=position_feu_x,
            distance_detection=25.0,
            axe="x"
        )

        # 3. Calcul des déplacements et application des distances de sécurité
        for index, v in enumerate(files_voitures_x):
            v_devant = files_voitures_x[index - 1] if index > 0 else None
            v.gerer_priorite_feu_et_file(
                feu_x,
                position_ligne_arret=position_feu_x,
                voiture_devant=v_devant,
                distance_securite=5.0,
                axe="x",
                dt=0.1
            )

        # Affichage console régulier (toutes les secondes, soit tous les 10 pas)
        if i % 10 == 0:
            print(f"\n[Temps {i * 0.1:.1f}s] - État du Feu X : {feu_x.etat}")
            for v in files_voitures_x:
                print(f"  {v}")
        time.sleep(0.05)

    # =========================================================================
    # --- 2. SIMULATION AXE Y AVEC VÉHICULE D'URGENCE (Sens -1) ---
    # =========================================================================
    feu_y = feuDeCirculation("rouge")
    position_feu_y = 30.0

    # Le SAMU descend (sens -1) en partant de y = 110.0 vers la ligne d'arrêt en y = 30.0
    samu_y = vehicule_urgence("SAMU1", 0.0, 110.0, 50.0, sens_circulation=-1)

    # File de véhicules circulant sur l'axe Y derrière le véhicule d'urgence
    files_voitures_y = [
        samu_y,
        Voiture("V2", 0.0, 125.0, 50.0, sens_circulation=-1),
        Voiture("V3", 0.0, 140.0, 50.0, sens_circulation=-1),
    ]

    print(f"\n--- 2. Simulation Axe Y (Sens -1, Feu en y = {position_feu_y}) ---")

    # Boucle de simulation sur l'axe Y (200 pas de 0.1s = 20 secondes)
    for i in range(200):
        # 1. Gestion automatique classique du cycle du feu
        feu_y.verifier_changement_automatique()

        # 2. Le SAMU vérifie s'il doit forcer le feu au vert sur l'axe Y
        samu_y.forcer_feu_vert_si_proche(
            feu=feu_y,
            position_ligne_arret=position_feu_y,
            distance_detection=25.0,
            axe="y"
        )

        # 3. Calcul des déplacements et application des distances de sécurité
        for index, v in enumerate(files_voitures_y):
            v_devant = files_voitures_y[index - 1] if index > 0 else None
            v.gerer_priorite_feu_et_file(
                feu_y,
                position_ligne_arret=position_feu_y,
                voiture_devant=v_devant,
                distance_securite=5.0,
                axe="y",
                dt=0.1
            )

        # Affichage console régulier (toutes les secondes)
        if i % 10 == 0:
            print(f"\n[Temps {i * 0.1:.1f}s] - État du Feu Y : {feu_y.etat}")
            for v in files_voitures_y:
                print(f"  {v}")
        time.sleep(0.05)