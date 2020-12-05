'''Provide interface for game.'''

from typing import Union

from flask import Blueprint, render_template, request
from flask_login import current_user, login_required
# from flask_wtf import FlaskForm
from flask_sse import sse
from werkzeug.wrappers import Response
# from wtforms import StringField, SubmitField
# from wtforms.validators import DataRequired, EqualTo, Length, Regexp

# from spades import exceptions
from spades.game import Game
from spades.models.player import Player

main = Blueprint('main', __name__)
# Game.player_max = 2
game = Game()


# class PlayForm(FlaskForm):
#     username: StringField = StringField(
#         'Play',
#         validators=[
#             DataRequired(),
#             Length(min=4, max=25),
#             Regexp('^[a-zA-Z][a-zA-Z0-9._]+[a-zA-Z0-9]$')
#         ]
#     )
#     # submit: SubmitField = SubmitField('Signin')


@main.route('/')
def index() -> str:
    '''Provide start page.'''
    return render_template('index.html')


@main.route('/lobby')
@login_required
def lobby() -> str:
    '''Check resource.'''
    return render_template('lobby.html')


@main.route('/play', methods=['POST'])
@login_required
def play():
    print('playing a card')
    user = request.form['user']
    rank = request.form['rank']
    suit = request.form['suit']
    card_played = {'user': user, 'rank': rank, 'suit': suit}
    sse.publish(card_played, type='play-card')
    return card_played


@main.route('/gameboard')
@login_required
def gameboard() -> Union[Response, str]:
    '''Provide gameboard.'''
    # Setup mock players - less than four fail
    for player in ['John', 'Edgar', 'Jill']:
        if not game.get_player_by_username(player):
            game.add_player(Player(player))
    # mock end

    player = game.get_player_by_username(current_user.username)
    if not player:
        game.add_player(Player(current_user.username))
        player = game.get_player_by_username(current_user.username)
        print(
            f"{game.get_player_by_username(current_user.username).username}"
        )

    print('players', game.players)
    if game.check_player_count():
        if game.state == 'waiting':
            game.start_game()
            print('starting game', game.state)
        elif game.state == 'bidding':
            print('cards', player.hand.to_json)
            print('accepting bids')
        elif game.state == 'playing':
            print('playing game')
        elif game.state == 'cleanup':
            print('clean up match')

    players = [
        {
            'name': 'test',
            'seat': 'main',
            'active': 'true',
            'hand': player.hand.to_json
        }, {
            'name': 'John',
            'seat': 'left',
            'active': 'false',
            'card_count': 13
        }, {
            'name': 'Edgar',
            'seat': 'across',
            'active': 'false',
            'card_count': 13
        }, {
            'name': 'Jill',
            'seat': 'right',
            'active': 'false',
            'card_count': 13
        },
    ]
    if hasattr(player, 'hand'):
        print('hand')
        return render_template('gameboard.html', data=players)
    else:
        print('no hand')
        return render_template('gameboard.html')
