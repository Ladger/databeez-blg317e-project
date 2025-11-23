-- Responsibility: Zeynep Nur Genel

USE databeez_db;

DROP TABLE IF EXISTS Genre_Stats;
CREATE TABLE Genre_Stats (
    Genre_ID INT NOT NULL PRIMARY KEY,
    `Total_Games` INT,
    `Total_Global_Sales` DECIMAL(10, 2) DEFAULT 0.00,
    `Avg_Global_Sales` DECIMAL(10, 2) DEFAULT 0.00,
    Top_Game_ID INT NOT NULL,
    
    FOREIGN KEY (Genre_ID) REFERENCES Genre(Genre_ID),
    FOREIGN KEY (Top_Game_ID) REFERENCES Game(Game_ID)
);