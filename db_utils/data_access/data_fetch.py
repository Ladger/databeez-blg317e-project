import mysql.connector
from ..db_connector import get_db_connection

def fetch_table_data(table_name, limit=100, offset=0, sort_by=None, sort_order='ASC', search_query=None, filters=None):
    ALLOWED_TABLES = ['Game', 'Publisher', 'Platform', 'Genre', 'Sales']
    
    if table_name not in ALLOWED_TABLES:
        return {'data': [], 'total': 0}

    conn = get_db_connection()
    if conn is None:
        return {'data': [], 'total': 0}

    try:
        cursor = conn.cursor(dictionary=True)
        params = []
        where_clauses = []

        if table_name == 'Game':
            select_sql = """
                SELECT g.Game_ID, g.Name, g.Year, g.`Rank`,
                    p.Publisher_Name, pl.Platform_Name, ge.Genre_Name
                FROM Game g
                LEFT JOIN Publisher p ON g.Publisher_ID = p.Publisher_ID
                LEFT JOIN Platform pl ON g.Platform_ID = pl.Platform_ID
                LEFT JOIN Genre ge ON g.Genre_ID = ge.Genre_ID
            """
            count_sql = "SELECT COUNT(*) as total FROM Game g"
            alias = "g" 
        elif table_name == 'Sales':
            select_sql = """
                SELECT s.Sales_ID, g.Name as Game_Name, s.NA_Sales, s.EU_Sales, 
                    s.JP_Sales, s.Other_Sales, s.Global_Sales
                FROM Sales s
                LEFT JOIN Game g ON s.Game_ID = g.Game_ID
            """
            count_sql = "SELECT COUNT(*) as total FROM Sales s LEFT JOIN Game g ON s.Game_ID = g.Game_ID"
            alias = "s"
        else:
            select_sql = f"SELECT * FROM {table_name}"
            count_sql = f"SELECT COUNT(*) as total FROM {table_name}"
            alias = "" 

        if search_query:
            if table_name == 'Game':
                where_clauses.append("g.Name LIKE %s")
                params.append(f"{search_query}%")
            elif table_name == 'Sales':
                where_clauses.append("g.Name LIKE %s")
                params.append(f"{search_query}%")
            else:
                name_col = f"{table_name}_Name"
                where_clauses.append(f"{name_col} LIKE %s")
                params.append(f"{search_query}%")

        if filters:
            for key, value in filters.items():
                if not value: continue 

                if key.startswith('min_'):
                    col = key.replace('min_', '')
                    prefix = f"{alias}." if alias else ""
                    where_clauses.append(f"{prefix}`{col}` >= %s")
                    params.append(value)
                elif key.startswith('max_'):
                    col = key.replace('max_', '')
                    prefix = f"{alias}." if alias else ""
                    where_clauses.append(f"{prefix}`{col}` <= %s")
                    params.append(value)
                else:
                    prefix = f"{alias}." if alias else ""
                    where_clauses.append(f"{prefix}`{key}` = %s")
                    params.append(value)

        if where_clauses:
            full_where = " WHERE " + " AND ".join(where_clauses)
            select_sql += full_where
            count_sql += full_where

        cursor.execute(count_sql, tuple(params))
        count_result = cursor.fetchone()
        total_records = count_result['total'] if count_result else 0

        safe_order = 'DESC' if str(sort_order).upper() == 'DESC' else 'ASC'
        if sort_by:
            select_sql += f" ORDER BY `{sort_by}` {safe_order}"
        else:
            if table_name == 'Game': select_sql += " ORDER BY g.`Rank` ASC"
            elif table_name == 'Sales': select_sql += " ORDER BY s.Global_Sales DESC"
            else: select_sql += f" ORDER BY {table_name}_ID ASC"

        select_sql += " LIMIT %s OFFSET %s"
        params.extend([limit, offset])

        cursor.execute(select_sql, tuple(params))
        result = cursor.fetchall()
        
        return {'data': result, 'total': total_records}

    except mysql.connector.Error as err:
        print(f"Error fetching data from {table_name}: {err}")
        return {'data': [], 'total': 0}
        
    finally:
        if conn:
            cursor.close()
            conn.close()

def get_distinct_values(table_name, column_name):
    """Helper to populate dropdowns like 'Country' or 'Manufacturer'"""
    conn = get_db_connection()
    if conn is None: return []
    
    cursor = conn.cursor(dictionary=True)
    try:
        sql = f"SELECT DISTINCT `{column_name}` as val FROM `{table_name}` WHERE `{column_name}` IS NOT NULL AND `{column_name}` != '' ORDER BY `{column_name}` ASC"
        cursor.execute(sql)
        return [row['val'] for row in cursor.fetchall()]
    except Exception as e:
        print(f"Error getting distinct: {e}")
        return []
    finally:
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

def fetch_filter_options():
    """
    Dropdownlar için Genre, Platform ve Publisher listelerini getirir.
    """
    conn = get_db_connection()
    if conn is None:
        return {'genres': [], 'platforms': [], 'publishers': []}

    cursor = conn.cursor(dictionary=True)
    try:
        data = {}
        
        # 1. Genres
        cursor.execute("SELECT Genre_ID, Genre_Name FROM Genre ORDER BY Genre_Name ASC")
        data['genres'] = cursor.fetchall()
        
        # 2. Platforms
        cursor.execute("SELECT Platform_ID, Platform_Name FROM Platform ORDER BY Platform_Name ASC")
        data['platforms'] = cursor.fetchall()
        
        # 3. Publishers
        cursor.execute("SELECT Publisher_ID, Publisher_Name FROM Publisher ORDER BY Publisher_Name ASC")
        data['publishers'] = cursor.fetchall()
        
        return data

    except mysql.connector.Error as err:
        print(f"Filter fetch error: {err}")
        return {'genres': [], 'platforms': [], 'publishers': []}
    finally:
        if conn:
            cursor.close()
            conn.close()

def search_games_advanced(query, genre_id=None, platform_id=None, publisher_id=None):
    """
    İsim ve seçilen filtrelere göre oyun arar.
    """
    conn = get_db_connection()
    if conn is None:
        return []

    cursor = conn.cursor(dictionary=True)
    try:
        # Temel Sorgu
        sql = """
            SELECT 
                g.Game_ID, 
                g.Name, 
                g.Year,
                pl.Platform_Name, 
                p.Publisher_Name, 
                gen.Genre_Name 
            FROM Game g
            LEFT JOIN Platform pl ON g.Platform_ID = pl.Platform_ID
            LEFT JOIN Publisher p ON g.Publisher_ID = p.Publisher_ID
            LEFT JOIN Genre gen ON g.Genre_ID = gen.Genre_ID
            WHERE 1=1
        """
        params = []

        # Dinamik Filtreleme
        if query:
            sql += " AND g.Name LIKE %s"
            params.append(f"%{query}%")
        
        if genre_id and genre_id != 'all':
            sql += " AND g.Genre_ID = %s"
            params.append(genre_id)
            
        if platform_id and platform_id != 'all':
            sql += " AND g.Platform_ID = %s"
            params.append(platform_id)
            
        if publisher_id and publisher_id != 'all':
            sql += " AND g.Publisher_ID = %s"
            params.append(publisher_id)

        # Sonuçları sırala ve limitle (Çok fazla veri gelmemesi için)
        sql += " ORDER BY g.Rank ASC LIMIT 50"

        cursor.execute(sql, tuple(params))
        return cursor.fetchall()

    except mysql.connector.Error as err:
        print(f"Advanced search error: {err}")
        return []
    finally:
        if conn:
            cursor.close()
            conn.close()