# db_utils/data_access/game_crud.py

import mysql.connector
from ..db_connector import get_db_connection

# ----------------------------------------------------------------------
# CREATE OPERASYONU (INSERT)
# ----------------------------------------------------------------------

def add_new_game(name, year, rank, publisher_id, platform_id, genre_id):
    """Game tablosuna yeni oyun verilerini ekler."""
    
    conn = get_db_connection()
    if conn is None:
        return False
        
    cursor = conn.cursor()
    
    query = """
    INSERT INTO Game (Name, Year, `Rank`, Publisher_ID, Platform_ID, Genre_ID) 
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    
    data = (name, year, rank, publisher_id, platform_id, genre_id)
    
    try:
        cursor.execute(query, data)
        conn.commit()

        new_game_id = cursor.lastrowid 
        return new_game_id
    except mysql.connector.Error as err:
        print(f"Oyun verisi eklenirken hata oluştu: {err}")
        conn.rollback()
        return None
    finally:
        cursor.close()
        conn.close()

# ----------------------------------------------------------------------
# READ OPERASYONU (READ)
# ----------------------------------------------------------------------

def get_game_by_id(game_id):
    """Belirtilen Game_ID'ye ait tek bir oyun kaydını döndürür."""
    conn = get_db_connection()
    if conn is None:
        return None
        
    cursor = conn.cursor(dictionary=True) 
    
    query = """
    SELECT Game_ID, Name, Year, `Rank`, Publisher_ID, Platform_ID, Genre_ID
    FROM Game 
    WHERE Game_ID = %s
    """
    
    try:
        cursor.execute(query, (game_id,))
        record = cursor.fetchone()
        return record
    except mysql.connector.Error as err:
        print(f"Game kaydı okunurken hata oluştu: {err}")
        return None
    finally:
        cursor.close()
        conn.close()

# ----------------------------------------------------------------------
# UPDATE OPERASYONU (UPDATE)
# ----------------------------------------------------------------------

def update_game_record(game_id, name, year, rank, publisher_id, platform_id, genre_id):
    """Belirtilen Game_ID'ye ait oyun bilgilerini günceller."""
    conn = get_db_connection()
    if conn is None:
        return False
        
    cursor = conn.cursor()
    
    query = """
    UPDATE Game
    SET 
        Name = %s,
        Year = %s,
        `Rank` = %s,
        Publisher_ID = %s,
        Platform_ID = %s,
        Genre_ID = %s
    WHERE Game_ID = %s
    """
    
    data = (name, year, rank, publisher_id, platform_id, genre_id, game_id)
    
    try:
        cursor.execute(query, data)
        conn.commit()
        return cursor.rowcount > 0 
    except mysql.connector.Error as err:
        print(f"Game kaydı güncellenirken hata oluştu: {err}")
        conn.rollback() 
        return False
    finally:
        cursor.close()
        conn.close()

# ----------------------------------------------------------------------
# DELETE OPERASYONU (DELETE)
# ----------------------------------------------------------------------

def delete_game_record(game_id):
    """Belirtilen Game_ID'ye ait oyun kaydını siler."""
    conn = get_db_connection()
    if conn is None:
        return False
        
    cursor = conn.cursor()
    
    query = "DELETE FROM Game WHERE Game_ID = %s"
    
    try:
        cursor.execute(query, (game_id,))
        conn.commit()
        return cursor.rowcount > 0 
    except mysql.connector.Error as err:
        print(f"Game kaydı silinirken hata oluştu: {err}")
        conn.rollback() 
        return False
    finally:
        cursor.close()
        conn.close()