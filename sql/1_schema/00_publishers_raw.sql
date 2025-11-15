-- Responsibility: Mertcan Kilinc

USE databeez_db;

DROP TABLE IF EXISTS Publisher_raw;
CREATE TABLE Publisher_raw (
    Publisher_Name VARCHAR(250),
    Country VARCHAR(100),
    Year_Established INT
);
