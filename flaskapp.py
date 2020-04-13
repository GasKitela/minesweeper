from flask import Flask, request
from sweeper import Game
import json
import uuid

app = Flask(__name__)

_games = {}

@app.route("/")
def hello():
    return 'Welcome to Minesweeper API by Gaston Kitela'

@app.route("/ms/new-game", methods=['POST'])
def gamestart():
    body = request.get_json()

    game_id = str(uuid.uuid1())
    new_game = Game(game_id, body.get("rows"), body.get("cols"), body.get("mines"))
    _games[game_id] = new_game

    return json.dumps(new_game.as_dict())

@app.route("/ms/<game_id>", methods=['GET'])
def get_game_in_progress(game_id):
    game = _games[game_id]
    return json.dumps(game.as_dict())

@app.route("/ms/<game_id>/click", methods=['PUT'])
def click_square(game_id):
    body = request.get_json()

    game = _games[game_id]
    game.click_square(body.get("rows"), body.get("cols"), body.get("action"))

    return json.dumps(game.as_dict())

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=4433)
