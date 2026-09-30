import sys
from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QApplication
from .map_canvas import MapCanvas
from .stats_panel import StatsPanel

class MainWindow(QMainWindow):
    def __init__(self, socket_client=None, db=None):
        super().__init__()
        self.setWindowTitle("Simulation de Trafic")
        self.resize(1024, 768)
        self.socket_client = socket_client
        self.db = db

        # Layout central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # IHM
        self.canvas = MapCanvas()
        self.stats_panel = StatsPanel()

        #widget
        main_layout.addWidget(self.canvas, stretch=3)
        main_layout.addWidget(self.stats_panel, stretch=1)


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
    win = MapCanvas()
    win.show()
    app.exec()