# db_utils/data_access/platform_stats_crud.py

import mysql.connector
from ..db_connector import get_db_connection

# ----------------------------------------------------------------------
# CREATE OPERASYONU (INSERT)
# ----------------------------------------------------------------------

def add_platform_stat(platform_id, total_games, total_global_sales, avg_global_sales, top_game_id):
    """
    Platform_Stats tablosuna yeni bir istatistik kaydı ekler.
    
    ÖNEMLİ: 
    - platform_id: Platform tablosunda var olan geçerli bir ID olmalıdır.
    - top_game_id: Game tablosunda var olan geçerli bir ID olmalıdır.
    """
    
    conn = get_db_connection()
    if conn is None:
        return False
        
    cursor = conn.cursor()
    
    query = """
    INSERT INTO Platform_Stats (Platform_ID, Total_Games, Total_Global_Sales, Avg_Global_Sales, Top_Game_ID) 
    VALUES (%s, %s, %s, %s, %s)
    """
    
    data = (platform_id, total_games, total_global_sales, avg_global_sales, top_game_id)
    
    try:
        cursor.execute(query, data)
        conn.commit()
        return True 
    except mysql.connector.Error as err:
        print(f"İstatistik eklenirken hata oluştu: {err}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()

# ----------------------------------------------------------------------
# READ OPERASYONU (READ)
# ----------------------------------------------------------------------

def get_platform_stat_by_id(platform_id):
    """Belirtilen Platform_ID'ye ait istatistik kaydını döndürür."""
    conn = get_db_connection()
    if conn is None:
        return None
        
    cursor = conn.cursor(dictionary=True) 
    
    query = """
    SELECT Platform_ID, Total_Games, Total_Global_Sales, Avg_Global_Sales, Top_Game_ID
    FROM Platform_Stats 
    WHERE Platform_ID = %s
    """
    
    try:
        cursor.execute(query, (platform_id,))
        record = cursor.fetchone()
        return record
    except mysql.connector.Error as err:
        print(f"İstatistik kaydı okunurken hata oluştu: {err}")
        return None
    finally:
        cursor.close()
        conn.close()

# ----------------------------------------------------------------------
# UPDATE OPERASYONU (UPDATE)
# ----------------------------------------------------------------------

def update_platform_stat(platform_id, total_games, total_global_sales, avg_global_sales, top_game_id):
    """Belirtilen Platform_ID'ye ait istatistikleri günceller."""
    conn = get_db_connection()
    if conn is None:
        return False
        
    cursor = conn.cursor()
    
    query = """
    UPDATE Platform_Stats
    SET 
        Total_Games = %s,
        Total_Global_Sales = %s,
        Avg_Global_Sales = %s,
        Top_Game_ID = %s
    WHERE Platform_ID = %s
    """
    
    data = (total_games, total_global_sales, avg_global_sales, top_game_id, platform_id)
    
    try:
        cursor.execute(query, data)
        conn.commit()
        return cursor.rowcount > 0 
    except mysql.connector.Error as err:
        print(f"İstatistik güncellenirken hata oluştu: {err}")
        conn.rollback() 
        return False
    finally:
        cursor.close()
        conn.close()

# ----------------------------------------------------------------------
# DELETE OPERASYONU (DELETE)
# ----------------------------------------------------------------------

def delete_platform_stat(platform_id):
    """Belirtilen Platform_ID'ye ait istatistik kaydını siler."""
    conn = get_db_connection()
    if conn is None:
        return False
        
    cursor = conn.cursor()
    
    query = "DELETE FROM Platform_Stats WHERE Platform_ID = %s"
    
    try:
        cursor.execute(query, (platform_id,))
        conn.commit()
        return cursor.rowcount > 0 
    except mysql.connector.Error as err:
        print(f"İstatistik silinirken hata oluştu: {err}")
        conn.rollback() 
        return False
    finally:
        cursor.close()
        conn.close()