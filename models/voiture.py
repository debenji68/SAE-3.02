class Voiture :
    def __init__(self,identifiant:str,positionX:float,positionY:float, vitesse:int):
        self.__identifiant = identifiant
        self.__positionX = positionX
        self.__positionY = positionY
        self.__vitesse = vitesse

    def __str__(self) -> str:
        return f" Voiture : ({self.__identifiant} , {self.__positionX} , {self.__positionY} , {self.__vitesse})"

    def get_identifiant(self):
        return self.__identifiant
    def set_identifiant(self,identifiant):
        self.__identifiant = identifiant
    def get_positionX(self):
        return self.__positionX
    def set_positionX(self,positionX):
        self.__positionX = positionX
    def get_positionY(self):
        return self.__positionY
    def set_positionY(self,positionY):
        self.__positionY = positionY
    def get_vitesse(self):
        return self.__vitesse
    def set_vitesse(self,vitesse):
        self.__vitesse = vitesse

    identifiant = property(fget=get_identifiant,fset=set_identifiant)
    positionX = property(fget=get_positionX,fset=set_positionX)
    positionY = property(fget=get_positionY,fset=set_positionY)
    vitesse = property(fget=get_vitesse,fset=set_vitesse)


if __name__ == "__main__":
