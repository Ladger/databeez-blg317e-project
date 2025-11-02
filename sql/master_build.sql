-- ----------------------------------------------
--          STEP 0: DATABASE CREATION
-- ----------------------------------------------

DROP DATABASE IF EXISTS DatabeeZ_db;
CREATE DATABASE DatabeeZ_db;

USE DatabeeZ_db;

-- ----------------------------------------------
--          STEP 1: TABLE CREATION
-- ----------------------------------------------

DROP TABLE IF EXISTS vgsales_raw;
CREATE TABLE vgsales_raw (
    `Rank` INT,
    `Name` VARCHAR(255),
    `Platform` VARCHAR(100),
    `Year` VARCHAR(10),
    `Genre` VARCHAR(100),
    `Publisher` VARCHAR(100),
    `NA_Sales` DECIMAL(5, 2),
    `EU_Sales` DECIMAL(5, 2),
    `JP_Sales` DECIMAL(5, 2),
    `Other_Sales` DECIMAL(5, 2),
    `Global_Sales` DECIMAL(5, 2)
);

DROP TABLE IF EXISTS Game;
CREATE TABLE Game (
    Game_ID INT AUTO_INCREMENT PRIMARY KEY,
    `Name` VARCHAR(255),
    `Year` INT,
    `Rank` INT,

    Publisher_ID INT,
    Platform_ID INT,
    Genre_ID INT
);

DROP TABLE IF EXISTS Publisher;
CREATE TABLE Publisher (
    Publisher_ID INT AUTO_INCREMENT PRIMARY KEY,
    Publisher_Name VARCHAR(250),
    Country VARCHAR(100),
    Year_Established INT
);

CREATE TABLE Platform (
    Platform_ID INT AUTO_INCREMENT PRIMARY KEY,
    Platform_Name VARCHAR(250),
    Manufacturer VARCHAR(250),
    Release_Year INT
);

DROP TABLE IF EXISTS Platform_Stats;
CREATE TABLE Platform_Stats(
    Platform_ID INT AUTO_INCREMENT PRIMARY KEY,
    Total_Games INT,
    Total_Global_Sales DECIMAL(5, 2),
    Avg_Global_Sales DECIMAL(5, 2),
    
    Top_Game_ID INT
);










-- ----------------------------------------------
--          STEP 2: LOADING DATA
-- ----------------------------------------------

LOAD DATA LOCAL INFILE 'D:/databeez-blg317e-project/data/vgsales.csv' -- Kendi file locationızı girin 
INTO TABLE vgsales_raw
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;
