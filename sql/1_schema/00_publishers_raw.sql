-- Responsibility: Mertcan Kilinc

USE databeez_db;

DROP TABLE IF EXISTS Publishers_raw;
CREATE TABLE Publishers_raw (
    Publisher_ID INT AUTO_INCREMENT PRIMARY KEY,
    Publisher_Name VARCHAR(250),
    Country VARCHAR(100),
    Year_Established INT
);
