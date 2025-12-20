# db_utils/db_connector.py

import mysql.connector

# Veritabanı Bağlantı Bilgileri (Kendi ayarlarınızla değiştirin)
DB_CONFIG = {
    'user': 'root',
    'password': 'Mustcan_3017.mysql', 
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



