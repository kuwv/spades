'''Provide interface for game.'''

from flask import Blueprint, jsonify, render_template
from flask_login import login_required

main = Blueprint('main', __name__)


@main.route('/')
def index() -> str:
    return render_template('index.html')


@main.route('/protected')
@login_required
def protected() -> str:
    '''Check resource.'''
    print('protected')
    return jsonify('hello world')
