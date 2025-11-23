-- Responsibility: Zeynep Nur Genel

USE DatabeeZ_db;

DELETE FROM Genre_Stats;

INSERT INTO Genre_Stats (
    Genre_ID,
    Top_Game_ID,
    Total_Games,
    Total_Global_Sales,
    Avg_Global_Sales
)
SELECT
    G.Genre_ID,
    (
        SELECT GI.Game_ID 
        FROM Game AS GI
        INNER JOIN Sales AS S ON GI.Game_ID = S.Game_ID        
        WHERE GI.Genre_ID = G.Genre_ID
        ORDER BY S.Global_Sales DESC
        LIMIT 1
    ) AS Top_Game_ID,
    COUNT(DISTINCT T1.Game_ID) AS Total_Games,
    COALESCE(SUM(T2.Global_Sales), 0.0) AS Total_Global_Sales,
    COALESCE(AVG(T2.Global_Sales), 0.0) AS Avg_Global_Sales
FROM
    Genre AS G
LEFT JOIN
    Game AS T1 ON G.Genre_ID = T1.Genre_ID
LEFT JOIN
    Sales AS T2 ON T1.Game_ID = T2.Game_ID
GROUP BY
    G.Genre_ID;



