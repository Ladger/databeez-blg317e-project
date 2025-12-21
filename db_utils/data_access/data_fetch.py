import mysql.connector
from ..db_connector import get_db_connection

def fetch_table_data(table_name, limit=100, offset=0, sort_by=None, sort_order='ASC', search_query=None):
    """
    Fetches data using JOIN operations, Sorting, Pagination, and SEARCH capabilities.
    """
    ALLOWED_TABLES = ['Game', 'Publisher', 'Platform', 'Genre', 'Sales']
    
    if table_name not in ALLOWED_TABLES:
        return []

    conn = get_db_connection()
    if conn is None:
        return []

    try:
        cursor = conn.cursor(dictionary=True)
        params = []

        if table_name == 'Game':
            base_query = """
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
            """
            if search_query:
                base_query += " WHERE g.Name LIKE %s"
                params.append(f"%{search_query}%")

        elif table_name == 'Sales':
            base_query = """
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
            """
            if search_query:
                base_query += " WHERE g.Name LIKE %s"
                params.append(f"%{search_query}%")

        elif table_name == 'Publisher':
            base_query = "SELECT * FROM Publisher"
            if search_query:
                base_query += " WHERE Publisher_Name LIKE %s"
                params.append(f"%{search_query}%")
        
        elif table_name == 'Platform':
            base_query = "SELECT * FROM Platform"
            if search_query:
                base_query += " WHERE Platform_Name LIKE %s"
                params.append(f"%{search_query}%")

        elif table_name == 'Genre':
            base_query = "SELECT * FROM Genre"
            if search_query:
                base_query += " WHERE Genre_Name LIKE %s"
                params.append(f"%{search_query}%")
                
        else:
            base_query = f"SELECT * FROM {table_name}"

        safe_order = 'DESC' if str(sort_order).upper() == 'DESC' else 'ASC'
        
        if sort_by:
            order_clause = f" ORDER BY `{sort_by}` {safe_order}"
        else:
            if table_name == 'Game':
                order_clause = " ORDER BY g.`Rank` ASC"
            elif table_name == 'Sales':
                order_clause = " ORDER BY s.Global_Sales DESC"
            else:
                order_clause = f" ORDER BY {table_name}_ID ASC"

        limit_clause = " LIMIT %s OFFSET %s"
        params.extend([limit, offset])
        
        final_query = base_query + order_clause + limit_clause
        

        cursor.execute(final_query, tuple(params))
        result = cursor.fetchall()
        
        return result

    except mysql.connector.Error as err:
        print(f"Error fetching data from {table_name}: {err}")
        return []
        
    finally:
        if conn:
            cursor.close()
            conn.close()

def search_all_tables(search_term, limit=5):
    """
    Game, Publisher, Platform ve Genre tablolarında 'UNION' ile arama yapar.
    """
    conn = get_db_connection()
    if conn is None:
        return []
        
    cursor = conn.cursor(dictionary=True)
    
    sql_term = f"{search_term}%" 
    
    query = f"""
    (SELECT 'Game' AS EntityType, Game_ID AS ID, Name FROM Game WHERE Name LIKE %s LIMIT %s)
    UNION ALL
    (SELECT 'Publisher' AS EntityType, Publisher_ID AS ID, Publisher_Name AS Name FROM Publisher WHERE Publisher_Name LIKE %s LIMIT %s)
    UNION ALL
    (SELECT 'Platform' AS EntityType, Platform_ID AS ID, Platform_Name AS Name FROM Platform WHERE Platform_Name LIKE %s LIMIT %s)
    UNION ALL
    (SELECT 'Genre' AS EntityType, Genre_ID AS ID, Genre_Name AS Name FROM Genre WHERE Genre_Name LIKE %s LIMIT %s)
    ORDER BY Name ASC
    LIMIT {limit};
    """
    
    params = (sql_term, limit, sql_term, limit, sql_term, limit, sql_term, limit)
    
    results = []
    try:
        cursor.execute(query, params)
        results = cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Arama hatası: {err}")
    finally:
        cursor.close()
        conn.close()
        
    return results

def get_record_by_id(table_name, record_id):
    """Tek bir kaydı ID'sine göre çeker."""
    conn = get_db_connection()
    if conn is None:
        return None
    
    cursor = conn.cursor(dictionary=True)
    
    # ID sütun adını bul (Örn: Game -> Game_ID)
    pk_column = f"{table_name}_ID"
    
    # Güvenlik notu: table_name ALLOWED_TABLES listesinde olmalı (fetch_table_data'da var)
    query = f"SELECT * FROM {table_name} WHERE {pk_column} = %s"
    
    try:
        cursor.execute(query, (record_id,))
        result = cursor.fetchone()
        return result
    except mysql.connector.Error as err:
        print(f"Detay çekme hatası: {err}")
        return None
    finally:
        cursor.close()
        conn.close()

def get_detailed_record(table_name, record_id):
    """
    Fetches a single record with JOINs appropriate for the entity type.
    Replaces the complex SQL logic previously in app.py api_get_record.
    """
    conn = get_db_connection()
    if conn is None:
        return None
    
    cursor = conn.cursor(dictionary=True)
    
    try:
        if table_name == 'Game':
            sql = """
                SELECT 
                    g.*,
                    p.Publisher_Name,
                    pl.Platform_Name,
                    ge.Genre_Name
                FROM Game g
                LEFT JOIN Publisher p ON g.Publisher_ID = p.Publisher_ID
                LEFT JOIN Platform pl ON g.Platform_ID = pl.Platform_ID
                LEFT JOIN Genre ge ON g.Genre_ID = ge.Genre_ID
                WHERE g.Game_ID = %s
            """
        elif table_name == 'Sales':
            sql = """
                SELECT 
                    s.*,
                    g.Name as Game_Name
                FROM Sales s
                LEFT JOIN Game g ON s.Game_ID = g.Game_ID
                WHERE s.Sales_ID = %s
            """
        elif table_name == 'Genre':
            sql = """
                SELECT 
                    g.*,
                    gs.Total_Games,
                    gs.Total_Global_Sales,
                    gs.Avg_Global_Sales,
                    gm.Name as Top_Game_Name
                FROM Genre g
                LEFT JOIN Genre_Stats gs ON g.Genre_ID = gs.Genre_ID
                LEFT JOIN Game gm ON gs.Top_Game_ID = gm.Game_ID
                WHERE g.Genre_ID = %s
            """
        elif table_name == 'Platform':
            sql = """
                SELECT 
                    p.*,
                    ps.Total_Games,
                    ps.Total_Global_Sales,
                    ps.Avg_Global_Sales,
                    gm.Name as Top_Game_Name
                FROM Platform p
                LEFT JOIN Platform_Stats ps ON p.Platform_ID = ps.Platform_ID
                LEFT JOIN Game gm ON ps.Top_Game_ID = gm.Game_ID
                WHERE p.Platform_ID = %s
            """
        else:
            pk_column = f"{table_name}_ID"
            sql = f"SELECT * FROM {table_name} WHERE {pk_column} = %s"

        cursor.execute(sql, (record_id,))
        return cursor.fetchone()

    except mysql.connector.Error as err:
        print(f"Error fetching detailed record: {err}")
        return None
    finally:
        cursor.close()
        conn.close()

def search_foreign_keys_data(table, query_text):
    """
    Performs the search for the autocomplete dropdowns.
    """
    table_map = {
        'Publisher': {'id': 'Publisher_ID', 'name': 'Publisher_Name'},
        'Platform':  {'id': 'Platform_ID',  'name': 'Platform_Name'},
        'Genre':     {'id': 'Genre_ID',     'name': 'Genre_Name'}
    }
    
    if table not in table_map or not query_text:
        return []

    col_id = table_map[table]['id']
    col_name = table_map[table]['name']

    conn = get_db_connection()
    if conn is None:
        return []

    cursor = conn.cursor(dictionary=True)
    try:
        sql = f"SELECT {col_id} as id, {col_name} as text FROM {table} WHERE {col_name} LIKE %s LIMIT 10"
        cursor.execute(sql, (f"{query_text}%",))
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"FK Search Error: {err}")
        return []
    finally:
        cursor.close()
        conn.close()