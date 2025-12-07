import mysql.connector
from ..db_connector import get_db_connection

def fetch_table_data(table_name, limit=100, offset=0, sort_by=None, sort_order='ASC'):
    """
    Game ve Sales tabloları için ID yerine isimleri getiren JOIN'li veri çekme fonksiyonu.
    Diğer tablolar için standart SELECT * yapar.
    """
    ALLOWED_TABLES = ['Game', 'Publisher', 'Platform', 'Genre', 'Sales']
    
    if table_name not in ALLOWED_TABLES:
        return []

    conn = get_db_connection()
    if conn is None:
        return []

    try:
        cursor = conn.cursor(dictionary=True)
        
        base_query = "" # Değişkeni başlatıyoruz

        # 1. Base Query Hazırlığı
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
            
        elif table_name == 'Sales':
            # DÜZELTME: 'query' yerine 'base_query' değişkenine atandı
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
            
        else:
            # DÜZELTME: LIMIT buraya eklenmemeli, aşağıda ortak mantıkta eklenecek.
            base_query = f"SELECT * FROM {table_name}"
        
        # 2. Sıralama Mantığı (Ordering)
        safe_order = 'DESC' if str(sort_order).upper() == 'DESC' else 'ASC'
        order_clause = ""
        
        if sort_by:
            # Güvenlik notu: sort_by sütun adının geçerliliği kontrol edilmelidir.
            order_clause = f" ORDER BY `{sort_by}` {safe_order}"
        else:
            if table_name == 'Game':
                order_clause = " ORDER BY g.`Rank` ASC"
            elif table_name == 'Sales':
                order_clause = " ORDER BY s.Global_Sales DESC"
            else:
                order_clause = f" ORDER BY {table_name}_ID ASC"
        
        # 3. Sayfalandırma ve Birleştirme
        limit_clause = " LIMIT %s OFFSET %s"

        # DÜZELTME: Tüm parçalar birleştirilip final_query oluşturuluyor
        final_query = base_query + order_clause + limit_clause
        
        # DÜZELTME: execute metoduna 'query' değil 'final_query' gönderiliyor
        cursor.execute(final_query, (limit, offset))
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