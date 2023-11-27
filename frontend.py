from game import Game

from flask import Flask, send_file, send_from_directory, request

app = Flask(__name__, static_url_path='', static_folder='static')

@app.route('/', methods = [
    'GET'
])
def index():
    return send_file('./views/index.html')

@app.route('/game', methods = [
    'GET'
])
def game():
    return send_file('./views/game.html')

@app.route('/game/status', methods = [
    'GET',
    'POST'
])
def status():
    if(request.method == 'GET'):
        return 'get_test'
    elif(request.method == 'POST'):
        return 'post_test'