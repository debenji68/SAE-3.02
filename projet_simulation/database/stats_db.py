import mysql.connector

class StatsDB:
    def __init__(self, host="localhost", user="simu_user", password="simu_password", database="simu_db"):
        self.config = {"host": host, "user": user, "password": password, "database": database}


    def get_connection(self):
        return mysql.connector.connect(**self.config)


    def enregistrer(self,vehicule_id, feu_id, distance):
        query = "INSERT INTO evenement(vehicule_id, feu_id, distance) VALUES (%s, %s, %s)"
        values = (vehicule_id, feu_id, distance)
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(query, values)
        connection.commit()
        cursor.close()
        connection.close()

    def enregistrer_metriques(self, vitesse_moyenne, nb_vehicule):
        query = "INSERT INTO info_traffic(vitesse_moyenne, nb_vehicule) VALUES (%s, %s)"
        values = (float(vitesse_moyenne), int(nb_vehicule))
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(query, values)
        connection.commit()
        cursor.close()
        connection.close()


    def lire_kpis(self):
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


