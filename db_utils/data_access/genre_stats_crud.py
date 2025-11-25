# db_utils/data_access/genre_stats_crud.py

import mysql.connector
from ..db_connector import get_db_connection

# Genre_Stats tablosu yapısı:
# primary_key: Genre_ID
# foreign_key: Top_Game_ID (Genre_ID'nin aynı zamanda Genre tablosunun PK'sı olduğu varsayılmıştır)
# non_key_columns: Total_Games, Total_Global_Sales, Avg_Global_Sales

# ----------------------------------------------------------------------
# CREATE OPERASYONU (INSERT)
# ----------------------------------------------------------------------

def add_new_genre_stats(genre_id, total_games, total_global_sales, avg_global_sales, top_game_id):
    """Genre_Stats tablosuna yeni bir istatistik kaydı ekler.
    Genre_ID aynı zamanda Primary Key'dir ve muhtemelen Genre tablosundaki bir kayda karşılık gelmelidir."""
    
    conn = get_db_connection()
    if conn is None:
        return False
        
    cursor = conn.cursor()
    
    query = """
    INSERT INTO Genre_Stats (Genre_ID, Total_Games, Total_Global_Sales, Avg_Global_Sales, Top_Game_ID) 
    VALUES (%s, %s, %s, %s, %s)
    """
    
    data = (genre_id, total_games, total_global_sales, avg_global_sales, top_game_id)
    
    try:
        cursor.execute(query, data)
        conn.commit()
        # Genre_ID zaten bilinen bir PK olduğu için True döndürmek yeterli
        return True 
    except mysql.connector.Error as err:
        # IntegrityError (Foreign Key veya Duplicate PK hatası) burada oluşabilir
        print(f"Tür İstatistikleri (Genre_Stats) eklenirken hata oluştu: {err}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()

# ----------------------------------------------------------------------
# READ OPERASYONU (READ)
# ----------------------------------------------------------------------


def get_genre_stats_by_id(genre_id):
    """Belirtilen Genre_ID'ye ait tek bir istatistik kaydını döndürür."""
    conn = get_db_connection()
    if conn is None:
        return None
        
    cursor = conn.cursor(dictionary=True) 
    
    query = """
    SELECT Genre_ID, Total_Games, Total_Global_Sales, Avg_Global_Sales, Top_Game_ID
    FROM Genre_Stats 
    WHERE Genre_ID = %s
    """
    
    try:
        cursor.execute(query, (genre_id,))
        record = cursor.fetchone()
        return record
    except mysql.connector.Error as err:
        print(f"Tür İstatistikleri (Genre_Stats) kaydı okunurken hata oluştu: {err}")
        return None
    finally:
        cursor.close()
        conn.close()

# ----------------------------------------------------------------------
# UPDATE OPERASYONU (UPDATE)
# ----------------------------------------------------------------------

def update_genre_stats_record(genre_id, total_games, total_global_sales, avg_global_sales, top_game_id):
    """Belirtilen Genre_ID'ye ait istatistik bilgilerini günceller."""
    conn = get_db_connection()
    if conn is None:
        return False
        
    cursor = conn.cursor()
    
    query = """
    UPDATE Genre_Stats
    SET 
        Total_Games = %s,
        Total_Global_Sales = %s,
        Avg_Global_Sales = %s,
        Top_Game_ID = %s
    WHERE Genre_ID = %s
    """
    
    data = (total_games, total_global_sales, avg_global_sales, top_game_id, genre_id)
    
    try:
        cursor.execute(query, data)
        conn.commit()
        # rowcount > 0 kontrolü, gerçekten bir satırın güncellendiğini doğrular.
        return cursor.rowcount > 0 
    except mysql.connector.Error as err:
        # Top_Game_ID'nin Game tablosunda var olmaması (Foreign Key hatası) burada oluşabilir
        print(f"Tür İstatistikleri (Genre_Stats) kaydı güncellenirken hata oluştu: {err}")
        conn.rollback() 
        return False
    finally:
        cursor.close()
        conn.close()


# ----------------------------------------------------------------------
# DELETE OPERASYONU (DELETE)
# ----------------------------------------------------------------------

def delete_genre_stats_record(genre_id):
    """Belirtilen Genre_ID'ye ait istatistik kaydını siler."""
    conn = get_db_connection()
    if conn is None:
        return False
        
    cursor = conn.cursor()
    
    # Genre_Stats tablosunda Genre_ID Primary Key olduğu için silme işlemi doğrudan yapılabilir.
    query = "DELETE FROM Genre_Stats WHERE Genre_ID = %s"
    
    try:
        cursor.execute(query, (genre_id,))
        conn.commit()
        # Eğer bir satır silindiyse (rowcount > 0), True döndür.
        return cursor.rowcount > 0 
    except mysql.connector.Error as err:
        print(f"Tür İstatistikleri (Genre_Stats) kaydı silinirken hata oluştu: {err}")
        conn.rollback() 
        return False
    finally:
        cursor.close()
        conn.close()