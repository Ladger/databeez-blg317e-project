from flask import Flask, request, render_template, jsonify
from flask_cors import CORS

from db_utils.db_connector import get_db_connection
from db_utils.data_access.data_fetch import fetch_table_data, search_all_tables, get_record_by_id
from db_utils.data_access.game_crud import add_new_game, update_all_game_ranks
from db_utils.data_access.sales_crud import add_new_sales
from db_utils.data_access.genre_crud import add_new_genre
from db_utils.data_access.platform_crud import add_new_platform
from db_utils.data_access.publisher_crud import add_new_publisher
from db_utils.data_access.stats_updater import update_all_genre_stats, update_all_platform_stats

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_entry')
def add_entry_page():
    return render_template('add_entry.html')

@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    term = request.args.get('term', '')
    if len(term) < 2:
        return jsonify([])
    results = search_all_tables(term, limit=5)
    return jsonify(results)

@app.route('/detailed_view/<entity_type>/<int:entity_id>')
def detailed_view(entity_type, entity_id):
    context = {
        'entity_type': entity_type,
        'entity_id': entity_id,
        'title': f"{entity_type} Detay Sayfası (ID: {entity_id})"
    }
    return render_template('detailed_view.html', **context)

@app.route('/api/get_record/<table_name>/<int:record_id>')
def api_get_record(table_name, record_id):
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Database connection failed'}), 500
    
    cursor = conn.cursor(dictionary=True)
    
    try:
        if table_name == 'Game':
            sql = """
                SELECT 
                    g.*,
                    p.Publisher_Name,
                    pl.Platform_Name,
                    ge.Genre_Name
                FROM Game g
                LEFT JOIN Publisher p ON g.Publisher_ID = p.Publisher_ID
                LEFT JOIN Platform pl ON g.Platform_ID = pl.Platform_ID
                LEFT JOIN Genre ge ON g.Genre_ID = ge.Genre_ID
                WHERE g.Game_ID = %s
            """
            cursor.execute(sql, (record_id,))
            data = cursor.fetchone()

        elif table_name == 'Sales':
            sql = """
                SELECT 
                    s.*,
                    g.Name as Game_Name
                FROM Sales s
                LEFT JOIN Game g ON s.Game_ID = g.Game_ID
                WHERE s.Sales_ID = %s
            """
            cursor.execute(sql, (record_id,))
            data = cursor.fetchone()

        elif table_name == 'Genre':
            sql = """
                SELECT 
                    g.*,
                    gs.Total_Games,
                    gs.Total_Global_Sales,
                    gs.Avg_Global_Sales,
                    gm.Name as Top_Game_Name
                FROM Genre g
                LEFT JOIN Genre_Stats gs ON g.Genre_ID = gs.Genre_ID
                LEFT JOIN Game gm ON gs.Top_Game_ID = gm.Game_ID
                WHERE g.Genre_ID = %s
            """
            cursor.execute(sql, (record_id,))
            data = cursor.fetchone()

        elif table_name == 'Platform':
            sql = """
                SELECT 
                    p.*,
                    ps.Total_Games,
                    ps.Total_Global_Sales,
                    ps.Avg_Global_Sales,
                    gm.Name as Top_Game_Name
                FROM Platform p
                LEFT JOIN Platform_Stats ps ON p.Platform_ID = ps.Platform_ID
                LEFT JOIN Game gm ON ps.Top_Game_ID = gm.Game_ID
                WHERE p.Platform_ID = %s
            """
            cursor.execute(sql, (record_id,))
            data = cursor.fetchone()

        else:
            pk_column = f"{table_name}_ID"
            sql = f"SELECT * FROM {table_name} WHERE {pk_column} = %s"
            cursor.execute(sql, (record_id,))
            data = cursor.fetchone()

        if data:
            return jsonify(data)
        else:
            return jsonify({'error': 'Record not found'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/update_record/<table_name>/<int:record_id>', methods=['POST'])
def update_record(table_name, record_id):
    allowed_tables = ['Game', 'Publisher', 'Platform', 'Genre', 'Sales']
    if table_name not in allowed_tables:
        return jsonify({'success': False, 'message': 'Invalid table'}), 400

    data = request.form.to_dict()
    
    pk_column = f"{table_name}_ID"
    if pk_column in data:
        del data[pk_column]
        
    keys_to_remove = [k for k in data.keys() if k.endswith('_display')]
    for k in keys_to_remove:
        del data[k]

    if 'Rank' in data:
        del data['Rank']

    if not data:
        return jsonify({'success': False, 'message': 'No data provided'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        set_clause = ", ".join([f"`{key}` = %s" for key in data.keys()])
        
        values = list(data.values())
        values.append(record_id)

        sql = f"UPDATE {table_name} SET {set_clause} WHERE {pk_column} = %s"
        
        cursor.execute(sql, tuple(values))
        conn.commit()
        
        if table_name == 'Game' or table_name == 'Sales':
            update_all_game_ranks()
            
            update_all_genre_stats()
            update_all_platform_stats()

        return jsonify({'success': True, 'message': 'Record updated successfully'})
    
    except Exception as e:
        conn.rollback()
        print(f"SQL Error: {str(e)}")
        return jsonify({'success': False, 'message': f"Database Error: {str(e)}"}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/table_view')
def table_view():
    return render_template('table_view.html')

@app.route('/api/get_data/<table_name>', methods=['GET'])
def get_data(table_name):
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', default=100, type=int)
    sort_by = request.args.get('sort_by', default=None, type=str)
    sort_order = request.args.get('order', default='ASC', type=str)
    search_query = request.args.get('search', default=None, type=str)
    
    offset = (page - 1) * limit
    
    result = fetch_table_data(
        table_name, 
        limit=limit, 
        offset=offset, 
        sort_by=sort_by, 
        sort_order=sort_order,
        search_query=search_query
    )
    
    return jsonify(result)

@app.route('/api/search_fk', methods=['GET'])
def search_fk():
    table_map = {
        'Publisher': {'id': 'Publisher_ID', 'name': 'Publisher_Name'},
        'Platform':  {'id': 'Platform_ID',  'name': 'Platform_Name'},
        'Genre':     {'id': 'Genre_ID',     'name': 'Genre_Name'}
    }
    
    table = request.args.get('table')
    query_text = request.args.get('query', '')
    
    if table not in table_map or not query_text:
        return jsonify([])

    col_id = table_map[table]['id']
    col_name = table_map[table]['name']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    sql = f"SELECT {col_id} as id, {col_name} as text FROM {table} WHERE {col_name} LIKE %s LIMIT 10"
    cursor.execute(sql, (f"{query_text}%",))
    results = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return jsonify(results)

@app.route('/api/delete_record/<entity_type>/<int:entity_id>', methods=['DELETE'])
def api_delete_record(entity_type, entity_id):
    ALLOWED_TABLES = ['Game', 'Publisher', 'Platform', 'Genre', 'Sales']
    
    if entity_type not in ALLOWED_TABLES:
        return jsonify({'success': False, 'message': 'Invalid table name.'}), 400

    conn = get_db_connection()
    if conn is None:
        return jsonify({'success': False, 'message': 'Database connection failed.'}), 500

    try:
        cursor = conn.cursor()
        pk_column = f"{entity_type}_ID"
        
        sql = f"DELETE FROM {entity_type} WHERE {pk_column} = %s"
        cursor.execute(sql, (entity_id,))
        
        conn.commit()
        
        if cursor.rowcount > 0:
            if entity_type == 'Game':
                update_all_game_ranks()

            if entity_type == 'Game' or entity_type == 'Sales':
                update_all_genre_stats()
                update_all_platform_stats()
                
            return jsonify({'success': True, 'message': f'Record deleted successfully from {entity_type}.'})
        else:
            return jsonify({'success': False, 'message': 'Record not found.'}), 404

    except Exception as e:
        conn.rollback()
        return jsonify({'success': False, 'message': f'Database Error: {str(e)}'}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/add_game', methods=['POST'])
def add_game():
    try:
        pub_id_str = request.form.get('publisher_id', '')
        plat_id_str = request.form.get('platform_id', '')
        gen_id_str = request.form.get('genre_id', '')

        if not pub_id_str or not plat_id_str or not gen_id_str:
            return jsonify({'success': False, 'message': "Error: Please select Publisher, Platform, and Genre from dropdowns."}), 400

        publisher_id = int(pub_id_str)
        platform_id = int(plat_id_str)
        genre_id = int(gen_id_str)
        name = request.form['game_name']
        year = int(request.form.get('game_year') or 0)
        temp_rank = 999999 
        
        new_game_id = add_new_game(name, year, temp_rank, publisher_id, platform_id, genre_id)

        if new_game_id:
            na = float(request.form.get('na_sales') or 0)
            eu = float(request.form.get('eu_sales') or 0)
            jp = float(request.form.get('jp_sales') or 0)
            other = float(request.form.get('other_sales') or 0)
            
            global_sales = na + eu + jp + other
            
            sales_success = add_new_sales(new_game_id, na, eu, jp, other, global_sales)
            
            if sales_success:
                rank_success = update_all_game_ranks()
                
                update_all_genre_stats()
                update_all_platform_stats()

                if rank_success:
                    return jsonify({'success': True, 'message': "Success! Game added and Ranks updated."})
                else:
                    return jsonify({'success': True, 'message': "Game added, but Rank calculation failed."})
            else:
                return jsonify({'success': False, 'message': "Game added, but Sales data failed."}), 500
        else:
            return jsonify({'success': False, 'message': "Failed to add Game."}), 500

    except ValueError as e:
        return jsonify({'success': False, 'message': f"System Error: {str(e)}"}), 400

@app.route('/add_publisher', methods=['POST'])
def add_publisher():
    try:
        name = request.form.get('publisher_name')
        country = request.form.get('country', '')
        year_val = request.form.get('year_established')
        year = int(year_val) if year_val else 0

        if not name:
             return jsonify({'success': False, 'message': "Error: Publisher Name is required."}), 400

        success = add_new_publisher(name, country, year)

        if success:
            return jsonify({'success': True, 'message': f"Publisher '{name}' added successfully!"})
        else:
            return jsonify({'success': False, 'message': "Database Error: Could not add publisher."}), 500

    except ValueError:
        return jsonify({'success': False, 'message': "Error: Year must be a valid number."}), 400


@app.route('/add_platform', methods=['POST'])
def add_platform():
    try:
        name = request.form.get('platform_name')
        manufacturer = request.form.get('manufacturer', '')
        
        year_val = request.form.get('release_year')
        year = int(year_val) if year_val else 0

        if not name:
             return jsonify({'success': False, 'message': "Error: Platform Name is required."}), 400

        success = add_new_platform(name, manufacturer, year)

        if success:
            return jsonify({'success': True, 'message': f"Platform '{name}' added successfully!"})
        else:
            return jsonify({'success': False, 'message': "Database Error: Could not add platform."}), 500

    except ValueError:
        return jsonify({'success': False, 'message': "Error: Year must be a valid number."}), 400


@app.route('/add_genre', methods=['POST'])
def add_genre():
    try:
        name = request.form.get('genre_name')
        description = request.form.get('description', '')
        example = request.form.get('example_game', '')

        if not name:
             return jsonify({'success': False, 'message': "Error: Genre Name is required."}), 400

        success = add_new_genre(name, description, example)

        if success:
            return jsonify({'success': True, 'message': f"Genre '{name}' added successfully!"})
        else:
            return jsonify({'success': False, 'message': "Database Error: Could not add genre."}), 500

    except Exception as e:
        return jsonify({'success': False, 'message': f"System Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)