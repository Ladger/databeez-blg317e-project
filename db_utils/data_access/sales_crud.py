# db_utils/data_access/sales_crud.py

import mysql.connector
from ..db_connector import get_db_connection # data_access'ten bir üst klasördeki db_connector'ı çağırır

# ----------------------------------------------------------------------
# CREATE OPERASYONU (INSERT)
# ----------------------------------------------------------------------

def add_new_sales(game_id, na_sales, eu_sales, jp_sales, other_sales, global_sales):
    """Sales tablosuna satış verilerini ekler."""
    
    conn = get_db_connection()
    if conn is None:
        return False
        
    cursor = conn.cursor()
    
    query = """
    INSERT INTO Sales (Game_ID, NA_Sales, EU_Sales, JP_Sales, Other_Sales, Global_Sales) 
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    
    data = (game_id, na_sales, eu_sales, jp_sales, other_sales, global_sales)
    
    try:
        cursor.execute(query, data)
        conn.commit()
        return True 
    except mysql.connector.Error as err:
        print(f"Satış verisi eklenirken hata oluştu: {err}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()
        
# ----------------------------------------------------------------------
# READ OPERASYONU (READ)
# ----------------------------------------------------------------------

def get_sales_by_id(sales_id):
    """Belirtilen Sales_ID'ye ait tek bir satış kaydını döndürür."""
    conn = get_db_connection()
    if conn is None:
        return None
        
    # dictionary=True: Sonuçları Python sözlüğü (dictionary) olarak döndürür
    cursor = conn.cursor(dictionary=True) 
    
    query = """
    SELECT Sales_ID, Game_ID, NA_Sales, EU_Sales, JP_Sales, Other_Sales, Global_Sales 
    FROM Sales 
    WHERE Sales_ID = %s
    """
    
    try:
        cursor.execute(query, (sales_id,))
        record = cursor.fetchone()
        return record
    except mysql.connector.Error as err:
        print(f"Sales kaydı okunurken hata oluştu: {err}")
        return None
    finally:
        cursor.close()
        conn.close()

# ----------------------------------------------------------------------
# UPDATE OPERASYONU (UPDATE)
# ----------------------------------------------------------------------

def update_sales_record(sales_id, na_sales, eu_sales, jp_sales, other_sales, global_sales):
    """Belirtilen Sales_ID'ye ait satış değerlerini günceller."""
    conn = get_db_connection()
    if conn is None:
        return False
        
    cursor = conn.cursor()
    
    query = """
    UPDATE Sales
    SET 
        NA_Sales = %s,
        EU_Sales = %s,
        JP_Sales = %s,
        Other_Sales = %s,
        Global_Sales = %s
    WHERE Sales_ID = %s
    """
    
    data = (na_sales, eu_sales, jp_sales, other_sales, global_sales, sales_id)
    
    try:
        cursor.execute(query, data)
        conn.commit()
        # Kaç satırın etkilendiğini kontrol ederek başarıyı döndürür
        return cursor.rowcount > 0 
    except mysql.connector.Error as err:
        print(f"Sales kaydı güncellenirken hata oluştu: {err}")
        conn.rollback() 
        return False
    finally:
        cursor.close()
        conn.close()

# ----------------------------------------------------------------------
# DELETE OPERASYONU (DELETE)
# ----------------------------------------------------------------------

def delete_sales_record(sales_id):
    """Belirtilen Sales_ID'ye ait satış kaydını siler."""
    conn = get_db_connection()
    if conn is None:
        return False
        
    cursor = conn.cursor()
    
    query = "DELETE FROM Sales WHERE Sales_ID = %s"
    
    try:
        cursor.execute(query, (sales_id,))
        conn.commit()
        return cursor.rowcount > 0 
    except mysql.connector.Error as err:
        print(f"Sales kaydı silinirken hata oluştu: {err}")
        conn.rollback() 
        return False
    finally:
        cursor.close()
        conn.close()


