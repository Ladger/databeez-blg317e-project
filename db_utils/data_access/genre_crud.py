# db_utils/data_access/genre_crud.py

import mysql.connector
from ..db_connector import get_db_connection # data_access'ten bir üst klasördeki db_connector'ı çağırır

# Genre tablosu yapısı:
# primary_key: Genre_ID
# non_key_columns: Genre_Name, Description, Example_Game

# ----------------------------------------------------------------------
# CREATE OPERASYONU (INSERT)
# ----------------------------------------------------------------------

def add_new_genre(genre_name, description, example_game):
    """Genre tablosuna yeni bir tür (genre) ekler."""
    
    conn = get_db_connection()
    if conn is None:
        return False
        
    cursor = conn.cursor()
    
    query = """
    INSERT INTO Genre (Genre_Name, Description, Example_Game) 
    VALUES (%s, %s, %s)
    """
    
    data = (genre_name, description, example_game)
    
    try:
        cursor.execute(query, data)
        conn.commit()
        return True 
    except mysql.connector.Error as err:
        print(f"Tür (Genre) eklenirken hata oluştu: {err}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()

# ----------------------------------------------------------------------
# READ OPERASYONU (READ)
# ----------------------------------------------------------------------


def get_genre_by_id(genre_id):
    """Belirtilen Genre_ID'ye ait tek bir tür kaydını döndürür."""
    conn = get_db_connection()
    if conn is None:
        return None
        
    # Sözlük formatında sonuç almak için dictionary=True kullanılır
    cursor = conn.cursor(dictionary=True) 
    
    query = """
    SELECT Genre_ID, Genre_Name, Description, Example_Game
    FROM Genre 
    WHERE Genre_ID = %s
    """
    
    try:
        cursor.execute(query, (genre_id,))
        record = cursor.fetchone() # Tek bir kayıt olduğu için fetchone kullanılır
        return record
    except mysql.connector.Error as err:
        print(f"Tür (Genre) kaydı okunurken hata oluştu: {err}")
        return None
    finally:
        cursor.close()
        conn.close()

# ----------------------------------------------------------------------
# UPDATE OPERASYONU (UPDATE)
# ----------------------------------------------------------------------

def update_genre_record(genre_id, genre_name, description, example_game):
    """Belirtilen Genre_ID'ye ait bilgileri günceller."""
    conn = get_db_connection()
    if conn is None:
        return False
        
    cursor = conn.cursor()
    
    query = """
    UPDATE Genre
    SET 
        Genre_Name = %s,
        Description = %s,
        Example_Game = %s
    WHERE Genre_ID = %s
    """
    
    data = (genre_name, description, example_game, genre_id)
    
    try:
        cursor.execute(query, data)
        conn.commit()
        # rowcount > 0 kontrolü, gerçekten bir satırın güncellendiğini doğrular.
        return cursor.rowcount > 0 
    except mysql.connector.Error as err:
        print(f"Tür (Genre) kaydı güncellenirken hata oluştu: {err}")
        conn.rollback() 
        return False
    finally:
        cursor.close()
        conn.close()


# ----------------------------------------------------------------------
# DELETE OPERASYONU (DELETE)
# ----------------------------------------------------------------------

def delete_genre_record(genre_id):
    """Belirtilen Genre_ID'ye ait kaydı siler."""
    conn = get_db_connection()
    if conn is None:
        return False
        
    cursor = conn.cursor()
    
    query = "DELETE FROM Genre WHERE Genre_ID = %s"
    
    try:
        cursor.execute(query, (genre_id,))
        conn.commit()
        # Eğer bir satır silindiyse (rowcount > 0), True döndür.
        return cursor.rowcount > 0 
    except mysql.connector.Error as err:
        # Eğer bu türe bağlı Game kayıtları varsa (Foreign Key kısıtlaması),
        # burada bir hata (IntegrityError) oluşacaktır.
        print(f"Tür (Genre) kaydı silinirken hata oluştu: {err}")
        conn.rollback() 
        return False
    finally:
        cursor.close()
        conn.close()