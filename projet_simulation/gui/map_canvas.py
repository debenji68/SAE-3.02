import sys
from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtGui import QPainter, QColor, QBrush, QPen
from PyQt6.QtCore import Qt
from projet_simulation.utils.gps_utils import gps_vers_pixels, metres_vers_gps

class MapCanvas(QWidget):
    def __init__(self):
        super().__init__()
        self.data = {"vehicules": [], "feux": []}
        self.etendue = 110   #nombre de metres entre le centre et le bord de la carte
        self.setMinimumSize(400, 400)


    def update_data(self, data):
        self.data = data
        self.update()


    def echelle(self):
        return min(self.width(), self.height()) / (2 * self.etendue)


    def gps_vers_ecran(self, lat, lon):
        px, py = gps_vers_pixels(lat, lon, self.width(), self.height(), self.etendue)
        return int(px), int(py)


    def paintEvent(self, event):
        painter = QPainter(self)
        e = self.echelle()
        coordonne_x = self.width() // 2
        coordonne_y = self.height() // 2

        #Dessin des routes
        largeur_route = int(14 * e)
        painter.setPen(QPen(QColor("white"), largeur_route))
        painter.drawLine(0, coordonne_y, self.width(), coordonne_y)
        painter.drawLine(coordonne_x, 0, coordonne_x, self.height())

        #Dessin des feux (a modifier selon la class)
        for feu in self.data.get("feux", []):
            x, y = self.gps_vers_ecran(feu.get("lat", 0), feu.get("lon", 0))
            etat = feu.get("etat", "rouge")
            if etat == "rouge":
                couleur = QColor("red")
            elif etat == "vert":
                couleur = QColor("green")
            else:
                couleur = QColor("orange")

            painter.setBrush(QBrush(couleur))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(x - 8, y - 8, 16, 16)

        #Dessin des véhicules
        taille = max(8, int(4 * e))
        decalage = int(3.5 * e)  # pour mettre la voiture sur sa voie et pas au milieu de la route
        for v in self.data.get("vehicules", []):
            x, y = self.gps_vers_ecran(v.get("lat", 0), v.get("lon", 0))
            sens = v.get("sens", 1)
            if v.get("axe") == "x":
                y = y + sens * decalage
            else:
                x = x + sens * decalage
            est_urgence = v.get("est_urgence", False)
            if est_urgence:
                couleur = QColor("yellow")
            else:
                couleur = QColor("blue")
            painter.setBrush(QBrush(couleur))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRect(x - taille // 2, y - taille // 2, taille, taille)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MapCanvas()
    win.show()
    app.exec()