CREATE DATABASE IF NOT EXISTS simu_db;
USE simu_db

CREATE USER IF NOT EXISTS 'simu_user'@'localhost' IDENTIFIED BY 'simu_password';
GRANT ALL PRIVILEGES ON simu_db.* TO 'simu_user'@'localhost';
FLUSH PRIVILEGES;


