CREATE USER 'bazy_user'@'localhost' IDENTIFIED BY 'bazy_password';
CREATE DATABASE bazy_projekt CHARACTER SET utf8; #thanks to giedek because of http://stackoverflow.com/questions/6681831/setting-django-mysql-site-to-use-utf-8
GRANT INDEX, ALTER,CREATE,SELECT,INSERT,UPDATE,DELETE ON bazy_projekt.* TO 'bazy_user'@'localhost';

USE bazy_projekt;
