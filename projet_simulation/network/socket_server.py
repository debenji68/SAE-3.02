import socket
import json
import time

from projet_simulation.simulation import Simulation

HOST = "0.0.0.0"
PORT = 5000

# Plusieurs voitures avec un identifiant different pour chacune.
vehicules = [
    {"id": 1, "x": 100, "y": 200, "vitesse": 50},
    {"id": 2, "x": 250, "y": 150, "vitesse": 30},
    {"id": 3, "x": 50, "y": 300, "vitesse": 60}
]

# On garde la connexion de chaque client dans cette liste.
clients = []

serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serveur.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serveur.bind((HOST, PORT))
serveur.listen(5)
serveur.settimeout(0.2)

print("Serveur demarre sur le port", PORT)

dernier_envoi = time.monotonic()

try:
    while True:
        try:
            connexion, adresse = serveur.accept()
            connexion.settimeout(0.5)
            clients.append(connexion)
            print("Nouveau client :", adresse)
        except socket.timeout:
            pass

        if time.monotonic() - dernier_envoi >= 1:

            # Chaque voiture est envoyee a tous les clients connectes.
            for vehicule in vehicules:
                vehicule["x"] += 5
                message = (json.dumps(vehicule) + "\n").encode("utf-8")

                for client in clients[:]:
                    try:
                        client.sendall(message)
                    except OSError:
                        clients.remove(client)
                        client.close()
                        print("Un client s'est deconnecte")

            dernier_envoi = time.monotonic()

except KeyboardInterrupt:
    print("Arret du serveur")

finally:
    for client in clients:
        client.close()
    serveur.close()
