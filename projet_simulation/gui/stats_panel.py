from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGroupBox, QApplication
import sys


class StatsPanel(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        group = QGroupBox("Tableau de bord")
        group_layout = QVBoxLayout()

        self.label_urgences = QLabel("Passages prioritaires : 0")
        self.label_vitesse = QLabel("Vitesse moyenne : 0 km/h")

        self.label_urgences.setStyleSheet("font-weight: bold; color: white;")
        self.label_vitesse.setStyleSheet("font-weight: bold; color: white;")

        group_layout.addWidget(self.label_urgences)
        group_layout.addWidget(self.label_vitesse)
        group.setLayout(group_layout)

        layout.addWidget(group)
        layout.addStretch()

    def update_kpis(self, kpis):
        nb = kpis.get("nb_urgences", 0)
        vitesse = kpis.get("vitesse_moyenne", 0.0)
        self.label_urgences.setText(f"Passages prioritaires : {nb}")
        self.label_vitesse.setText(f"Vitesse moyenne : {vitesse} km/h")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = StatsPanel()
    win.show()
    app.exec()