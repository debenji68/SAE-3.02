import mysql.connector

class StatsDB:
    def __init__(self, host="localhost", user="simu_user", password="simu_password", database="simu_db"):
        self.config = {"host": host, "user": user, "password": password, "database": database
        }

    def get_connection(self):
        return mysql.connector.connect(self.config)


    def enregistrer(self,vehicule_id, feu_id, distance):
        query = "INSERT INTO uregnce(vehicule_id, feu_id, distance) VALUES (%s, %s, %s)"
        values = (vehicule_id, feu_id, distance)
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(query, values)
        conne   ction.commit()
        cursor.close()
        connection.close()


    def lire_kpis(self):
        query_urgences = "SELECT COUNT(*) FROM evenements_urgence"
        query_vitesse = "SELECT AVG(vitesse_moyenne) FROM metriques_trafic"


