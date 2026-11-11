import sys
from PyQt6.QtWidgets import QMainWindow, QWidget, QApplication,QVBoxLayout,QTabWidget
from .map_canvas import MapCanvas
from .stats_panel import StatsPanel

class MainWindow(QMainWindow):
    """Fenêtre principale avec deux onglets : la carte et les statistiques."""
    def __init__(self, socket_client=None, db=None):
        """Construit les onglets et branche le client réseau.

        Args:
            socket_client (SocketClient): client TCP qui reçoit les états (None pour tester l'affichage seul)
            db (StatsDB): base de données
        """
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
        if self.socket_client:
            self.socket_client.state_received.connect(self.donne_recu)


    def donne_recu(self, data):
         """Met à jour la carte et le tableau de bord avec un nouvel état.

        Appelée par le signal state_received du client, environ 10 fois par seconde.

        Args:
            data (dict): état complet de la simulation reçu du serveur
        """
        self.canvas.update_data(data)
        self.stats_panel.update_kpis(data.get("kpis", {}), data.get("temps", 0))


    def closeEvent(self, event):
        """Arrête proprement le thread réseau quand on ferme la fenêtre.

        Args:
            event (QCloseEvent): événement de fermeture envoyé par Qt
        """
        if self.socket_client:
            self.socket_client.stop()
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    app.exec()
