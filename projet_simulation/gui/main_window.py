import sys
from PyQt6.QtWidgets import QMainWindow, QWidget, QApplication,QVBoxLayout,QTabWidget
from map_canvas import MapCanvas
from stats_panel import StatsPanel

class MainWindow(QMainWindow):
    def __init__(self, socket_client=None, db=None):
        super().__init__()
        self.setWindowTitle("Simulation de Trafic")
        self.resize(1024, 768)
        self.socket_client = socket_client
        self.db = db
        self.setStyleSheet("background-color: gray;")

        self.onglets = QTabWidget()
        self.setCentralWidget(self.onglets)


        # Onglet 1 : Canva
        self.page_canva = QWidget()
        self.layout_canva = QVBoxLayout(self.page_canva)
        self.canvas = MapCanvas()
        self.layout_canva.addWidget(self.canvas)
        self.onglets.addTab(self.page_canva, "Simulation")

        # Onglet 2 : Stat
        self.page_stat = QWidget()
        self.layout_stat = QVBoxLayout(self.page_stat)
        self.stats_panel = StatsPanel()
        self.layout_stat.addWidget(self.stats_panel)
        self.onglets.addTab(self.page_stat, "Statistique")

        # Lier le signal Sockets de Quentin s'il existe
        if self.socket_client and hasattr(self.socket_client, 'data_received'):
            self.socket_client.data_received.connect(self.donne_recu)

    def donne_recu(self, data):
        self.canvas.update_data(data)
        if self.db:
            kpis = self.db.lire_kpis()
            self.stats_panel.update_kpis(kpis)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    app.exec()