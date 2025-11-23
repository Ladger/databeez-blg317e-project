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

    -- Top_Game_ID: The game's ID with top Global Sales within the genre
    (
        SELECT
            GI.Game_ID 
        FROM
            Game AS GI
        INNER JOIN
            Sales AS S ON GI.Game_ID = S.Game_ID        
        WHERE
            GI.Genre_ID = G.Genre_ID
        ORDER BY
            S.Global_Sales DESC
        -- Limit to 1 to get the highest selling game
        LIMIT 1
    ) AS Top_Game_ID,

    -- Total Games: counts games within the current genre
    COUNT(DISTINCT T1.Game_ID) AS Total_Games,
    
    -- Total Global Sales: COALESCE converts NULL (for genres with no sales/games) to 0.0
    COALESCE(SUM(T2.Global_Sales), 0.0) AS Total_Global_Sales,
    
    -- Avg Global Sales: COALESCE converts NULL (for genres with no sales/games) to 0.0
    COALESCE(AVG(T2.Global_Sales), 0.0) AS Avg_Global_Sales

-- Aggregate data:
FROM
    Genre AS G -- The definitive list of all genres
LEFT JOIN
    Game AS T1 ON G.Genre_ID = T1.Genre_ID -- LEFT JOIN includes all genres
LEFT JOIN
    Sales AS T2 ON T1.Game_ID = T2.Game_ID

-- Group the results by the Genre_ID from the Genre table (G)
GROUP BY
    G.Genre_ID;



