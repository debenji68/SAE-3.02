import socket
import json

HOST = "127.0.0.1"
PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("Connexion au serveur...")

client.connect((HOST, PORT))

print("Connecté au serveur")

donnees = client.recv(1024)

message = donnees.decode()

print("Message reçu :", message)

vehicule = json.loads(message)

print("ID :", vehicule["id"])
print("Position X :", vehicule["x"])
print("Position Y :", vehicule["y"])
print("Vitesse :", vehicule["vitesse"])

client.close()

print("Connexion fermée")
