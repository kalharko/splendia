# -*- coding: utf-8 -*-
from flask import Flask, jsonify, Response, request

from model.game_manager import GameManager
from utils.exception import InvalidNbPlayer
from utils.run_server_utils import jsonifyException, jsonifyErrorMessage
from typing import List

app = Flask(__name__)
gameManager: GameManager = GameManager(4)


@app.route('/api/launch_game', methods=['GET'])
def launchGame() -> Response:
    """API route to launch a new game

    Query params:
        nb_player (int): number of players for the game

    Returns:
        Response:
            An error message with the HTTP status 400 is returned in the following cases:
            - no nb_player query param was given
            - the nb_player query param is not an integer
            - an invalid number of players is given
            Otherwise, the board state of the game with the HTTP status 200 is returned.
        
    """
    try:
        gameManager.launch_game(int(request.args['nb_player']))
    except ValueError as err:
        return jsonifyErrorMessage("nb_player query param is not a integer. The given value was '" + request.args['nb_player'] + "'"), 400
    except KeyError as err:
        return jsonifyErrorMessage("No nb_player query param was given"), 400
    except InvalidNbPlayer as err:
        return jsonifyException(err), 400

    return jsonify(gameManager.gather_api_board_state())


@app.route('/api/buy_card', methods=['GET'])
def buyCard() -> Response:
    """API route to buy a card

    Query params:
        card_id (int): id of the card to buy

    Returns:
        An error message with the HTTP status 400 is returned in the following cases:
        - no card_id query param was given
        - the card_id query param is not an integer
        - an exception happens when buying the card
        Otherwise, the board state of the game with the HTTP status 200 is returned.
    """
    try:
        cardId = int(request.args['card_id'])
    except ValueError as err:
        return jsonifyErrorMessage("card_id query param is not a integer. The given value was '" + request.args['card_id'] + "'"), 400
    except KeyError as err:
        return jsonifyErrorMessage("No card_id query param was given"), 400
    
    if(err := gameManager.buy_card(cardId)):
        return jsonifyException(err), 400
    
    return jsonify(gameManager.gather_api_board_state())


@app.route('/api/reserve_card', methods=['GET'])
def reserveCard():
    """API route to reserve a visible card

    Query params:
        card_id (int): id of the card to reserve

    Returns:
        An error message with the HTTP status 400 is returned in the following cases:
        - no card_id query param was given
        - the card_id query param is not an integer
        - an exception happens when reserving the card
        Otherwise, the board state of the game with the HTTP status 200 is returned.
    """
    try:
        cardId = int(request.args['card_id'])
    except ValueError as err:
        return jsonifyErrorMessage("card_id query param is not a integer. The given value was '" + request.args['card_id'] + "'"), 400
    except KeyError as err:
        return jsonifyErrorMessage("No card_id query param was given"), 400
    
    if(err := gameManager.reserve_card(cardId)):
        return jsonifyException(err), 400
    
    return jsonify(gameManager.gather_api_board_state())


@app.route('/api/reserve_card_on_pile', methods=['GET'])
def reserveCardOnPile():
    """API route to reserve the top card of one of the piles

    Query params:
        deck_level (int): level of the pile to reserve the card from

    Returns:
        An error message with the HTTP status 400 is returned in the following cases:
        - no deck_level query param was given
        - the deck_level query param is not an integer
        - an exception happens when reserving the card
        Otherwise, the board state of the game with the HTTP status 200 is returned.
    """
    try:
        deckLevel = int(request.args['deck_level'])
    except ValueError as err:
        return jsonifyErrorMessage("deck_level query param is not a integer. The given value was '" + request.args['deck_level'] + "'"), 400
    except KeyError as err:
        return jsonifyErrorMessage("No deck_level query param was given"), 400
    
    if(err := gameManager.reserve_pile_card(deckLevel)):
        return jsonifyException(err), 400
    
    return jsonify(gameManager.gather_api_board_state())


@app.route('/api/take_token', methods=['GET'])
def takeToken():
    pass
    return jsonify(gameManager.gather_api_board_state())


@app.route('/api/cpu_turn', methods=['GET'])
def cpuTurn():
    pass
    return jsonify(gameManager.gather_api_board_state())


if __name__ == "__main__":
    app.run(debug=True)
