USE DatabeeZ_db;

SET SQL_SAFE_UPDATES = 0;

DELETE FROM Platform_Stats;

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
            Global_Sales,
            ROW_NUMBER() OVER(
                PARTITION BY Platform_ID
                ORDER BY Global_Sales DESC, Game_ID ASC
            ) AS rn
        FROM
            GameSales 
    )
    
INSERT INTO Platform_Stats (
    Platform_ID,
    Total_Games,
    Total_Global_Sales,
    Avg_Global_Sales,
    Top_Game_ID
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