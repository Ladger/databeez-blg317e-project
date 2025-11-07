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

-- Since order is important for the tables with foreign keys, it should start with parents to dependents

-- a. PARENT TABLES (Tables without foreign keys)

DROP TABLE IF EXISTS Publisher;
CREATE TABLE Publisher (
    Publisher_ID INT AUTO_INCREMENT PRIMARY KEY,
    Publisher_Name VARCHAR(250),
    Country VARCHAR(100),
    Year_Established INT
);

DROP TABLE IF EXISTS Platform;
CREATE TABLE Platform (
    Platform_ID INT AUTO_INCREMENT PRIMARY KEY,
    Platform_Name VARCHAR(250),
    Manufacturer VARCHAR(250),
    Release_Year INT
);

DROP TABLE IF EXISTS Genre;
CREATE TABLE Genre (
    Genre_ID INT AUTO_INCREMENT PRIMARY KEY,
    `Genre_Name` VARCHAR(100),
    `Description` VARCHAR(255),
    `Example_Game` VARCHAR(255)
);


-- b. CHILD TABLES (Have foreign key of parent tables)

DROP TABLE IF EXISTS Game;
CREATE TABLE Game (
    Game_ID INT AUTO_INCREMENT PRIMARY KEY,
    `Name` VARCHAR(255),
    `Year` INT,
    `Rank` INT,

    Publisher_ID INT NOT NULL,
    Platform_ID INT NOT NULL,
    Genre_ID INT NOT NULL,

    FOREIGN KEY (Publisher_ID) REFERENCES Publisher(Publisher_ID),
    FOREIGN KEY (Platform_ID) REFERENCES Platform(Platform_ID),
    FOREIGN KEY (Genre_ID) REFERENCES Genre(Genre_ID)
);

DROP TABLE IF EXISTS Sales;
CREATE TABLE Sales (
    Sales_ID INT AUTO_INCREMENT PRIMARY KEY,  
    Game_ID INT NOT NULL,                  
    NA_Sales DECIMAL(5, 2),
    EU_Sales DECIMAL(5, 2),
    JP_Sales DECIMAL(5, 2),
    Other_Sales DECIMAL(5, 2),
    Global_Sales DECIMAL(5, 2),
    
    FOREIGN KEY (Game_ID) REFERENCES Game(Game_ID)
);

-- c. SUMMARY TABLES

DROP TABLE IF EXISTS Genre_Stats;
CREATE TABLE Genre_Stats (
    Genre_ID INT NOT NULL PRIMARY KEY,
    `Total_Games` INT,
    `Total_Global_Sales` INT,
    `Avg_Global_Sales` INT,
    Top_Game_ID INT NOT NULL,
    
    FOREIGN KEY (Genre_ID) REFERENCES Genre(Genre_ID),
    FOREIGN KEY (Top_Game_ID) REFERENCES Game(Game_ID)
);

DROP TABLE IF EXISTS Platform_Stats;
CREATE TABLE Platform_Stats(
    Platform_ID INT NOT NULL PRIMARY KEY,
    Total_Games INT,
    Total_Global_Sales DECIMAL(5, 2),
    Avg_Global_Sales DECIMAL(5, 2),
    Top_Game_ID INT NOT NULL,
    
    FOREIGN KEY (Platform_ID) REFERENCES Platform(Platform_ID),
    FOREIGN KEY (Top_Game_ID) REFERENCES Game(Game_ID)
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

-- Load Non-keys for Game Table

ALTER TABLE Game
MODIFY COLUMN Publisher_ID INT NULL,
MODIFY COLUMN Platform_ID  INT NULL,
MODIFY COLUMN Genre_ID     INT NULL;

-- If the entry is "N/A" we are returning NULL for that cell
INSERT INTO Game (`Name`, `Year`, `Rank`)
SELECT
    `Name`,
    CAST(NULLIF(`Year`, 'N/A') AS UNSIGNED),
    `Rank`
FROM
    vgsales_raw;

