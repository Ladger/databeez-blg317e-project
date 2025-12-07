from flask import Flask, request, render_template, jsonify
from flask_cors import CORS

from db_utils.data_access.data_fetch import fetch_table_data
from db_utils.data_access.data_fetch import search_all_tables
from db_utils.data_access.data_fetch import get_record_by_id
from db_utils.data_access.game_crud import add_new_game
from db_utils.data_access.genre_crud import add_new_genre
from db_utils.data_access.platform_crud import add_new_platform
from db_utils.data_access.publisher_crud import add_new_publisher

app = Flask(__name__)
CORS(app)

# 1. YENİ ROTA: Welcome Page (Arama Çubuğu burada gösterilecek)
@app.route('/')
def index():
    return render_template('index.html')

# 2. Arama API'si (JavaScript buraya istek atacak)
@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    term = request.args.get('term', '')
    
    # 2 karakterden kısaysa boş dön (DB'yi yorma)
    if len(term) < 2:
        return jsonify([])

    # Veritabanında ara
    results = search_all_tables(term, limit=5)
    return jsonify(results)

# 3. YENİ ROTA: Detay Sayfası (Kullanıcı arama sonucuna tıkladığında yönlendirilir)
@app.route('/detailed_view/<entity_type>/<int:entity_id>')
def detailed_view(entity_type, entity_id):
    # Bu sayfada, entity_type'a (Game, Publisher vb.) göre
    # data_fetch.py'den ilgili detay çekme fonksiyonu çağrılmalıdır.
    
    # Örnek: if entity_type == 'Game': data = fetch_game_details(entity_id)
    
    # Şimdilik, sadece sayfayı render edelim
    context = {
        'entity_type': entity_type,
        'entity_id': entity_id,
        'title': f"{entity_type} Detay Sayfası (ID: {entity_id})"
    }
    return render_template('detailed_view.html', **context)

# Yeni Rota ekleyin:
@app.route('/api/get_record/<table_name>/<int:record_id>')
def api_get_record(table_name, record_id):
    data = get_record_by_id(table_name, record_id)
    if data:
        return jsonify(data)
    else:
        return jsonify({'error': 'Record not found'}), 404
    

@app.route('/table_view')
def table_view():
    # Sadece HTML şablonunu döndürür, veriyi JS ile /api/get_data/... üzerinden çeker
    return render_template('table_view.html')

@app.route('/api/get_data/<table_name>', methods=['GET'])
def get_data(table_name):
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', default=100, type=int)
    
    sort_by = request.args.get('sort_by', default=None, type=str)
    sort_order = request.args.get('order', default='ASC', type=str)

    offset = (page - 1) * limit

    data = fetch_table_data(
        table_name, 
        limit=limit, 
        offset=offset, 
        sort_by=sort_by, 
        sort_order=sort_order
    )    
    return jsonify(data)

# Örnek bir POST route'u (veri göndermek için)
@app.route('/add_game', methods=['GET', 'POST'])
def add_game():
    if request.method == 'POST':
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
        
    return render_template('add_game_form.html')

@app.route('/add_publisher', methods=['GET', 'POST'])
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

    return render_template('add_publisher_form.html')

@app.route('/add_platform', methods=['GET', 'POST'])
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

    return render_template('add_platform_form.html')

@app.route('/add_genre', methods=['GET', 'POST'])
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

    return render_template('add_genre_form.html')

if __name__ == '__main__':
    app.run(debug=True)