import math
from .feu_carrefour import feuDeCirculation


class Voiture:
    """Représente un véhicule doté d'un modèle physique, d'une gestion des distances

    de sécurité, du respect des feux tricolores et de capacités de virage.
    """

    def __init__(self, identifiant: str, positionX: float, positionY: float, vitesse: float, sens_circulation: int = 1):
        self.__identifiant = identifiant  # Identifiant unique du véhicule
        self.__positionX = positionX  # Position X (axe horizontal : gauche -> droite)
        self.__positionY = positionY  # Position Y (axe vertical : bas -> haut)
        self.__vitesse = vitesse  # Vitesse actuelle (en km/h)
        self.__sens_circulation = sens_circulation  # 1 (sens positif) ou -1 (sens inverse)

        self.__acceleration = 15.0  # Gain de vitesse (km/h par seconde)
        self.__deceleration = 20.0  # Perte de vitesse (km/h par seconde)
        self.__vitesse_nominale = vitesse  # Vitesse maximale autorisée pour ce véhicule

        # Position au pas de temps précédent
        self.positionX_prev = positionX
        self.positionY_prev = positionY

        # Attributs de gestion des virages
        self.en_virage = False  # Vrai si le véhicule est en train de tourner
        self.angle_parcouru = 0.0  # Angle déjà parcouru dans le virage en radians
        self.orientation = 0.0  # Cap actuel du véhicule (en radians)
        self.rayon_virage = 8.0  # Rayon de courbure du virage (en mètres)
        self.centre_virage = (0.0, 0.0)  # Coordonnées (Xc, Yc) du centre du cercle de virage
        self.type_virage_courant = None  # 'gauche' ou 'droite'

    def __str__(self) -> str:
        return f"Voiture(ID: {self.__identifiant}, X: {self.__positionX:.1f}, Y: {self.__positionY:.1f}, Vitesse: {self.__vitesse:.1f} km/h)"

    # --- Accesseurs et Propriétés ---

    def get_identifiant(self):
        return self.__identifiant

    def set_identifiant(self, val):
        self.__identifiant = val

    def get_positionX(self):
        return self.__positionX

    def set_positionX(self, val):
        self.__positionX = val

    def get_positionY(self):
        return self.__positionY

    def set_positionY(self, val):
        self.__positionY = val

    def get_vitesse(self):
        return self.__vitesse

    def set_vitesse(self, val):
        self.__vitesse = val

    def get_sens_circulation(self):
        return self.__sens_circulation

    def set_sens_circulation(self, val):
        self.__sens_circulation = val

    identifiant = property(fget=get_identifiant, fset=set_identifiant)
    positionX = property(fget=get_positionX, fset=set_positionX)
    positionY = property(fget=get_positionY, fset=set_positionY)
    vitesse = property(fget=get_vitesse, fset=set_vitesse)
    sens_circulation = property(fget=get_sens_circulation, fset=set_sens_circulation)

    # --- Dynamique de déplacement ---

    def avancer(self, dt: float = 0.1):
        """Avance le véhicule en ligne droite selon son orientation actuelle."""
        if self.en_virage:
            return

        self.positionX_prev = self.positionX
        self.positionY_prev = self.positionY

        # Conversion km/h -> m/s, puis calcul de la distance parcourue pendant le pas de temps dt
        vitesse_ms = (self.vitesse * 1000) / 3600
        distance = vitesse_ms * dt

        # Mise à jour des coordonnées via la trigonométrie (cos/sin de l'orientation)
        self.positionX += distance * math.cos(self.orientation)
        self.positionY += distance * math.sin(self.orientation)

    def freiner(self):
        """Arrêt complet immédiat du véhicule."""
        self.__vitesse = 0.0

    def deceleration(self, dt: float = 0.1):
        """Réduit progressivement la vitesse du véhicule."""
        self.__vitesse = max(0.0, self.__vitesse - (self.__deceleration * dt))

    def acceleration(self, dt: float = 0.1):
        """Augmente progressivement la vitesse jusqu'à la vitesse nominale."""
        self.__vitesse = min(self.__vitesse_nominale, self.__vitesse + (self.__acceleration * dt))

    # --- Gestion des virages ---

    def initialiser_virage(self, direction_initiale: str, type_virage: str):
        """Calcule le centre du cercle de virage et initialise l'orientation de départ."""
        self.en_virage = True
        self.angle_parcouru = 0.0
        self.type_virage_courant = type_virage

        angles_init = {
            "+X": 0.0,
            "+Y": math.pi / 2,
            "-X": math.pi,
            "-Y": 3 * math.pi / 2
        }
        self.orientation = angles_init.get(direction_initiale, 0.0)

        # Calcul de la perpendiculaire pour situer le centre du cercle (gauche = +90°, droite = -90°)
        angle_centre = self.orientation + (math.pi / 2 if type_virage == "gauche" else -math.pi / 2)

        self.centre_virage = (
            self.positionX + self.rayon_virage * math.cos(angle_centre),
            self.positionY + self.rayon_virage * math.sin(angle_centre)
        )

    def tourner(self, type_virage: str, dt: float = 0.1):
        """Met à jour la position et l'orientation pas à pas le long de l'arc de cercle."""
        if not self.en_virage:
            return

        vitesse_ms = (self.vitesse * 1000) / 3600
        d_theta = (vitesse_ms * dt) / self.rayon_virage
        signe = 1.0 if type_virage == "gauche" else -1.0

        # Si on atteint ou dépasse un virage complet à 90 degrés (pi / 2)
        if self.angle_parcouru + d_theta >= math.pi / 2:
            d_theta_restant = (math.pi / 2) - self.angle_parcouru
            self.angle_parcouru = math.pi / 2
            self.orientation += signe * d_theta_restant
            self.en_virage = False
        else:
            self.angle_parcouru += d_theta
            self.orientation += signe * d_theta

        # Calcul de la nouvelle position sur le cercle par rapport au centre (Xc, Yc)
        Xc, Yc = self.centre_virage
        angle_depuis_centre = self.orientation - (math.pi / 2 if type_virage == "gauche" else -math.pi / 2)

        self.positionX = Xc + self.rayon_virage * math.cos(angle_depuis_centre)
        self.positionY = Yc + self.rayon_virage * math.sin(angle_depuis_centre)

    def realigner_apres_virage(self):
        """Ajuste parfaitement l'orientation et la position sur la grille en fin de virage."""
        quadrant = round(self.orientation / (math.pi / 2)) % 4
        self.orientation = quadrant * (math.pi / 2)

        Xc, Yc = self.centre_virage
        R = self.rayon_virage

        signe = 1.0 if self.type_virage_courant == "gauche" else -1.0
        angle_depuis_centre = self.orientation - (signe * math.pi / 2)

        self.positionX = Xc + R * math.cos(angle_depuis_centre)
        self.positionY = Yc + R * math.sin(angle_depuis_centre)
        self.type_virage_courant = None

    # --- Gestion des priorités et files d'attente ---

    def gerer_priorite_feu_et_file(
            self,
            feu,
            position_ligne_arret: float,
            voiture_devant=None,
            distance_securite: float = 5.0,
            axe: str = "x",
            dt: float = 0.1
    ):
        """Vérifie les feux et la distance avec le véhicule précédent pour ajuster la vitesse."""
        pos_actuelle = self.positionX if axe == "x" else self.positionY

        # 1. Calcul de la position limite à ne pas dépasser
        if self.__sens_circulation == 1:
            pos_limite = float("inf")
            if voiture_devant is not None:
                pos_devant = voiture_devant.positionX if axe == "x" else voiture_devant.positionY
                pos_limite = min(pos_limite, pos_devant - distance_securite)

            if feu.etat in ["rouge", "orange"] and pos_actuelle <= position_ligne_arret:
                pos_limite = min(pos_limite, position_ligne_arret)
        else:
            pos_limite = float("-inf")
            if voiture_devant is not None:
                pos_devant = voiture_devant.positionX if axe == "x" else voiture_devant.positionY
                pos_limite = max(pos_limite, pos_devant + distance_securite)

            if feu.etat in ["rouge", "orange"] and pos_actuelle >= position_ligne_arret:
                pos_limite = max(pos_limite, position_ligne_arret)

        # 2. Estimation de la distance de freinage nécessaire
        vitesse_m_s = self.__vitesse / 3.6
        decel_m_s2 = self.__deceleration / 3.6
        dist_freinage = (vitesse_m_s ** 2) / (2 * decel_m_s2) if decel_m_s2 > 0 else 0.0

        # 3. Prise de décision (freiner, décélérer ou accélérer)
        if self.__sens_circulation == 1:
            dist_obstacle = pos_limite - pos_actuelle
            if dist_obstacle <= 0.05:
                self.freiner()
            elif dist_obstacle <= dist_freinage + (vitesse_m_s * dt):
                self.deceleration(dt)
            else:
                self.acceleration(dt)
        else:
            dist_obstacle = pos_actuelle - pos_limite
            if dist_obstacle <= 0.05:
                self.freiner()
            elif dist_obstacle <= dist_freinage + (vitesse_m_s * dt):
                self.deceleration(dt)
            else:
                self.acceleration(dt)

        # 4. Calcul du déplacement effectif
        vitesse_effective_m_s = self.__vitesse / 3.6
        deplacement = vitesse_effective_m_s * dt * self.__sens_circulation

        if self.__sens_circulation == 1:
            nouvelle_pos = min(pos_actuelle + deplacement, pos_limite)
        else:
            nouvelle_pos = max(pos_actuelle + deplacement, pos_limite)

        # 5. Application de la nouvelle position sur l'axe concerné
        if axe == "x":
            self.positionX = nouvelle_pos
        else:
            self.positionY = nouvelle_pos

    def detecter_sens_circulation(self) -> str:
        """Détermine le sens de déplacement principal (+X, -X, +Y, -Y)."""
        dx = self.positionX - self.positionX_prev
        dy = self.positionY - self.positionY_prev

        if abs(dx) >= abs(dy):
            return "+X" if dx >= 0 else "-X"
        else:
            return "+Y" if dy >= 0 else "-Y"


def tester_tous_les_virages():
    print("=" * 60)
    print("TEST DE TOUTES LES COMBINAISONS DE VIRAGES (4 Directions x 2 Côtés)")
    print("=" * 60)

    rayon = 8.0
    dt = 0.1

    cas_de_test = [
        ("+X", "gauche", (0.0, 0.0), (rayon, rayon), 90.0),
        ("+X", "droite", (0.0, 0.0), (rayon, -rayon), 270.0),
        ("+Y", "gauche", (0.0, 0.0), (-rayon, rayon), 180.0),
        ("+Y", "droite", (0.0, 0.0), (rayon, rayon), 0.0),
        ("-X", "gauche", (0.0, 0.0), (-rayon, -rayon), 270.0),
        ("-X", "droite", (0.0, 0.0), (-rayon, rayon), 90.0),
        ("-Y", "gauche", (0.0, 0.0), (rayon, -rayon), 0.0),
        ("-Y", "droite", (0.0, 0.0), (-rayon, -rayon), 180.0),
    ]

    succes_total = True

    for dir_init, type_v, (x0, y0), (x_attendu, y_attendu), angle_attendu in cas_de_test:
        v = Voiture("Test", x0, y0, 30.0)
        v.rayon_virage = rayon
        v.initialiser_virage(dir_init, type_v)

        while v.en_virage:
            v.tourner(type_v, dt)

        v.realigner_apres_virage()

        angle_final_deg = math.degrees(v.orientation) % 360
        angle_attendu_norm = angle_attendu % 360

        erreur_x = abs(v.positionX - x_attendu)
        erreur_y = abs(v.positionY - y_attendu)
        erreur_angle = abs(angle_final_deg - angle_attendu_norm)

        ok = erreur_x < 0.1 and erreur_y < 0.1 and erreur_angle < 0.1
        if not ok:
            succes_total = False

        status = "OK" if ok else "ÉCHEC"
        print(f"[{status}] {dir_init} -> {type_v:<6} | Pos finale : ({v.positionX:5.1f}, {v.positionY:5.1f}) [Attendu : ({x_attendu:5.1f}, {y_attendu:5.1f})] | Cap : {angle_final_deg:5.0f}°")

    print("-" * 60)
    if succes_total:
        print("RÉSULTAT : Les 8 combinaisons de virage fonctionnent parfaitement !")
    else:
        print("RÉSULTAT : Des erreurs ont été détectées sur certains virages.")
    print("=" * 60)


if __name__ == "__main__":
    tester_tous_les_virages()