from flask import Flask, request, render_template, jsonify
from flask_cors import CORS

from db_utils.db_connector import get_db_connection
from db_utils.data_access.data_fetch import fetch_table_data, search_all_tables, get_record_by_id
from db_utils.data_access.game_crud import add_new_game
from db_utils.data_access.sales_crud import add_new_sales
from db_utils.data_access.genre_crud import add_new_genre
from db_utils.data_access.platform_crud import add_new_platform
from db_utils.data_access.publisher_crud import add_new_publisher

app = Flask(__name__)
CORS(app)

# 1. Ana Sayfa (Welcome Page)
@app.route('/')
def index():
    return render_template('index.html')

# 2. Merkezi Form Gösterme Rotası (Tüm formlar için tek bir HTML)
@app.route('/add_entry')
def add_entry_page():
    # add_entry.html şablonu, JS ile hangi formun çizileceğini URL'den okuyacak.
    return render_template('add_entry.html')

# 3. Arama API'si
@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    term = request.args.get('term', '')
    if len(term) < 2:
        return jsonify([])
    results = search_all_tables(term, limit=5)
    return jsonify(results)

# 4. Detay ve API Rotaları (Aynı Kalır)
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
    data = get_record_by_id(table_name, record_id)
    if data:
        return jsonify(data)
    else:
        return jsonify({'error': 'Record not found'}), 404

@app.route('/table_view')
def table_view():
    return render_template('table_view.html')

@app.route('/api/get_data/<table_name>', methods=['GET'])
def get_data(table_name):
    # Get Existing Parameters (Keeping them as is)
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', default=100, type=int) # Your preference: 100
    sort_by = request.args.get('sort_by', default=None, type=str)
    sort_order = request.args.get('order', default='ASC', type=str)
    
    # Capture Search Parameter 
    search_query = request.args.get('search', default=None, type=str)
    
    # Calculate Offset 
    offset = (page - 1) * limit
    
    # Call Database Function
    data = fetch_table_data(
        table_name, 
        limit=limit, 
        offset=offset, 
        sort_by=sort_by, 
        sort_order=sort_order,
        search_query=search_query # <-- Passing the new search capability
    )
    
    return jsonify(data)

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

# 5. CREATE POST Endpoints
# -------------------------------------------------------------

@app.route('/add_game', methods=['POST'])
def add_game():
    try:
        pub_id_str = request.form.get('publisher_id', '')
        plat_id_str = request.form.get('platform_id', '')
        gen_id_str = request.form.get('genre_id', '')

        if not pub_id_str or not plat_id_str or not gen_id_str:
            return "Error: Please make sure to SELECT Publisher, Platform, and Genre from the dropdown list.", 400

        publisher_id = int(pub_id_str)
        platform_id = int(plat_id_str)
        genre_id = int(gen_id_str)

        name = request.form['game_name']
        
        try:
            year = int(request.form.get('game_year') or 0)
            rank = int(request.form.get('game_rank') or 0)
        except ValueError:
             return "Error: Year and Rank must be valid numbers.", 400

        new_game_id = add_new_game(name, year, rank, publisher_id, platform_id, genre_id)

        if new_game_id:
            na = float(request.form.get('na_sales') or 0)
            eu = float(request.form.get('eu_sales') or 0)
            jp = float(request.form.get('jp_sales') or 0)
            other = float(request.form.get('other_sales') or 0)
            
            global_sales = na + eu + jp + other
            
            sales_success = add_new_sales(new_game_id, na, eu, jp, other, global_sales)
            
            if sales_success:
                return "Game and Sales added successfully!"
            else:
                return "Game added, but Sales data failed to save.", 500
        else:
            return "Failed to add Game (Database Error).", 500

    except ValueError as e:
        return f"System Error: {str(e)}", 400

@app.route('/add_publisher', methods=['POST'])
def add_publisher():
    if request.method == 'POST':
        try:
            name = request.form['publisher_name']
            country = request.form['country']
            year = int(request.form['year_established'])
            
            success = add_new_publisher(name, country, year)
            
            if success:
                return "Yayıncı başarıyla eklendi!"
            else:
                return "Hata: Publisher eklenemedi.", 500
        except ValueError:
            return "Hata: Yıl bir sayı olmalıdır", 400

@app.route('/add_platform', methods=['POST'])
def add_platform():
    if request.method == 'POST':
        try:
            name = request.form['platform_name']
            manufacturer = request.form['manufacturer']
            year = int(request.form['release_year'])
            
            success = add_new_platform(name, manufacturer, year)
            
            if success:
                return "Platform başarıyla eklendi!"
            else:
                return "Hata: Platform eklenemedi.", 500
        except ValueError:
            return "ERROR: Yıl bir sayı olmalıdır.", 400

@app.route('/add_genre', methods=['POST'])
def add_genre():
    if request.method == 'POST':
        name = request.form['genre_name']
        description = request.form['description']
        example = request.form['example_game']
        
        success = add_new_genre(name, description, example)
        
        if success:
            return "Genre başarıyla eklendi!"
        else:
            return "Hata: Genre eklenemedi.", 500

if __name__ == '__main__':
    app.run(debug=True)