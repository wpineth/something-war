from game import Game

from flask import Flask, send_file, send_from_directory, request, make_response, json

from ai_agent import AIAgent

adversary = AIAgent

games = []
agents = []

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
    response = make_response()

    user = request.cookies.get('user')
    if(user == None):
        user = str(len(games))
        response.set_cookie('user', user)
        games.append(Game())
        agents.append(adversary())

    user = int(user)

    while(len(games) < user + 1):
        games.append(Game())
        agents.append(adversary())
    
    game = games[user]
    agent = agents[user]

    if(request.method == 'POST'):
        try:
            if 't1' in request.json:
                if type(request.json['t1']) is list:
                    game.take_action(game.infer_action(tuple(request.json['t1']), tuple(request.json['t2'])))
                else:
                    #create
                    game.take_action(Game.Action(Game.Action.TYPE_PLACE, tuple(request.json['t2']), None, request.json['t1']))
                    pass
            else:
                #research
                if 'research' in request.json and request.json['research'] != None:
                    game.take_action(Game.Action(Game.Action.TYPE_RESEARCH, None, None, request.json['research']))
                    game.take_action(Game.Action(Game.Action.TYPE_END_TURN, None, None, None))
                    while game.get_player_to_move() == -1:
                        game.take_action(agent.decide_action(game))
                elif 'economy_phase' in request.json:
                    game.take_action(Game.Action(Game.Action.TYPE_ECONOMY, None, None, None))
                else:
                    game.take_action(Game.Action(Game.Action.TYPE_END_TURN, None, None, None))
                    while game.get_player_to_move() == -1:
                        game.take_action(agent.decide_action(game))
        except Exception as e:
            print(e)
        
    response.response = json.dumps({
        'max_health': game._M_MAP,
        'attack': game._A_MAP,
        'retaliation': game._R_MAP,
        'cost': game._C_MAP,
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