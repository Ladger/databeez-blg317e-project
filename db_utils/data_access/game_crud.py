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
    """
    Belirtilen Game_ID'yi siler. 
    ÖNCE Sales tablosundaki bağlı veriyi siler, SONRA Game'i siler.
    """
    conn = get_db_connection()
    if conn is None:
        return False
        
    cursor = conn.cursor()
    
    try:
        query_sales = "DELETE FROM Sales WHERE Game_ID = %s"
        cursor.execute(query_sales, (game_id,))
        
        query_game = "DELETE FROM Game WHERE Game_ID = %s"
        cursor.execute(query_game, (game_id,))
        
        conn.commit()
        
        return cursor.rowcount > 0 
        
    except mysql.connector.Error as err:
        print(f"Game silinirken hata oluştu: {err}")
        conn.rollback() 
        return False
    finally:
        cursor.close()
        conn.close()


def update_all_game_ranks():
    """
    Recalculates Rank for all games based on Global_Sales.
    Uses a fresh connection to avoid 'Unread result found' errors.
    """
    # 1. Use a FRESH connection specifically for this heavy operation
    # Calling get_db_connection() usually creates a new instance if implemented correctly,
    # but ensure your db_connector doesn't return a stale/dirty connection.
    conn = get_db_connection()
    if conn is None:
        return False

    cursor = conn.cursor(buffered=True)

    # 2. Complex Update Query (MySQL 8.0+ syntax)
    # If you are on an older MySQL version that doesn't support CTEs or Window Functions in UPDATE,
    # let me know (we might need a different approach).
    query = """
    UPDATE Game g
    JOIN (
        SELECT 
            Game_ID, 
            RANK() OVER (ORDER BY Global_Sales DESC) as new_rank 
        FROM Sales
    ) as r ON g.Game_ID = r.Game_ID
    SET g.Rank = r.new_rank;
    """

    try:
        # 3. Consume any potential unread results (Safety measure)
        if conn.is_connected():
            conn.commit() # Clear any pending transaction state

        cursor.execute(query)
        conn.commit()
        print(f"Ranks updated successfully. Rows affected: {cursor.rowcount}")
        return True

    except mysql.connector.Error as err:
        print(f"Rank Update Error: {err}")
        # 4. Explicit Rollback on error
        try:
            conn.rollback()
        except:
            pass
        return False

    finally:
        # 5. Clean up
        try:
            cursor.close()
            conn.close()
        except:
            pass