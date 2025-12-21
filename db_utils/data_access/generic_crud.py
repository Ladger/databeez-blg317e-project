import mysql.connector
from ..db_connector import get_db_connection

def update_record_dynamic(table_name, record_id, data_dict):
    """
    Constructs a dynamic SQL UPDATE statement based on the dictionary keys provided.
    """
    conn = get_db_connection()
    if conn is None:
        return False, "Database connection failed"

    cursor = conn.cursor()
    pk_column = f"{table_name}_ID"

    try:
        set_clause = ", ".join([f"`{key}` = %s" for key in data_dict.keys()])
        values = list(data_dict.values())
        values.append(record_id)

        sql = f"UPDATE {table_name} SET {set_clause} WHERE {pk_column} = %s"
        
        cursor.execute(sql, tuple(values))
        conn.commit()
        
        return True, "Record updated successfully"
    except mysql.connector.Error as err:
        conn.rollback()
        return False, f"Database Error: {str(err)}"
    finally:
        cursor.close()
        conn.close()

def delete_record_dynamic(table_name, record_id):
    """
    Generic delete function for any table.
    """
    conn = get_db_connection()
    if conn is None:
        return False, "Database connection failed"

    cursor = conn.cursor()
    pk_column = f"{table_name}_ID"
    
    try:
        sql = f"DELETE FROM {table_name} WHERE {pk_column} = %s"
        cursor.execute(sql, (record_id,))
        conn.commit()
        
        if cursor.rowcount > 0:
            return True, "Record deleted successfully"
        else:
            return False, "Record not found"
            
    except mysql.connector.Error as err:
        conn.rollback()
        return False, f"Database Error: {str(err)}"
    finally:
        cursor.close()
        conn.close()