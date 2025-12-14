from flask import Flask, request, render_template, jsonify
from flask_cors import CORS

from db_utils.data_access.data_fetch import fetch_table_data, search_all_tables, get_record_by_id
from db_utils.data_access.game_crud import add_new_game
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

# 5. CREATE POST Endpoints (SADECE POST Metodu Kaldı)
# -------------------------------------------------------------

@app.route('/add_game', methods=['POST'])
def add_game():
    # Burası sadece form verisini işler. Form artık add_entry.html'den gelir.
    try:
        # Kritik: Sayısal değerleri int'e dönüştür ve hata yakalama bloğuna al
        name = request.form['game_name']
        year = int(request.form['game_year'])
        rank = int(request.form['game_rank']) 
        publisher_id = int(request.form['publisher_id']) 
        platform_id = int(request.form['platform_id']) 
        genre_id = int(request.form['genre_id']) 
        
        success = add_new_game(name, year, rank, publisher_id, platform_id, genre_id)
        
        if success:
            return "Oyun başarıyla eklendi!"
        else:
            return "Hata: Oyun eklenemedi (Veritabanı Hatası).", 500
    except ValueError:
        return "Hata: Yıl, Sıralama ve ID alanları geçerli sayılar olmalıdır.", 400
    
    # Not: GET metodu tamamen kaldırıldı.

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