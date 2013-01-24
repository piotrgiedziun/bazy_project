BEGIN;
CREATE TABLE "mieszkaniec" (
    "id" integer NOT NULL PRIMARY KEY,
    "mieszkanie_id" integer NOT NULL UNIQUE,
    "user_id" integer NOT NULL UNIQUE REFERENCES "auth_user" ("id"),
    "imie" varchar(60) NOT NULL,
    "nazwisko" varchar(60) NOT NULL,
    "telefon" varchar(11) NOT NULL
)
;
CREATE TABLE "brama" (
    "id" integer NOT NULL PRIMARY KEY,
    "numer_bramy" varchar(45) NOT NULL,
    "ulica" varchar(45) NOT NULL,
    "miejscowosc" varchar(45) NOT NULL,
    "kod_pocztowy" varchar(45) NOT NULL,
    "saldo" real NOT NULL
)
;
CREATE TABLE "mieszkanie" (
    "id" integer NOT NULL PRIMARY KEY,
    "brama_id" integer NOT NULL REFERENCES "brama" ("id"),
    "numer_mieszkania" varchar(10) NOT NULL
)
;
CREATE TABLE "newsy_mieszkancy" (
    "id" integer NOT NULL PRIMARY KEY,
    "newsy_id" integer NOT NULL,
    "mieszkaniec_id" integer NOT NULL REFERENCES "mieszkaniec" ("id"),
    UNIQUE ("newsy_id", "mieszkaniec_id")
)
;
CREATE TABLE "newsy" (
    "id" integer NOT NULL PRIMARY KEY,
    "tytul" varchar(60) NOT NULL,
    "tresc" text NOT NULL,
    "data" datetime NOT NULL
)
;
CREATE TABLE "oplaty_type" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar(60) NOT NULL,
    "global_saldo" bool NOT NULL
)
;
CREATE TABLE "oplaty" (
    "id" integer NOT NULL PRIMARY KEY,
    "mieszkanie_id" integer NOT NULL REFERENCES "mieszkanie" ("id"),
    "oplaty_type_id" integer NOT NULL REFERENCES "oplaty_type" ("id"),
    "data_platnosci" date NOT NULL,
    "saldo" decimal NOT NULL
)
;
CREATE TABLE "wplaty" (
    "id" integer NOT NULL PRIMARY KEY,
    "oplaty_id" integer NOT NULL UNIQUE REFERENCES "oplaty" ("id"),
    "data_wplaty" date NOT NULL
)
;
COMMIT;
