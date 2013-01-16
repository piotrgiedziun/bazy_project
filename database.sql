CREATE USER 'bazy_user'@'localhost' IDENTIFIED BY 'bazy_password';
CREATE DATABASE bazy_projekt;
GRANT SELECT,INSERT,UPDATE,DELETE ON bazy_projekt.* TO 'bazy_user'@'localhost';

USE bazy_projekt;
