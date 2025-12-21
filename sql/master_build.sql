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

DROP TABLE IF EXISTS Platform_raw;
CREATE TABLE Platform_raw (
    Platform_Name VARCHAR(100) NOT NULL UNIQUE, -- Her platform adı benzersiz olmalı
    Manufacturer VARCHAR(100),
    Release_Year INT
);

DROP TABLE IF EXISTS Genre_Raw;
CREATE TABLE Genre_Raw (
    Genre_Name VARCHAR(100) NOT NULL UNIQUE, -- Genre names are unique
    `Description` VARCHAR(255),
    Example_Game VARCHAR(255)
);

DROP TABLE IF EXISTS Publisher_raw;
CREATE TABLE Publisher_raw (
    Publisher_Name VARCHAR(250),
    Country VARCHAR(100),
    Year_Established INT
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

    Publisher_ID INT NULL,
    Platform_ID INT NOT NULL,
    Genre_ID INT NOT NULL,

    -- PUBLISHER: Silinirse oyun kalsın ama yayıncı alanı boşalsın
    CONSTRAINT fk_game_publisher FOREIGN KEY (Publisher_ID) 
        REFERENCES Publisher(Publisher_ID) ON DELETE SET NULL ON UPDATE CASCADE,
    
    -- PLATFORM: Silinirse bağlı tüm oyunlar silinsin
    CONSTRAINT fk_game_platform FOREIGN KEY (Platform_ID) 
        REFERENCES Platform(Platform_ID) ON DELETE CASCADE ON UPDATE CASCADE,
    
    -- GENRE: Silinirse bağlı tüm oyunlar silinsin (Arayüzde uyarı vereceğiz)
    CONSTRAINT fk_game_genre FOREIGN KEY (Genre_ID) 
        REFERENCES Genre(Genre_ID) ON DELETE CASCADE ON UPDATE CASCADE
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
    
    CONSTRAINT fk_sales_game FOREIGN KEY (Game_ID) 
        REFERENCES Game(Game_ID) ON DELETE CASCADE
);
 
-- c. SUMMARY TABLES

DROP TABLE IF EXISTS Genre_Stats;
CREATE TABLE Genre_Stats (
    Genre_ID INT NOT NULL PRIMARY KEY,
    `Total_Games` INT,
    `Total_Global_Sales` DECIMAL(10, 2) DEFAULT 0.00,
    `Avg_Global_Sales` DECIMAL(10, 2) DEFAULT 0.00,
    Top_Game_ID INT,
    
    CONSTRAINT fk_genre_stats_id FOREIGN KEY (Genre_ID) 
        REFERENCES Genre(Genre_ID) ON DELETE CASCADE,
    CONSTRAINT fk_genre_stats_topgame FOREIGN KEY (Top_Game_ID) 
        REFERENCES Game(Game_ID) ON DELETE SET NULL
);

 

DROP TABLE IF EXISTS Platform_Stats;
CREATE TABLE Platform_Stats(
    Platform_ID INT NOT NULL PRIMARY KEY,
    Total_Games INT,
    Total_Global_Sales DECIMAL(10, 2) DEFAULT 0.00,
    Avg_Global_Sales DECIMAL(10, 2) DEFAULT 0.00,
    Top_Game_ID INT,
    
    CONSTRAINT fk_platform_stats_id FOREIGN KEY (Platform_ID) 
        REFERENCES Platform(Platform_ID) ON DELETE CASCADE,
    CONSTRAINT fk_platform_stats_topgame FOREIGN KEY (Top_Game_ID) 
        REFERENCES Game(Game_ID) ON DELETE SET NULL
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

LOAD DATA LOCAL INFILE 'D:/databeez-blg317e-project/data/platforms.csv'
INTO TABLE Platform_raw
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE 'D:/databeez-blg317e-project/data/genres.csv'
INTO TABLE Genre_Raw
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE 'D:/databeez-blg317e-project/data/publishers.csv'
INTO TABLE Publisher_raw
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

-- a. PARENT TABLES (Tables without foreign keys)

-- Load Non-keys for Genre Table (Zeynep Nur Genel)
INSERT INTO Genre (
    Genre_Name, 
    Description, 
    Example_Game)

SELECT
    t.Genre_Name, 
    t.`Description`, 
    t.Example_Game
FROM    
    genre_raw t;

-- Load Non-keys for Platform Table (Mertcan Kılınç)
INSERT INTO Platform (
    Platform_Name, 
    Manufacturer, 
    Release_Year)

SELECT
    t.Platform_Name, 
    t.Manufacturer, 
    t.Release_Year
FROM    
    platform_raw t;

-- Load Non-keys for Publisher Table (Mertcan Kılınç)
INSERT INTO Publisher (
    Publisher_Name, 
    Country, 
    Year_Established)

SELECT
    t.Publisher_Name, 
    t.Country, 
    t.Year_Established
FROM    
    publisher_raw t;

-- b. CHILD TABLES (Have foreign key of parent tables)

-- Load Game table with foreign keys (Berk Özcan)
INSERT INTO Game (
    `Name`,
    `Year`,
    `Rank`,
    Publisher_ID,
    Platform_ID,
    Genre_ID
)
SELECT
    r.`Name`,
    CAST(NULLIF(r.`Year`, 'N/A') AS UNSIGNED),
    r.`Rank`,
    p.Publisher_ID,
    pl.Platform_ID,
    g.Genre_ID
FROM
    vgsales_raw r
JOIN Publisher p ON r.Publisher = p.Publisher_Name
JOIN Platform pl ON r.Platform = pl.Platform_Name
JOIN Genre g ON r.Genre = g.Genre_Name;

-- Load sales data into Sales Table (Zeynep Kocabıyık)
INSERT INTO Sales (
    Game_ID, 
    NA_Sales, 
    EU_Sales, 
    JP_Sales, 
    Other_Sales, 
    Global_Sales
)
SELECT
    g.Game_ID,
    r.NA_Sales,
    r.EU_Sales,
    r.JP_Sales,
    r.Other_Sales,
    r.Global_Sales
FROM
    vgsales_raw r
JOIN
    Game g ON r.`Name` = g.`Name` AND r.`Rank` = g.`Rank`;
    
-- c. SUMMARY TABLES

-- Load Genre Stats Table
INSERT INTO Genre_Stats (Genre_ID, Top_Game_ID, Total_Games, Total_Global_Sales, Avg_Global_Sales)
WITH GenreAggregates AS (
    SELECT 
        g.Genre_ID,
        COUNT(g.Game_ID) AS Total_Games,
        SUM(s.Global_Sales) AS Total_Sales,
        ROUND(AVG(s.Global_Sales), 2) AS Avg_Sales
    FROM Game g
    JOIN Sales s ON g.Game_ID = s.Game_ID
    GROUP BY g.Genre_ID
),
TopGames AS (
    SELECT 
        g.Genre_ID,
        g.Game_ID,
        ROW_NUMBER() OVER (PARTITION BY g.Genre_ID ORDER BY s.Global_Sales DESC) as rn
    FROM Game g
    JOIN Sales s ON g.Game_ID = s.Game_ID
)
SELECT 
    ga.Genre_ID,
    tg.Game_ID,
    ga.Total_Games,
    ga.Total_Sales,
    ga.Avg_Sales
FROM GenreAggregates ga
JOIN TopGames tg ON ga.Genre_ID = tg.Genre_ID
WHERE tg.rn = 1;
-- Load Platform Stats Table
 
 

INSERT INTO Platform_Stats (
    Platform_ID,
    Total_Games,
    Total_Global_Sales,
    Avg_Global_Sales,
    Top_Game_ID
)
WITH
    GameSales AS (
        SELECT
            g.Game_ID,
            g.Platform_ID,
            s.Global_Sales
        FROM
            Game AS g
        JOIN
            Sales AS s ON g.Game_ID = s.Game_ID
        WHERE
            s.Global_Sales IS NOT NULL 
    ),
    Aggregates AS (
        SELECT
            p.Platform_ID,
            COUNT(gs.Game_ID) AS Total_Games,
            COALESCE(SUM(gs.Global_Sales), 0.00) AS Total_Global_Sales,
            COALESCE(AVG(gs.Global_Sales), 0.00) AS Avg_Global_Sales
        FROM
            Platform AS p 
        LEFT JOIN
            GameSales AS gs ON p.Platform_ID = gs.Platform_ID
        GROUP BY
            p.Platform_ID
    ),
    RankedGames AS (
        SELECT
            Game_ID,
            Platform_ID,
            ROW_NUMBER() OVER(
                PARTITION BY Platform_ID
                ORDER BY Global_Sales DESC, Game_ID ASC
            ) AS rn
        FROM
            GameSales 
    )
SELECT
    agg.Platform_ID,
    agg.Total_Games,
    agg.Total_Global_Sales,
    agg.Avg_Global_Sales,
    rg.Game_ID AS Top_Game_ID
FROM
    Aggregates AS agg 
LEFT JOIN
    RankedGames AS rg ON agg.Platform_ID = rg.Platform_ID AND rg.rn = 1;

SET SQL_SAFE_UPDATES = 1;