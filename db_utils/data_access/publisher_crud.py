# db_utils/data_access/publisher_crud.py

import mysql.connector
from ..db_connector import get_db_connection

# ----------------------------------------------------------------------
# CREATE OPERASYONU (INSERT)
# ----------------------------------------------------------------------

def add_new_publisher(publisher_name, country, year_established):
    """Publisher tablosuna yeni bir yayıncı ekler."""
    
    conn = get_db_connection()
    if conn is None:
        return False
        
    cursor = conn.cursor()
    
    query = """
    INSERT INTO Publisher (Publisher_Name, Country, Year_Established) 
    VALUES (%s, %s, %s)
    """
    
    data = (publisher_name, country, year_established)
    
    try:
        cursor.execute(query, data)
        conn.commit()
        return True 
    except mysql.connector.Error as err:
        print(f"Publisher eklenirken hata oluştu: {err}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()

# ----------------------------------------------------------------------
# READ OPERASYONU (READ)
# ----------------------------------------------------------------------

def get_publisher_by_id(publisher_id):
    """Belirtilen Publisher_ID'ye ait tek bir yayıncı kaydını döndürür."""
    conn = get_db_connection()
    if conn is None:
        return None
        
    cursor = conn.cursor(dictionary=True) 
    
    query = """
    SELECT Publisher_ID, Publisher_Name, Country, Year_Established
    FROM Publisher 
    WHERE Publisher_ID = %s
    """
    
    try:
        cursor.execute(query, (publisher_id,))
        record = cursor.fetchone()
        return record
    except mysql.connector.Error as err:
        print(f"Publisher kaydı okunurken hata oluştu: {err}")
        return None
    finally:
        cursor.close()
        conn.close()

# ----------------------------------------------------------------------
# UPDATE OPERASYONU (UPDATE)
# ----------------------------------------------------------------------

def update_publisher_record(publisher_id, publisher_name, country, year_established):
    """Belirtilen Publisher_ID'ye ait bilgileri günceller."""
    conn = get_db_connection()
    if conn is None:
        return False
        
    cursor = conn.cursor()
    
    query = """
    UPDATE Publisher
    SET 
        Publisher_Name = %s,
        Country = %s,
        Year_Established = %s
    WHERE Publisher_ID = %s
    """
    
    data = (publisher_name, country, year_established, publisher_id)
    
    try:
        cursor.execute(query, data)
        conn.commit()
        return cursor.rowcount > 0 
    except mysql.connector.Error as err:
        print(f"Publisher kaydı güncellenirken hata oluştu: {err}")
        conn.rollback() 
        return False
    finally:
        cursor.close()
        conn.close()

# ----------------------------------------------------------------------
# DELETE OPERASYONU (DELETE)
# ----------------------------------------------------------------------

def delete_publisher_record(publisher_id):
    """Belirtilen Publisher_ID'ye ait kaydı siler."""
    conn = get_db_connection()
    if conn is None:
        return False
        
    cursor = conn.cursor()
    
    query = "DELETE FROM Publisher WHERE Publisher_ID = %s"
    
    try:
        cursor.execute(query, (publisher_id,))
        conn.commit()
        return cursor.rowcount > 0 
    except mysql.connector.Error as err:
        # ÖNEMLİ: Eğer bu yayıncıya bağlı oyunlar (Game tablosunda) varsa,
        # Foreign Key kısıtlaması nedeniyle silme işlemi başarısız olabilir.
        print(f"Publisher kaydı silinirken hata oluştu: {err}")
        conn.rollback() 
        return False
    finally:
        cursor.close()
        conn.close()