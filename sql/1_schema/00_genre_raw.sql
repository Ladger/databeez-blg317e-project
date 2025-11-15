-- TABLE CREATION - Genres Table -- Zeynep Nur Genel
USE databeez_db;

DROP TABLE IF EXISTS Genre_Raw;

CREATE TABLE Genre_Raw (
    Genre_Name VARCHAR(100) NOT NULL UNIQUE, -- Genre names are unique
    Description VARCHAR(255),
    Example_Game VARCHAR(255)
);