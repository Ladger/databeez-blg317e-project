-- STEP 1: TABLE CREATION - Platform Table -- Zeynep Kocabıyık
USE databeez_db;

DROP TABLE IF EXISTS Platform_raw;

CREATE TABLE Platform_raw (
    Platform_Name VARCHAR(100) NOT NULL UNIQUE, -- Her platform adı benzersiz olmalı
    Manufacturer VARCHAR(100),
    Release_Year INT
);