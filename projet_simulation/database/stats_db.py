import mysql.connector

class StatsDB:
    """Gère la connexion à la base MariaDB et les requêtes SQL du projet."""
    def __init__(self, host="localhost", user="simu_user", password="simu_password", database="simu_db"):
        """Garde les paramètres de connexion à la base.

        Args:
            host (str): adresse du serveur MariaDB
            user (str): utilisateur MariaDB
            password (str): mot de passe de l'utilisateur
            database (str): nom de la base
        """
        self.config = {"host": host, "user": user, "password": password, "database": database}


    def get_connection(self):
        """Ouvre une nouvelle connexion à la base.

        Returns:
            MySQLConnection: connexion à fermer après usage
        """
        return mysql.connector.connect(**self.config)


    def enregistrer(self,vehicule_id, feu_id, distance):
        """Enregistre un passage prioritaire dans la table evenement.

        Args:
            vehicule_id (str): identifiant du véhicule d'urgence
            feu_id (str): feu forcé au vert
            distance (float): distance au feu au moment de la détection, en mètres
        """
        query = "INSERT INTO evenement(vehicule_id, feu_id, distance) VALUES (%s, %s, %s)"
        values = (vehicule_id, feu_id, distance)
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(query, values)
        connection.commit()
        cursor.close()
        connection.close()

    def enregistrer_metriques(self, vitesse_moyenne, nb_vehicule):
        """Enregistre la vitesse moyenne et le nombre de véhicules dans info_traffic.

        Args:
            vitesse_moyenne (float): vitesse moyenne des véhicules dans la zone, en km/h
            nb_vehicule (int): nombre de véhicules dans la zone
        """
        query = "INSERT INTO info_traffic(vitesse_moyenne, nb_vehicule) VALUES (%s, %s)"
        values = (float(vitesse_moyenne), int(nb_vehicule))
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(query, values)
        connection.commit()
        cursor.close()
        connection.close()


    def lire_kpis(self):
        """Lit les indicateurs du tableau de bord.

        Returns:
            dict: {"nb_urgences": int, "vitesse_moyenne": float}.
        """
        query_urgences = "SELECT COUNT(*) FROM evenement"
        query_vitesse = "SELECT COALESCE(AVG(vitesse_moyenne), 0) FROM info_traffic"
        kpis = {"nb_urgences": 0, "vitesse_moyenne": 0.0}
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(query_urgences)
        resultat_urg = cursor.fetchone()
        if resultat_urg is not None:
            kpis["nb_urgences"] = resultat_urg[0]
        cursor.execute(query_vitesse)
        resultat_vitesse = cursor.fetchone()
        if resultat_vitesse is not None:
            kpis["vitesse_moyenne"] = resultat_vitesse[0]
        cursor.close()
        connection.close()
        return kpis


