from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QColor, QBrush, QPen
from PyQt6.QtCore import Qt


class MapCanvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.data = {"vehicules": [], "feux": []}
        self.setStyleSheet("background-color: Black;")

    def update_data(self, data):
        self.data = data
        self.update()  # Redessine le composant (appelle paintEvent)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # 1. Dessin des routes
        painter.setPen(QPen(QColor(80, 80, 80), 40))
        painter.drawLine(0, self.height() // 2, self.width(), self.height() // 2)
        painter.drawLine(self.width() // 2, 0, self.width() // 2, self.height())

        # 2. Dessin des feux
        for feu in self.data.get("feux", []):
            x, y = feu.get("x", 0), feu.get("y", 0)
            etat = feu.get("couleur", "rouge")

            couleur = QColor(255, 50, 50) if etat == "rouge" else QColor(50, 255, 50)
            if etat == "orange":
                couleur = QColor(255, 165, 0)

            painter.setBrush(QBrush(couleur))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(int(x) - 8, int(y) - 8, 16, 16)

        # 3. Dessin des véhicules
        for v in self.data.get("vehicules", []):
            x, y = v.get("x", 0), v.get("y", 0)
            est_urgence = v.get("est_urgence", False)

            couleur = QColor(255, 0, 0) if est_urgence else QColor(0, 150, 255)
            painter.setBrush(QBrush(couleur))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRect(int(x) - 6, int(y) - 6, 12, 12)
