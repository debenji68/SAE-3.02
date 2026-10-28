"""Serveur TCP de la simulation : aucun lancement lors de l'import."""

import json
import socket
import time


class ServeurSimulation:
    """Transmet les états de Simulation à une VM cliente à la fois."""

    def __init__(self, db, host="0.0.0.0", port=5000):
        self.db = db
        self.host = host
        self.port = port

    def demarrer(self):
        """Lance le serveur jusqu'à Ctrl+C ; attend un client pour avancer."""
        # Import différé : importer ce fichier ne charge pas le moteur.
        from ..simulation import Simulation

        sim = Simulation(self.db)

        try:
            # Le bloc with ferme automatiquement la socket à la sortie.
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serveur:
                serveur.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                serveur.bind((self.host, self.port))
                serveur.listen(1)

                print(f"Serveur en écoute sur {self.host}:{self.port}")

                # Après une déconnexion, on attend une nouvelle connexion
                # en conservant la même instance de Simulation.
                while True:
                    print("En attente d'un client...")
                    client, adresse = serveur.accept()

                    with client:
                        # Évite de rester bloqué indéfiniment sur un envoi.
                        client.settimeout(2.0)
                        print(f"Client connecté : {adresse}")

                        while True:
                            debut = time.monotonic()

                            # Le moteur calcule les véhicules, feux et KPI.
                            sim.step()
                            etat = sim.etat()

                            # Un JSON complet par ligne, encodé en UTF-8.
                            message = json.dumps(etat, ensure_ascii=False) + "\n"

                            try:
                                client.sendall(message.encode("utf-8"))
                            except OSError as erreur:
                                print(f"Connexion interrompue : {erreur}")
                                break

                            # Vise un envoi par pas de simulation en tenant
                            # compte du temps de calcul et de transmission.
                            duree = time.monotonic() - debut
                            time.sleep(max(0.0, sim.dt - duree))

        except KeyboardInterrupt:
            print("\nArrêt demandé.")
        finally:
            print("Serveur arrêté.")
