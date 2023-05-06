# -*- coding: utf-8 -*-
from flask import Flask, render_template, jsonify

from model.game_manager import GameManager

app = Flask(__name__)
gameManager: GameManager = GameManager(4)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('front/splendia/src/index.html')

@app.route('/api/launchGame', defaults={'nbPlayer': 4})
@app.route('/api/launchGame/<int:nbPlayer>')
def launchGame(nbPlayer):
    response = jsonify(gameManager.gather_ia_board_state())
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    return response


@app.route('/api/buyCard/<cardId>')
def buyCard(cardId=-1):
    response = jsonify(gameManager.gather_ia_board_state())
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    return response


@app.route('/api/reserveCard/<cardId>')
def reserveCard(cardId=-1):
    response = jsonify(gameManager.gather_ia_board_state())
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    return response


@app.route('/api/reserveCardOnPile/<deckLevel>')
def reserveCardOnPile(deckLevel=-1):
    response = jsonify(gameManager.gather_ia_board_state())
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    return response


@app.route('/api/takeToken')
def takeToken():
    response = jsonify(gameManager.gather_ia_board_state())
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    return response


@app.route('/api/cpuTurn')
def cpuTurn():
    response = jsonify(gameManager.gather_ia_board_state())
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    return response


if __name__ == "__main__":
    app.run(debug=True)
