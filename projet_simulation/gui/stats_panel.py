from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGroupBox

class StatsPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)

        group = QGroupBox("Tableau de bord")
        group_layout = QVBoxLayout()

        self.lbl_urgences = QLabel("Passages prioritaires : 0")
        self.lbl_vitesse = QLabel("Vitesse moyenne : 0 km/h")

        self.lbl_urgences.setStyleSheet("font-size: 13px; font-weight: bold; color: #dcdcdc;")
        self.lbl_vitesse.setStyleSheet("font-size: 13px; font-weight: bold; color: #dcdcdc;")

        group_layout.addWidget(self.lbl_urgences)
        group_layout.addWidget(self.lbl_vitesse)
        group.setLayout(group_layout)

        layout.addWidget(group)
        layout.addStretch()

    def update_kpis(self, kpis):
        nb = kpis.get("nb_urgences", 0)
        vitesse = kpis.get("vitesse_moyenne", 0.0)
        self.lbl_urgences.setText(f"Passages prioritaires : {nb}")
        self.lbl_vitesse.setText(f"Vitesse moyenne : {vitesse} km/h")