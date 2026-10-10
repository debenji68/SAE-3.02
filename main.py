def lancer_serveur():
    print("=== Démarrage du Serveur de Simulation ===")
    # Exemple d'import et de lancement du module serveur
    # from projet_simulation.network.server import Server
    # serveur = Server(host="127.0.0.1", port=5555)
    # serveur.demarrer()


def lancer_client():
    print("=== Démarrage du Client / Affichage Graphique ===")
    # Exemple d'import et de lancement de la boucle simulation/IHM
    # from projet_simulation.gui.window import FenetreSimulation
    # app = FenetreSimulation()
    # app.run()


if __name__ == "__main__":
    # Sélection interactive du rôle sans dépendance réseau ou système
    choix = input("Choisissez le rôle à exécuter (server/client) [client] : ").strip().lower()

    if choix == "server":
        lancer_serveur()
    else:
        lancer_client()