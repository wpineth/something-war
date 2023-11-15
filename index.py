from flask import Flask, send_file, send_from_directory

app = Flask(__name__, static_url_path='', static_folder='static')

@app.route('/')
def index():
    return send_file('./views/index.html')

@app.route('/game')
def game():
    return send_file('./views/game.html')