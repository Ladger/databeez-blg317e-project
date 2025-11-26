import mysql.connector
from ..db_connector import get_db_connection

def fetch_table_data(table_name, limit=100):
    """
    Fetches data with JOINS to replace IDs with actual names for Game and Sales tables.
    """
    ALLOWED_TABLES = ['Game', 'Publisher', 'Platform', 'Genre', 'Sales']
    
    if table_name not in ALLOWED_TABLES:
        return []

    conn = get_db_connection()
    if conn is None:
        return []

    try:
        cursor = conn.cursor(dictionary=True)
        
        if table_name == 'Game':
            query = """
                SELECT 
                    g.Game_ID, 
                    g.Name, 
                    g.Year, 
                    g.`Rank`,
                    p.Publisher_Name, 
                    pl.Platform_Name, 
                    ge.Genre_Name
                FROM Game g
                LEFT JOIN Publisher p ON g.Publisher_ID = p.Publisher_ID
                LEFT JOIN Platform pl ON g.Platform_ID = pl.Platform_ID
                LEFT JOIN Genre ge ON g.Genre_ID = ge.Genre_ID
                LIMIT %s
            """
            
        elif table_name == 'Sales':
            query = """
                SELECT 
                    s.Sales_ID, 
                    g.Name as Game_Name, 
                    s.NA_Sales, 
                    s.EU_Sales, 
                    s.JP_Sales, 
                    s.Other_Sales, 
                    s.Global_Sales
                FROM Sales s
                LEFT JOIN Game g ON s.Game_ID = g.Game_ID
                LIMIT %s
            """
            
        else:
            query = f"SELECT * FROM {table_name} LIMIT %s"
        
        cursor.execute(query, (limit,))
        result = cursor.fetchall()
        
        return result

    except mysql.connector.Error as err:
        print(f"Error fetching data from {table_name}: {err}")
        return []
        
    finally:
        if conn:
            cursor.close()
            conn.close()