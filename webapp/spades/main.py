'''Provide interface for game.'''

from typing import Union

from flask import Blueprint, jsonify, render_template
from flask_login import login_required
from werkzeug.wrappers import Response

from spades.game import Game

main = Blueprint('main', __name__)
game = Game()


@main.route('/')
def index() -> str:
    return render_template('index.html')


@main.route('/lobby')
@login_required
def lobby() -> str:
    '''Check resource.'''
    print('protected')
    return jsonify('hello world')


@main.route('/game')
@login_required
def game() -> Union[Response, str]:
    '''Provide game board.'''
    return render_template('game.html')
