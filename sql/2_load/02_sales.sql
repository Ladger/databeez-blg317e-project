-- Responsibility: Zeynep Kocabıyık
-- Sales Table

USE DatabeeZ_db;

 
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

 