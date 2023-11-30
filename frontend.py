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

        user = request.cookies.get('user')
        if(user == None):
            user = str(len(games))
            response.set_cookie('user', user)
            games.append(Game())

        user = int(user)

        while(len(games) < user + 1):
            games.append(Game())
        
        game = games[user]
        response.response = json.dumps({
            'attack_ready': game.get_attack_ready(),
            'black_money': game.get_black_money(),
            'black_research': game.get_black_research(),
            'bless': game.get_bless(),
            'cities': game.get_cities(),
            'economy_phase': game.get_economy_phase(),
            'move_ready': game.get_move_ready(),
            'piece_health': game.get_piece_health(),
            'pieces': game.get_pieces(),
            'player_to_move': game.get_player_to_move(),
            'white_money': game.get_white_money(),
            'white_research': game.get_white_research()
        })
        
        return response
    elif(request.method == 'POST'):
        return 'post_test'