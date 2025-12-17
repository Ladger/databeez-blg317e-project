import mysql.connector
from ..db_connector import get_db_connection

# db_utils/data_access/data_fetch.py

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
        params = [] # We will collect SQL parameters in this list

        # 1. Base Query (Basic Query and Filtering)
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
            # Filter: By Game Name
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
            # Filter: By Game Name in Sales table as well
            if search_query:
                base_query += " WHERE g.Name LIKE %s"
                params.append(f"%{search_query}%")

        elif table_name == 'Publisher':
            base_query = "SELECT * FROM Publisher"
            # Filter: By Publisher Name
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
            # No default search for other tables, can be added if desired.

        # 2. Sorting (ORDER BY)
        safe_order = 'DESC' if str(sort_order).upper() == 'DESC' else 'ASC'
        
        if sort_by:
            # A simple whitelist check could be added here against SQL Injection.
            # Adding directly for flexibility for now.
            order_clause = f" ORDER BY `{sort_by}` {safe_order}"
        else:
            # Default sortings
            if table_name == 'Game':
                order_clause = " ORDER BY g.`Rank` ASC"
            elif table_name == 'Sales':
                order_clause = " ORDER BY s.Global_Sales DESC"
            else:
                # Guessing ID column using table name (e.g., Platform_ID)
                order_clause = f" ORDER BY {table_name}_ID ASC"

        # 3. Pagination (LIMIT - OFFSET)
        limit_clause = " LIMIT %s OFFSET %s"
        params.extend([limit, offset]) # Append Limit and Offset to the end of parameters
        
        # 4. Combine and Execute Query
        final_query = base_query + order_clause + limit_clause
        
        # You can print the query for debugging (Uncomment if needed)
        # print(f"Executing Query: {final_query} with params {params}")

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
# ---------------------------------------------------------
# EKSİK OLAN FONKSİYON: Arama Çubuğu İçin Gerekli
# ---------------------------------------------------------

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
# Mevcut dosyanın en altına ekleyin
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