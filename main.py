from flask import Flask, render_template
import pandas as pd
from games_data import GamesData
from web_processor import WebProcessor

# ZMIANA USTAWIEŃ PODGLĄDU W EDYTORZE
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 300)

# INICJALIZACJA APLIKACJI
app = Flask(__name__)

# POBRANIE DANYCH
processor = WebProcessor()

# ŚCIEŻKI STRONY - FLASK
@app.route('/')
def generate_search_list():
    players = processor.generate_search_list()
    return render_template('index.html', players=players)

@app.route('/player')
def send_games_to_js():
    return processor.send_games_to_js()

app.run(debug=True)
