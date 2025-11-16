-- Responsibility: Mertcan Kilinc

USE DatabeeZ_db;

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

