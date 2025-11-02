-- Responsibility: Mertcan Kilinc

USE databeez_db;

DROP TABLE IF EXISTS Platform;
CREATE TABLE Platform (
    Platform_ID INT AUTO_INCREMENT PRIMARY KEY,
    Platform_Name VARCHAR(250),
    Manufacturer VARCHAR(250),
    Release_Year INT
);
