-- STEP 1: TABLE CREATION - Platform Table -- Zeynep Kocabıyık
USE databeez_db;

DROP TABLE IF EXISTS Platform;

CREATE TABLE Platform (
    Platform_ID INT AUTO_INCREMENT PRIMARY KEY,
    Platform_Name VARCHAR(100) NOT NULL UNIQUE, -- Her platform adı benzersiz olmalı
    Manufacturer VARCHAR(100),
    Release_Year INT
);