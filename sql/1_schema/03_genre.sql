-- Responsibility: Zeynep Nur Genel

USE databeez_db;

DROP TABLE IF EXISTS Genre;

CREATE TABLE Genre (
    Genre_ID INT AUTO_INCREMENT PRIMARY KEY,
    `Genre_Name` VARCHAR(100),
    `Description` VARCHAR(255),
    `Example_Game` VARCHAR(255),

);