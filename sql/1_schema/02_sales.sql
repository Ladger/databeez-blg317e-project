-- Responsibility: Zeynep Kocabıyık
USE DatabeeZ_db;
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