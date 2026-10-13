import mysql.connector

class StatsDB:
    def __init__(self, host="localhost", user="simu_user", password="simu_password", database="simu_db"):
        self.config = {"host": host, "user": user, "password": password, "database": database
        }

    def get_connection(self):
        return mysql.connector.connect(self.config)


