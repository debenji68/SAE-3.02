from datetime import datetime, timedelta


class feuDeCirculation:
    """Gère un feu de circulation avec gestion des transitions temporelles (Vert -> Orange -> Rouge)."""

    def __init__(self, etat: str, duree_maintien_feu_vert: float = 5.0, duree_maintien_feu_rouge: float = 5.0):
        # État courant du feu ('vert', 'orange', 'rouge')
        self.__etat = etat

        # Indicateur de transition : True si le feu est actuellement au feu orange
        self.en_transition = False

        # Couleur visée à la fin de la phase orange ('vert' ou 'rouge')
        self.etat_cible = None

        # Chronomètre enregistrant le début de la phase orange (réinitialisé hors transition)
        self.heure_debut_transition = None

        # Chronomètre enregistrant le moment du dernier passage au vert ou au rouge fixe
        self.heure_dernier_changement = datetime.now()

        # Durées d'affichage minimales des feux fixes (en secondes)
        self.__duree_maintien_feu_vert = duree_maintien_feu_vert
        self.__duree_maintien_feu_rouge = duree_maintien_feu_rouge

    def __str__(self) -> str:
        return f"feuDeCirculation(état={self.__etat}, vert={self.__duree_maintien_feu_vert}s, rouge={self.__duree_maintien_feu_rouge}s)"

    # --- Accesseurs ---

    def get_etat(self):
        return self.__etat

    def set_etat(self, etat):
        self.__etat = etat

    def get_duree_maintien_feu_vert(self):
        return self.__duree_maintien_feu_vert

    def set_duree_maintien_feu_vert(self, duree_maintien_feu_vert: float):
        self.__duree_maintien_feu_vert = duree_maintien_feu_vert

    def get_duree_maintien_feu_rouge(self):
        return self.__duree_maintien_feu_rouge

    def set_duree_maintien_feu_rouge(self, duree_maintien_feu_rouge: float):
        self.__duree_maintien_feu_rouge = duree_maintien_feu_rouge

    # Définition des propriétés
    etat = property(get_etat, set_etat)
    duree_maintien_feu_vert = property(fget=get_duree_maintien_feu_vert, fset=set_duree_maintien_feu_vert)
    duree_maintien_feu_rouge = property(fget=get_duree_maintien_feu_rouge, fset=set_duree_maintien_feu_rouge)

    # --- Gestion des transitions d'état ---

    def passer_au_feu_vert(self):
        """Initie la transition d'un feu rouge vers le feu vert (passage à l'orange)."""
        if self.etat == "rouge" and not self.en_transition:
            self.etat = "orange"
            self.etat_cible = "vert"
            self.en_transition = True
            self.heure_debut_transition = datetime.now()

    def mettre_au_feu_vert(self, delai_secondes: float = 2.0):
        """Finalise le passage au feu vert si le délai au feu orange est écoulé."""
        # Vérifie qu'une transition vers le vert est bien engagée
        if self.en_transition and self.heure_debut_transition and self.etat_cible == "vert":
            temps_ecoule = datetime.now() - self.heure_debut_transition

            # Si la durée minimale au feu orange est atteinte, on valide le feu vert
            if temps_ecoule >= timedelta(seconds=delai_secondes):
                self.etat = "vert"
                self.en_transition = False
                self.etat_cible = None
                self.heure_debut_transition = None
                self.heure_dernier_changement = datetime.now()  # Redémarre le chrono du feu vert fixe

    def passer_au_feu_rouge(self):
        """Initie la transition d'un feu vert vers le feu rouge (passage à l'orange)."""
        if self.etat == "vert" and not self.en_transition:
            self.etat = "orange"
            self.etat_cible = "rouge"
            self.en_transition = True
            self.heure_debut_transition = datetime.now()

    def mettre_au_feu_rouge(self, delai_secondes: float = 2.0):
        """Finalise le passage au feu rouge si le délai au feu orange est écoulé."""
        # Vérifie qu'une transition vers le rouge est bien engagée
        if self.en_transition and self.heure_debut_transition and self.etat_cible == "rouge":
            temps_ecoule = datetime.now() - self.heure_debut_transition

            # Si la durée minimale au feu orange est atteinte, on valide le feu rouge
            if temps_ecoule >= timedelta(seconds=delai_secondes):
                self.etat = "rouge"
                self.en_transition = False
                self.etat_cible = None
                self.heure_debut_transition = None
                self.heure_dernier_changement = datetime.now()  # Redémarre le chrono du feu rouge fixe

    def verifier_changement_automatique(self, delai_orange: float = 2.0):
        """Gère le cycle d'alternance automatique du feu à chaque pas de simulation."""
        # Phase 1 : Si une transition est déjà en cours (orange), on tente de finaliser l'état cible
        if self.en_transition:
            self.mettre_au_feu_vert(delai_orange)
            self.mettre_au_feu_rouge(delai_orange)
            return

        # Phase 2 : Si le feu est fixe (vert ou rouge), on vérifie si la durée de maintien est dépassée
        temps_maintien = datetime.now() - self.heure_dernier_changement

        if self.__etat == "vert" and temps_maintien >= timedelta(seconds=self.__duree_maintien_feu_vert):
            self.passer_au_feu_rouge()  # Le feu vert passe à l'orange (cible rouge)
        elif self.__etat == "rouge" and temps_maintien >= timedelta(seconds=self.__duree_maintien_feu_rouge):
            self.passer_au_feu_vert()  # Le feu rouge passe à l'orange (cible vert)


if __name__ == "__main__":
    import time

    # Script de test : vérification du cycle automatique des feux de circulation
    print("=== Test du cycle automatique d'un feu ===")

    # Initialisation du feu de circulation à l'état 'rouge'
    feuDeCirculation1 = feuDeCirculation("rouge")

    # Sauvegarde de l'état initial pour pouvoir détecter chaque changement de couleur
    etat_actuel = feuDeCirculation1.etat
    print(f"État de départ : {etat_actuel}\n")

    # Boucle de simulation : 500 itérations de 0,1s (durée totale : 50 secondes)
    for pas in range(500):
        # Mise à jour de l'état du feu à chaque pas de temps
        feuDeCirculation1.verifier_changement_automatique()

        # On n'affiche un message que si la couleur du feu a changé
        if feuDeCirculation1.etat != etat_actuel:
            etat_actuel = feuDeCirculation1.etat
            temps_ecoule = (pas + 1) * 0.1
            print(f"[{temps_ecoule:.1f}s] Changement d'état -> {etat_actuel}")

        # Pause de 0,1 seconde pour simuler le temps réel
        time.sleep(0.1)