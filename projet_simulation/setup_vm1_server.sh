#!/bin/bash
echo "Configuration de la VM 1 (Serveur & BDD)..."
sudo apt update
sudo apt install -y python3 python3-venv mariadb-server ufw

# Configuration Pare-feu
sudo ufw allow 5000/tcp
sudo ufw allow 3306/tcp
sudo ufw reload

# Configuration de la base de données
sudo systemctl start mariadb
sudo systemctl enable mariadb
sudo mariadb < database/schema.sql

# Mise en place de l'environnement Python
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

echo "VM 1 prête. Pour lancer le serveur :"
echo "source venv/bin/activate && python main.py --role server"