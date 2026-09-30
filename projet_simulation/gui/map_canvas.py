import sys

from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtGui import QPainter, QColor, QBrush, QPen
from PyQt6.QtCore import Qt


class MapCanvas(QWidget):
    def __init__(self):
        super().__init__()
        self.data = {"vehicules": [], "feux": []}
        self.setStyleSheet("background-color: Black;")


    def update_data(self, data):
        self.data = data
        self.update()


    def paintEvent(self, event):
        painter = QPainter(self)

        #Dessin des routes
        painter.setPen(QPen(QColor("gray"), 80))
        painter.drawLine(0, self.height() // 2, self.width(), self.height() // 2)
        painter.drawLine(self.width() // 2, 0, self.width() // 2, self.height())

        #Dessin des feux (a modifier selon la class)
        for feu in self.data.get("feux", []):
            x, y = feu.get("x", 0), feu.get("y", 0)
            etat = feu.get("etat", "rouge")
            if etat == "rouge":
                couleur = QColor("red")
            elif etat == "vert":
                couleur = QColor("green")
            else:
                couleur = QColor("orange")

            painter.setBrush(QBrush(couleur))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(int(x) - 8, int(y) - 8, 16, 16)

        #Dessin des véhicules (a modifier selon la class)
        for v in self.data.get("vehicules", []):
            x, y = v.get("x", 0), v.get("y", 0)
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