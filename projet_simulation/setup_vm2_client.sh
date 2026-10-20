#!/bin/bash
echo "Configuration de la VM 2 (Client GUI)..."
sudo apt update
# python3-pyqt6 est installé via apt pour s'assurer d'avoir les dépendances système Qt
sudo apt install -y python3 python3-venv python3-pyqt6

# Mise en place de l'environnement Python
# L'option --system-site-packages permet d'accéder à PyQt6 installé globalement si besoin
python3 -m venv venv --system-site-packages
source venv/bin/activate
pip install -r requirements.txt

echo "VM 2 prête. Pour lancer le client :"
echo "source venv/bin/activate && python main.py --role client --ip <ADRESSE_IP_VM1>"