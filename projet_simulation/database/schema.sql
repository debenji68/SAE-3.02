CREATE DATABASE IF NOT EXISTS simu_db;
USE simu_db;

CREATE USER IF NOT EXISTS 'simu_user'@'localhost' IDENTIFIED BY 'simu_password';
GRANT ALL PRIVILEGES ON simu_db.* TO 'simu_user'@'localhost';
FLUSH PRIVILEGES;

CREATE TABLE IF NOT EXISTS evenement (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vehicule_id VARCHAR(50) NOT NULL,
    feu_id VARCHAR(50) NOT NULL,
    distance FLOAT NOT NULL
);


CREATE TABLE IF NOT EXISTS info_traffic (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vitesse_moyenne FLOAT NOT NULL,
    nb_vehicule INT NOT NULL
);
