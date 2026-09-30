from datetime import datetime, timedelta

class feuDeCirculation:
    #déclaration des attributs privés ainsi que du constructeur
    def __init__(self,etat:str,duree_maintien_feu_vert:float=5.0,duree_maintien_feu_rouge:float=5.0):
        self.__etat = etat # l'etat du feu de circulation
        self.en_transition = False # permet de changer l'etat du feux de circulation si c'est false
        self.etat_cible = None # <-- Retient si on vise vert ou rouge
        self.heure_debut_transition = None
        # efface le chronomètre pour les calculs de durée  pour les changements d'état
        self.heure_dernier_changement = datetime.now()

        self.__duree_maintien_feu_vert = duree_maintien_feu_vert
        self.__duree_maintien_feu_rouge = duree_maintien_feu_rouge

    def __str__(self) -> str:
        return f" feuDeCirculation ({self.__etat}{self.__duree_maintien_feu_vert}{self.__duree_maintien_feu_rouge})"

    # déclaration des accesseurs pour les changements d'état du feu

    def get_etat(self):
        return self.__etat
    def set_etat(self,etat):
        self.__etat = etat
    etat = property(get_etat,set_etat)


    def passer_au_feu_vert(self):
    #Initie la transition du feu rouge au feu vert (par le feu orange)
        if self.etat == "rouge" and not self.en_transition:
            self.etat = "orange"
            self.etat_cible = "vert" # <-- On indique la cible
            self.en_transition = True
            self.heure_debut_transition = datetime.now()
            # calculer le temps d'attente du feu pour passer au feu vert dans la méthode mettre_au_feu_vert


    def mettre_au_feu_vert(self, delai_secondes: float = 2):
        # Met à jour le feu pour passer de l'orange au vert après le temps d'attente

        # vérifie que self.en_transition = True  et self.heure_debut_transition contient une date
        if self.en_transition and self.heure_debut_transition and self.etat_cible=="vert":
            temps_ecoule = datetime.now() - self.heure_debut_transition
            # calcul de la durée depuis que le feu est orange


            # permet de passer au feu vert si le temps écoulé est supérieur a 2 secondes
            if temps_ecoule >= timedelta(seconds=delai_secondes):
                self.etat = "vert"
                self.en_transition = False
                self.etat_cible = None
                self.heure_debut_transition = None
                self.heure_dernier_changement = datetime.now()
                # Recommence a compter le temps du feu vert

    def passer_au_feu_rouge(self):
        # Initie la transition du feu vert au feu rouge (par le feu orange)
        if self.etat == "vert" and not self.en_transition:
            self.etat = "orange"
            self.etat_cible = "rouge" # <-- On indique la cible
            self.en_transition = True
            self.heure_debut_transition = datetime.now()
            # calculer le temps d'attente du feu pour passer au feu rouge dans la méthode mettre_au_feu_rouge

    def mettre_au_feu_rouge(self, delai_secondes: float = 2):
        # Met à jour le feu pour passer de l'orange au vert après le temps d'attente

        # vérifie que self.en_transition = True  et self.heure_debut_transition contient une date
        if self.en_transition and self.heure_debut_transition and self.etat_cible=="rouge":
            temps_ecoule = datetime.now() - self.heure_debut_transition
            # calcul de la durée depuis que le feu est orange

            if temps_ecoule >= timedelta(seconds=delai_secondes):
            # permet de passer au feu vert si le temps écoulé est supérieur a 2 secondes
                self.etat = "rouge"
                self.en_transition = False
                self.etat_cible = None
                self.heure_debut_transition = None
                self.heure_dernier_changement = datetime.now()
            # Recommence a compter le temps en du feu rouge

    def verifier_changement_automatique(self, delai_orange: float= 2.0):
        if self.en_transition:
            self.mettre_au_feu_vert(delai_orange)
            self.mettre_au_feu_rouge(delai_orange)
            return

        temps_fixe = datetime.now() - self.heure_dernier_changement

        if self.__etat =="vert" and temps_fixe >= timedelta(seconds=self.__duree_maintien_feu_vert):
            self.passer_au_feu_rouge()

        elif self.__etat == "rouge" and temps_fixe >= timedelta(seconds=self.__duree_maintien_feu_rouge):
            self.passer_au_feu_vert()

if __name__ == "__main__":
    import time
    feuDeCirculation1 = feuDeCirculation("rouge")
    etat_actuel = feuDeCirculation1.etat
    print(f"état de départ : {feuDeCirculation1.etat}")

    #feuDeCirculation1.passer_au_feu_vert()
    #print(f"état pendant transition : {feuDeCirculation1.etat}")

    #print("Attente des 2 secondes d'orange...")
    for _ in range(500):
        feuDeCirculation1.verifier_changement_automatique()

        if feuDeCirculation1.etat != etat_actuel:
            #print(f"état après 2 secondes : {feuDeCirculation1.etat}")
            etat_actuel = feuDeCirculation1.etat
            print(f"Changement d'état -> {etat_actuel}")

        time.sleep(0.1)
