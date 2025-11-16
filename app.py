from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return "Merhaba! Flask web sitemiz çalışıyor."

if __name__ == '__main__':
    app.run(debug=True)