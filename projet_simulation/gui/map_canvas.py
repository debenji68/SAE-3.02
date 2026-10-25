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
        cx = self.width() // 2
        cy = self.height() // 2

        #Dessin des routes
        largeur_route = int(14 * e)
        painter.setPen(QPen(QColor("white"), largeur_route))
        painter.drawLine(0, cy, self.width(), cy)
        painter.drawLine(cx, 0, cx, self.height())

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
            est_urgence = v.get("est_urgence", False)
            if est_urgence:
                couleur = QColor("yellow")
            else:
                couleur = QColor("blue")
            painter.setBrush(QBrush(couleur))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRect(int(x) - 6, int(y) - 6, 12, 12)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MapCanvas()
    win.show()
    app.exec()