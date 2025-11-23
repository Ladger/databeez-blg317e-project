# db_utils/db_connector.py

import mysql.connector

# Veritabanı Bağlantı Bilgileri (Kendi ayarlarınızla değiştirin)
DB_CONFIG = {
    'user': 'root',
    'password': 'your_db_password', 
    'host': '127.0.0.1',
    'database': 'DatabeeZ_db'
}

def get_db_connection():
    """MySQL veritabanı bağlantısını kurar ve döndürür."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        print(f"Veritabanına bağlanırken hata oluştu: {err}")
        return None


def add_new_game(name, year, rank, publisher_id, platform_id, genre_id):
    """Game tablosuna yeni bir oyun kaydı ekler."""
    
    conn = get_db_connection()
    if conn is None:
        return False
        
    cursor = conn.cursor()
    
    # 1. SQL Sorgusu: Parametreler (%s) ile güvenli sorgu hazırlama
    query = """
    INSERT INTO Game (`Name`, `Year`, `Rank`, Publisher_ID, Platform_ID, Genre_ID) 
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    
    # 2. Veri Demeti: Parametreleri bir tuple (demet) olarak hazırlama
    data = (name, year, rank, publisher_id, platform_id, genre_id)
    
    try:
        # 3. Sorguyu Yürütme
        cursor.execute(query, data)
        # 4. Değişiklikleri Kaydetme
        conn.commit()
        return True # Başarılı
    except mysql.connector.Error as err:
        print(f"Oyun eklenirken hata oluştu: {err}")
        conn.rollback() # Hata durumunda geri alma
        return False # Başarısız
    finally:
        # 5. Bağlantıyı Kapatma
        cursor.close()
        conn.close()

# Diğer tablolar için de (Platform, Publisher) benzer fonksiyonlar yazılmalıdır.