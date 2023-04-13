# -*- coding: utf-8 -*-
from flask import Flask, render_template, jsonify
import json
import requests

from model.game_manager import GameManager

app = Flask(__name__)
gameManager: GameManager = GameManager(4)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('front/index.html')


@app.route('/api/launchGame')
def launchGame():
    gameManager = GameManager()
    return jsonify(gameManager.gather_board_state())


@app.route('/api/buyCard')
def buyCard():
    pass
    return jsonify(gameManager.gather_board_state())


@app.route('/api/reserveCard')
def reserveCard():
    pass
    return jsonify(gameManager.gather_board_state())


@app.route('/api/reserveCardOnPile')
def reserveCardOnPile():
    pass
    return jsonify(gameManager.gather_board_state())


@app.route('/api/takeToken')
def takeToken():
    pass
    return jsonify(gameManager.gather_board_state())


@app.route('/api/cpuTurn')
def cpuTurn():
    pass
    return jsonify(gameManager.gather_board_state())




if __name__ == "__main__":
    app.run(debug=True)
