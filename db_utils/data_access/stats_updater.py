import mysql.connector
from ..db_connector import get_db_connection

def update_all_genre_stats():
    """
    Recalculates Genre_Stats from scratch based on current Game and Sales data.
    FIXED: Starts from 'Genre' table to ensure empty genres get reset to 0.
    """
    conn = get_db_connection()
    if conn is None: return False
    
    cursor = conn.cursor()
    
    sql = """
    REPLACE INTO Genre_Stats (Genre_ID, Top_Game_ID, Total_Games, Total_Global_Sales, Avg_Global_Sales)
    SELECT 
        g.Genre_ID,
        (
            SELECT gm.Game_ID 
            FROM Game gm 
            JOIN Sales s ON gm.Game_ID = s.Game_ID 
            WHERE gm.Genre_ID = g.Genre_ID 
            ORDER BY s.Global_Sales DESC 
            LIMIT 1
        ) AS Top_Game_ID,
        COUNT(gm.Game_ID) AS Total_Games,
        COALESCE(SUM(s.Global_Sales), 0) AS Total_Global_Sales,
        COALESCE(ROUND(AVG(s.Global_Sales), 2), 0) AS Avg_Global_Sales
    FROM Genre g
    LEFT JOIN Game gm ON g.Genre_ID = gm.Genre_ID
    LEFT JOIN Sales s ON gm.Game_ID = s.Game_ID
    GROUP BY g.Genre_ID;
    """
    
    try:
        cursor.execute(sql)
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Error updating Genre Stats: {err}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()

def update_all_platform_stats():
    """
    Recalculates Platform_Stats from scratch based on current Game and Sales data.
    FIXED: Starts from 'Platform' table to ensure empty platforms get reset to 0.
    """
    conn = get_db_connection()
    if conn is None: return False
    
    cursor = conn.cursor()
    
    sql = """
    REPLACE INTO Platform_Stats (Platform_ID, Top_Game_ID, Total_Games, Total_Global_Sales, Avg_Global_Sales)
    SELECT 
        p.Platform_ID,
        (
            SELECT gm.Game_ID 
            FROM Game gm 
            JOIN Sales s ON gm.Game_ID = s.Game_ID 
            WHERE gm.Platform_ID = p.Platform_ID 
            ORDER BY s.Global_Sales DESC 
            LIMIT 1
        ) AS Top_Game_ID,
        COUNT(gm.Game_ID) AS Total_Games,
        COALESCE(SUM(s.Global_Sales), 0) AS Total_Global_Sales,
        COALESCE(ROUND(AVG(s.Global_Sales), 2), 0) AS Avg_Global_Sales
    FROM Platform p
    LEFT JOIN Game gm ON p.Platform_ID = gm.Platform_ID
    LEFT JOIN Sales s ON gm.Game_ID = s.Game_ID
    GROUP BY p.Platform_ID;
    """
    
    try:
        cursor.execute(sql)
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Error updating Platform Stats: {err}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()