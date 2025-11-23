# app.py

from flask import Flask, request, render_template
from db_utils.db_connector import (
    add_new_game, 
    add_new_publisher, 
    add_new_platform, 
    add_new_genre
)

app = Flask(__name__)

# Örnek bir POST route'u (veri göndermek için)
@app.route('/add_game', methods=['GET', 'POST'])
def add_game():
    if request.method == 'POST':
        # Formdan gelen verileri al
        name = request.form['game_name']
        year = request.form['game_year']
        rank = request.form['game_rank']  # Eksik Alan
        publisher_id = request.form['publisher_id'] # Eksik Alan
        platform_id = request.form['platform_id'] # Eksik Alan
        genre_id = request.form['genre_id'] # Eksik Alan
        
        # Veriyi veritabanına ekle
        success = add_new_game(name, year, rank, publisher_id, platform_id, genre_id) # Diğer parametreler buraya
        
        if success:
            return "Oyun başarıyla eklendi!"
        else:
            return "Hata: Oyun eklenemedi.", 500
            
    # GET isteğinde formu göster
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