# -*- coding: utf-8 -*-
from flask import Flask, jsonify, Response, request

from model.game_manager import GameManager
from utils.exception import InvalidNbPlayer
from utils.run_server_utils import jsonifyException, jsonifyErrorMessage
import json
from json.decoder import JSONDecodeError
from model.token_array import TokenArray

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
    except ValueError:
        return jsonifyErrorMessage("nb_player query param is not a integer. The given value was '" + request.args['nb_player'] + "."), 400
    except KeyError:
        return jsonifyErrorMessage("No nb_player query param was given"), 400
    except InvalidNbPlayer as err:
        return jsonifyException(err), 400

    while gameManager.currentPlayer != gameManager.userId:
        if (err := gameManager.cpu_turn()) is not None:
            return jsonifyException('cpu turn problem : ' + str(err)), 400
    response = jsonify(gameManager.gather_api_board_state())
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    return response


@app.route('/api/buy_card', methods=['GET'])
def buyCard() -> Response:
    """API route to buy a card

    Query params:
        cardId (int): id of the card to buy

    Returns:
        An error message with the HTTP status 400 is returned in the following cases:
        - no cardId query param was given
        - the cardId query param is not an integer
        - an exception happens when buying the card
        Otherwise, the board state of the game with the HTTP status 200 is returned.
    """

    try:
        cardId = int(request.args['card_id'])
    except ValueError:
        return jsonifyErrorMessage("cardId query param is not a integer. The given value was '" + request.args['cardId'] + "."), 400
    except KeyError:
        return jsonifyErrorMessage("No cardId query param was given"), 400

    if (err := gameManager.buy_card(cardId)):
        return jsonifyException(err), 400

    while gameManager.currentPlayer != gameManager.userId:
        if (err := gameManager.cpu_turn()) is not None:
            return jsonifyException('cpu turn problem : ' + str(err)), 400
    response = jsonify(gameManager.gather_api_board_state())
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    return response


@app.route('/api/reserve_card', methods=['GET'])
def reserveCard():
    """API route to reserve a visible card

    Query params:
        cardId (int): id of the card to reserve

    Returns:
        An error message with the HTTP status 400 is returned in the following cases:
        - no cardId query param was given
        - the cardId query param is not an integer
        - an exception happens when reserving the card
        Otherwise, the board state of the game with the HTTP status 200 is returned.
    """
    try:
        cardId = int(request.args['cardId'])
    except ValueError:
        return jsonifyErrorMessage("cardId query param is not a integer. The given value was " + request.args['cardId'] + "."), 400
    except KeyError:
        return jsonifyErrorMessage("No cardId query param was given"), 400

    if (err := gameManager.reserve_card(cardId)):
        return jsonifyException(err), 400

    while gameManager.currentPlayer != gameManager.userId:
        if (err := gameManager.cpu_turn()) is not None:
            return jsonifyException('cpu turn problem : ' + str(err)), 400
    response = jsonify(gameManager.gather_api_board_state())
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    return response


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
    except ValueError:
        return jsonifyErrorMessage("deck_level query param is not a integer. The given value was " + request.args['deck_level'] + "."), 400
    except KeyError:
        return jsonifyErrorMessage("No deck_level query param was given"), 400

    if (err := gameManager.reserve_pile_card(deckLevel)):
        return jsonifyException(err), 400

    while gameManager.currentPlayer != gameManager.userId:
        if (err := gameManager.cpu_turn()) is not None:
            return jsonifyException('cpu turn problem : ' + str(err)), 400
    response = jsonify(gameManager.gather_api_board_state())
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    return response


@app.route('/api/take_tokens', methods=['GET'])
def takeTokens():
    """API route to take 2 tokens of the same colour or 3 tokens of different colours.

    Query params:
        token_list (list[int]):
            list of ints that correspond to the number of taken tokens per colour.
            The format of the list should be [numberOfWhiteTokens, numberOfBlueTokens, numberOfGreenTokens, numberOfRedTokens, numberOfBlackTokens, numberOfGoldTokens]

    Returns:
        An error message with the HTTP status 400 is returned in the following cases:
        - no token_list query param was given
        - the token_list query param is not a list of 6 ints
        - an exception happens when taking the tokens
        Otherwise, the board state of the game with the HTTP status 200 is returned.
    """

    try:
        tokensString = request.args['token_list']
    except KeyError:
        return jsonifyErrorMessage("No token_list query param was given"), 400

    # The following code is used to check that the given token_list query param is a list of 6 ints
    jsonifiedIntListErrorMessageWith400HttpStats: Response = jsonifyErrorMessage(
        "It was not possible to convert the token_list query params into a list of ints. The given value was " + tokensString + "."), 400
    try:
        tokens = json.loads(tokensString)
    except JSONDecodeError:
        return jsonifiedIntListErrorMessageWith400HttpStats

    if type(tokens) is not list:
        return jsonifiedIntListErrorMessageWith400HttpStats

    if len(tokens) != 6:
        return jsonifyErrorMessage("The length of the tokens list is incorrect. It should be 6 but it is " + str(len(tokens)) + ". The given token_list query param value was " + tokensString + "."), 400

    for value in tokens:
        if type(value) is not int:
            return jsonifiedIntListErrorMessageWith400HttpStats

    if (err := gameManager.take_token(TokenArray(tokens))):
        return jsonifyException(err), 400

    while gameManager.currentPlayer != gameManager.userId:
        if (err := gameManager.cpu_turn()) is not None:
            return jsonifyException('cpu turn problem : ' + str(err)), 400
    response = jsonify(gameManager.gather_api_board_state())
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    return response


@app.route('/api/cpu_turn', methods=['GET'])
def cpuTurn():
    """API route to make a CPU play

    Returns:
        An error message with the HTTP status 400 is returned if an error happens during the turn of the cpu
        Otherwise, the board state of the game with the HTTP status 200 is returned.
    """
    if gameManager.currentPlayer == gameManager.userId:
        return jsonifyException('cpu turn called when it is human turn'), 400

    while gameManager.currentPlayer != gameManager.userId:
        if (err := gameManager.cpu_turn()) is not None:
            return jsonifyException('cpu turn problem : ' + str(err)), 400
    response = jsonify(gameManager.gather_api_board_state())
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    return response


if __name__ == "__main__":
    app.run(debug=True)
