import socket
import json
from PyQt6.QtCore import QThread, pyqtSignal

class SocketClient(QThread):
    state_received = pyqtSignal(dict)
    connection_changed = pyqtSignal(bool)
    error_received = pyqtSignal(str)

    def __init__(self, host: str, port: int = 5000):
        super().__init__()
        self.host = host
        self.port = port
        self.socket = None

    def run(self):
         class SocketClient(QThread):
            message_recu = pyqtSignal(dict)
            def __init__(self, host, port=5000):
                super().__init__()
                self.host = host
                self.port = port

            def run(self):
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # création du socket TCP
                try:
                    client.connect((self.host, self.port))   # connexion au serveur

                    print("Connecté au serveur")

                    while True:

                        data = client.recv(4096)  # création du socket TCP

                        if not data:
                            break
                        texte = data.decode("utf-8")  # bytes -> texte
                        message = json.loads(texte)  # texte JSON -> dictionnaire Python

                        print("Message reçu :", message)
                        self.message_recu.emit(message)   # envoie le message à l'interface

                except ConnectionRefusedError:
                    print("Impossible de se connecter au serveur")

                except json.JSONDecodeError:
                    print("Erreur dans le JSON reçu")

                except Exception as erreur:
                    print("Erreur :", erreur)
                client.close() # fermeture de la connexion

                print("Connexion fermée")
