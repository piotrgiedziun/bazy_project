BEGIN;
CREATE TABLE `mieszkaniec` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `mieszkanie_id` integer NOT NULL UNIQUE,
    `user_id` integer NOT NULL UNIQUE,
    `imie` varchar(60) NOT NULL,
    `nazwisko` varchar(60) NOT NULL,
    `telefon` varchar(11) NOT NULL
)
;
ALTER TABLE `mieszkaniec` ADD CONSTRAINT `user_id_refs_id_70ee26f4` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
CREATE TABLE `brama` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `numer_bramy` varchar(45) NOT NULL,
    `ulica` varchar(45) NOT NULL,
    `miejscowosc` varchar(45) NOT NULL,
    `kod_pocztowy` varchar(45) NOT NULL,
    `saldo` double precision NOT NULL
)
;
CREATE TABLE `mieszkanie` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `brama_id` integer NOT NULL,
    `numer_mieszkania` varchar(10) NOT NULL
)
;
ALTER TABLE `mieszkanie` ADD CONSTRAINT `brama_id_refs_id_1029f175` FOREIGN KEY (`brama_id`) REFERENCES `brama` (`id`);
ALTER TABLE `mieszkaniec` ADD CONSTRAINT `mieszkanie_id_refs_id_7e8c2d93` FOREIGN KEY (`mieszkanie_id`) REFERENCES `mieszkanie` (`id`);
CREATE TABLE `newsy_mieszkancy` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `newsy_id` integer NOT NULL,
    `mieszkaniec_id` integer NOT NULL,
    UNIQUE (`newsy_id`, `mieszkaniec_id`)
)
;
ALTER TABLE `newsy_mieszkancy` ADD CONSTRAINT `mieszkaniec_id_refs_id_6bc399d8` FOREIGN KEY (`mieszkaniec_id`) REFERENCES `mieszkaniec` (`id`);
CREATE TABLE `newsy` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `tytul` varchar(60) NOT NULL,
    `tresc` longtext NOT NULL,
    `data` datetime NOT NULL
)
;
ALTER TABLE `newsy_mieszkancy` ADD CONSTRAINT `newsy_id_refs_id_4ccb21b9` FOREIGN KEY (`newsy_id`) REFERENCES `newsy` (`id`);
CREATE TABLE `oplaty_type` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `name` varchar(60) NOT NULL,
    `global_saldo` bool NOT NULL
)
;
CREATE TABLE `oplaty` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `mieszkanie_id` integer NOT NULL,
    `oplaty_type_id` integer NOT NULL,
    `data_platnosci` date NOT NULL,
    `saldo` numeric(10, 2) NOT NULL
)
;
ALTER TABLE `oplaty` ADD CONSTRAINT `mieszkanie_id_refs_id_4fb56e6` FOREIGN KEY (`mieszkanie_id`) REFERENCES `mieszkanie` (`id`);
ALTER TABLE `oplaty` ADD CONSTRAINT `oplaty_type_id_refs_id_56b529c5` FOREIGN KEY (`oplaty_type_id`) REFERENCES `oplaty_type` (`id`);
CREATE TABLE `wplaty` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `oplaty_id` integer NOT NULL UNIQUE,
    `data_wplaty` date NOT NULL
)
;
ALTER TABLE `wplaty` ADD CONSTRAINT `oplaty_id_refs_id_6a90245d` FOREIGN KEY (`oplaty_id`) REFERENCES `oplaty` (`id`);
COMMIT;
