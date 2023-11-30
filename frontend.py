from game import Game

from flask import Flask, send_file, send_from_directory, request, make_response, json

games = []

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
        response = make_response()

        if(request.cookies.get('user') == None):
            response.set_cookie('user', str(len(games)))
            games.append(Game())
        
        user = int(request.cookies.get('user'))

        while(len(games) < user + 1):
            games.append(Game())
        
        response.response = games[int(request.cookies.get('user'))].stringify_board()
        
        return response
    elif(request.method == 'POST'):
        return 'post_test'