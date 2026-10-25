import argparse
import sys

def lancer_serveur(port):
    print("=== Démarrage du Serveur de Simulation ===")
    from projet_simulation.network.socket_server import ServeurSimulation
    from projet_simulation.database.stats_db import StatsDB
    db = StatsDB()
    ServeurSimulation(db, host="0.0.0.0", port=port).demarrer()


def lancer_client(host, port):
    print("=== Démarrage du Client / Affichage Graphique ===")
    from PyQt6.QtWidgets import QApplication
    from projet_simulation.gui.main_window import MainWindow
    from projet_simulation.network.socket_client import SocketClient

    app = QApplication(sys.argv)
    client = SocketClient(host, port)
    fenetre = MainWindow(socket_client=client)
    fenetre.show()
    client.start()
    sys.exit(app.exec())


if __name__ == "__main__":
    # Sélection interactive du rôle sans dépendance réseau ou système
    choix = input("Choisissez le rôle à exécuter (server/client) [client] : ").strip().lower()

    if choix == "server":
        lancer_serveur()
    else:
        lancer_client()
