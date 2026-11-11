import socket
import json
from PyQt6.QtCore import QThread, pyqtSignal


class SocketClient(QThread):
    """Thread qui se connecte au serveur et lit les états JSON ligne par ligne.

    Signaux:
        state_received (dict): un état complet de la simulation
        connection_changed (bool): True à la connexion, False à la déconnexion
        error_received (str): message d'erreur (réseau ou JSON invalide)
    """
    # Signaux Qt : le thread ne touche jamais l'interface directement
    state_received = pyqtSignal(dict)
    connection_changed = pyqtSignal(bool)
    error_received = pyqtSignal(str)

    DELAI_RECONNEXION_MS = 2000 # attente avant de retenter une connexion

    def __init__(self, host: str, port: int = 5000):
        """Prépare le client sans se connecter (la connexion se fait dans run).

        Args:
            host (str): adresse IP du serveur
            port (int): port du serveur
        """
        super().__init__()
        self.host = host
        self.port = port
        self.en_cours = True

    def stop(self):
        """Demande l'arrêt du thread et attend sa fin (3 s au maximum).""""""Demande l'arrêt du thread et attend sa fin (3 s au maximum)."""
        self.en_cours = False
        self.wait(3000)

    def run(self):
        """Boucle du thread : connexion, lecture des messages, reconnexion.

        Lancée par start(). Chaque ligne reçue est un état JSON complet,
        envoyé à l'interface par le signal state_received.
        """
        while self.en_cours:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                    # Timeout court pour vérifier en_cours régulièrement (arrêt rapide)
                    client.settimeout(0.5)
                    client.connect((self.host, self.port))

                    print("Connecte au serveur")
                    self.connection_changed.emit(True)

                    buffer = ""

                    while self.en_cours:
                        try:
                            data = client.recv(4096)
                        except socket.timeout:
                            continue

                        if not data:
                            # Le serveur a fermé la connexion
                            break

                        buffer += data.decode("utf-8")

                        while "\n" in buffer:
                            texte, buffer = buffer.split("\n", 1)

                            if texte.strip():
                                try:
                                    vehicule = json.loads(texte)
                                    if isinstance(vehicule, dict):
                                        self.state_received.emit(vehicule)
                                except json.JSONDecodeError:
                                    self.error_received.emit("JSON incorrect")

            except OSError as erreur:
                if self.en_cours:
                    self.error_received.emit(str(erreur))

            finally:
                self.connection_changed.emit(False)
                print("Connexion fermee")

            if self.en_cours:
                self.msleep(self.DELAI_RECONNEXION_MS)


if __name__ == "__main__":
    # Test du client sans interface : affiche les états reçus pendant 15 s
    import sys
    from PyQt6.QtCore import QCoreApplication, QTimer

    app = QCoreApplication(sys.argv)
    hote = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"

    client = SocketClient(hote)
    client.state_received.connect(lambda vehicule: print("Voiture recue :", vehicule))
    client.error_received.connect(lambda erreur: print("Erreur :", erreur))
    client.start()

    QTimer.singleShot(15000, app.quit)
    app.exec()
    client.stop()
