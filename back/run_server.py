# -*- coding: utf-8 -*-
from flask import Flask, render_template, jsonify

from model.business_model.game_manager import GameManager

app = Flask(__name__)
gameManager: GameManager = GameManager(4)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('front/splendia/src/index.html')

@app.route('/api/launchGame', defaults={'nbPlayer': 4})
@app.route('/api/launchGame/<int:nbPlayer>')
def launchGame(nbPlayer):
    gameManager = GameManager(nbPlayer)
    return jsonify(gameManager.gather_api_board_state())


@app.route('/api/buyCard/<cardId>')
def buyCard(cardId=-1):
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
