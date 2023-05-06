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

@app.route('/api/launch_game', defaults={'nbPlayer': 4})
@app.route('/api/launch_game/<int:nbPlayer>')
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


@app.route('/api/buy_card/<int:cardId>')
def buyCard(cardId: int) -> Response:
    """API route to buy a card

    Args:
        cardId (int): id of the card to buy

    Returns:
        Response: If an exception happens when buying the card, a response containing an error message with the HTTP status 400 is returned.
        Otherwise, the board state of the game with the HTTP status 200 is returned.
    """
    if(err := gameManager.buy_card(cardId)):
        return jsonifyException(err), 400
    
    return jsonify(gameManager.gather_api_board_state())


@app.route('/api/reserve_card/<int:cardId>')
def reserveCard(cardId: int=-1):
    """API route to reserve a visible card

    Args:
        cardId (int): id of the card to reserve

    Returns:
        Response: If an exception happens when reserving the card, a response containing an error message with the HTTP status 400 is returned.
        Otherwise, the board state of the game with the HTTP status 200 is returned.
    """
    if(err := gameManager.reserve_card(cardId)):
        return jsonifyException(err), 400
    
    return jsonify(gameManager.gather_api_board_state())


@app.route('/api/reserve_card_on_pile/<deckLevel>')
def reserveCardOnPile(deckLevel=-1):
    pass
    return jsonify(gameManager.gather_api_board_state())


@app.route('/api/take_token')
def takeToken():
    pass
    return jsonify(gameManager.gather_api_board_state())


@app.route('/api/cpu_turn')
def cpuTurn():
    pass
    return jsonify(gameManager.gather_api_board_state())


if __name__ == "__main__":
    app.run(debug=True)
