# app.py

from flask import Flask, request, render_template
from db_utils.db_connector import add_new_game # Yeni fonksiyonu içe aktar

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