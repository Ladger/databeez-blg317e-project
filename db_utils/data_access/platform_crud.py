# db_utils/data_access/platform_crud.py

import mysql.connector
from ..db_connector import get_db_connection # data_access'ten bir üst klasördeki db_connector'ı çağırır

# ----------------------------------------------------------------------
# CREATE OPERASYONU (INSERT)
# ----------------------------------------------------------------------

def add_new_platform(platform_name, manufacturer, release_year):
    """Platform tablosuna yeni bir platform ekler."""
    
    conn = get_db_connection()
    if conn is None:
        return False
        
    cursor = conn.cursor()
    
    query = """
    INSERT INTO Platform (Platform_Name, Manufacturer, Release_Year) 
    VALUES (%s, %s, %s)
    """
    
    data = (platform_name, manufacturer, release_year)
    
    try:
        cursor.execute(query, data)
        conn.commit()
        return True 
    except mysql.connector.Error as err:
        print(f"Platform eklenirken hata oluştu: {err}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()

# ----------------------------------------------------------------------
# READ OPERASYONU (READ)
# ----------------------------------------------------------------------


def get_platform_by_id(platform_id):
    """Belirtilen Platform_ID'ye ait tek bir platform kaydını döndürür."""
    conn = get_db_connection()
    if conn is None:
        return None
        
    cursor = conn.cursor(dictionary=True) 
    
    query = """
    SELECT Platform_ID, Platform_Name, Manufacturer, Release_Year
    FROM Platform 
    WHERE Platform_ID = %s
    """
    
    try:
        cursor.execute(query, (platform_id,))
        record = cursor.fetchone() # Tek bir kayıt olduğu için fetchone kullanılır
        return record
    except mysql.connector.Error as err:
        print(f"Platform kaydı okunurken hata oluştu: {err}")
        return None
    finally:
        cursor.close()
        conn.close()

# ----------------------------------------------------------------------
# UPDATE OPERASYONU (UPDATE)
# ----------------------------------------------------------------------

def update_platform_record(platform_id, platform_name, manufacturer, release_year):
    """Belirtilen Platform_ID'ye ait bilgileri günceller."""
    conn = get_db_connection()
    if conn is None:
        return False
        
    cursor = conn.cursor()
    
    query = """
    UPDATE Platform
    SET 
        Platform_Name = %s,
        Manufacturer = %s,
        Release_Year = %s
    WHERE Platform_ID = %s
    """
    
    data = (platform_name, manufacturer, release_year, platform_id)
    
    try:
        cursor.execute(query, data)
        conn.commit()
        # rowcount > 0 kontrolü, gerçekten bir satırın güncellendiğini doğrular.
        return cursor.rowcount > 0 
    except mysql.connector.Error as err:
        print(f"Platform kaydı güncellenirken hata oluştu: {err}")
        conn.rollback() 
        return False
    finally:
        cursor.close()
        conn.close()


# ----------------------------------------------------------------------
# DELETE OPERASYONU (DELETE)
# ----------------------------------------------------------------------

# db_utils/data_access/platform_crud.py

def delete_platform_record(platform_id):
    """Belirtilen Platform_ID'ye ait kaydı siler."""
    conn = get_db_connection()
    if conn is None:
        return False
        
    cursor = conn.cursor()
    
    query = "DELETE FROM Platform WHERE Platform_ID = %s"
    
    try:
        cursor.execute(query, (platform_id,))
        conn.commit()
        # Eğer bir satır silindiyse (rowcount > 0), True döndür.
        return cursor.rowcount > 0 
    except mysql.connector.Error as err:
        # Eğer bu platforma bağlı Game kayıtları varsa (Foreign Key kısıtlaması),
        # burada bir hata (IntegrityError) oluşacaktır.
        print(f"Platform kaydı silinirken hata oluştu: {err}")
        conn.rollback() 
        return False
    finally:
        cursor.close()
        conn.close()