from flask import Flask, render_template, request
from sweeper import Game
import json

app = Flask(__name__, static_folder="/client")
_games = {}

@app.route("/")
def hello():
    return 'Hello World!'

#CAMBIAR A POST CON FORM
#CAMBIAR A: O GENERAR UN UUID, O DEJAR ELEGIR, PERO CHEQUEAR QUE NO SE REPITA
@app.route("/games/<game_id>/<rows>/<cols>/<mines>", methods=['POST'])
def gamestart(game_id, rows, cols, mines):
    print()
    gg = Game(game_id, int(rows), int(cols), int(mines))
    _games[game_id] = gg
    return json.dumps(gg.as_dict())

@app.route("/games/<game_id>", methods=['GET'])
def get_game_in_progress(game_id):
    game = _games[game_id]
    return json.dumps(game.as_dict())

@app.route("/games/<game_id>/click/<row>/<col>/<action>", methods=['PUT'])
def click_square(game_id, row, col, action):
    game = _games[game_id]
    game.click_square(int(row), int(col), action)
    return json.dumps(game.as_dict())

@app.route("/hola-mundo", methods=['GET'])
def hola_mundo():
    return 'hola mundo'


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=4433)
