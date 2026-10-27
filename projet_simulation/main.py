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
    parser = argparse.ArgumentParser(description="SAE 3.02 - Simulation de trafic distribuée")
    parser.add_argument("--role", choices=["server", "client"], required=True,
                        help="server sur la VM 1, client sur la VM 2")
    parser.add_argument("--host", default="127.0.0.1", help="IP de la VM 1 (côté client)")
    parser.add_argument("--port", type=int, default=5000)
    args = parser.parse_args()

    if args.role == "server":
        lancer_serveur(args.port)
    else:
        lancer_client(args.host, args.port)