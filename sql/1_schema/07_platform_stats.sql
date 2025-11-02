-- Responsibility: Mertcan Kilinc

USE databeez_db;

DROP TABLE IF EXISTS Platform_Stats;
CREATE TABLE Platform_Stats(
    Platform_ID INT AUTO_INCREMENT PRIMARY KEY,
    Total_Games INT,
    Total_Global_Sales DECIMAL(5, 2),
    Avg_Global_Sales DECIMAL(5, 2),
    
    Top_Game_ID INT
);

