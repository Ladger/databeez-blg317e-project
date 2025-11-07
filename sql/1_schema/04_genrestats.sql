-- Responsibility: Zeynep Nur Genel

USE databeez_db;

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