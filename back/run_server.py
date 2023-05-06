# -*- coding: utf-8 -*-
from flask import Flask, render_template, jsonify, Response

from model.game_manager import GameManager
from utils.exception import InvalidNbPlayer
from utils.run_server_utils import jsonifyException

app = Flask(__name__)
gameManager: GameManager = GameManager(4)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('front/splendia/src/index.html')

@app.route('/api/launchGame', defaults={'nbPlayer': 4})
@app.route('/api/launchGame/<int:nbPlayer>')
def launchGame(nbPlayer: int) -> Response:
    """API route to launch a new game

    Args:
        nbPlayer (int): number of players for the game

    Returns:
        Response: 
            If an invalid number of players is given, a response containing an error message with the HTTP status 403 is returned.
            Otherwise, the board state of the game with the HTTP status 200 is returned.
        
    """
    
    try:
        gameManager.launch_game(nbPlayer)
    except InvalidNbPlayer as err:
        return jsonifyException(err), 403 
    
    return jsonify(gameManager.gather_api_board_state())


@app.route('/api/buyCard/<int:cardId>')
def buyCard(cardId: int):
    pass
    return jsonify(gameManager.gather_ia_board_state())


@app.route('/api/reserveCard/<cardId>')
def reserveCard(cardId=-1):
    pass
    return jsonify(gameManager.gather_ia_board_state())


@app.route('/api/reserveCardOnPile/<deckLevel>')
def reserveCardOnPile(deckLevel=-1):
    pass
    return jsonify(gameManager.gather_ia_board_state())


@app.route('/api/takeToken')
def takeToken():
    pass
    return jsonify(gameManager.gather_ia_board_state())


@app.route('/api/cpuTurn')
def cpuTurn():
    pass
    return jsonify(gameManager.gather_ia_board_state())


if __name__ == "__main__":
    app.run(debug=True)
