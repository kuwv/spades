'''Provide interface for game.'''

from typing import List, Union

import flask
from flask import Blueprint, url_for
from flask_login import current_user, login_required
from flask_wtf import FlaskForm
from flask_sse import sse
from werkzeug.wrappers import Response
from wtforms import SubmitField
# from wtforms.validators import DataRequired, EqualTo, Length, Regexp

# from spades import exceptions
from spades.game import Game
from spades.models.player import Player

main = Blueprint('main', __name__)

mock_names: List[str] = ['John']
games: List[Game] = []
game = Game()


class LobbyForm(FlaskForm):
    start_game: SubmitField = SubmitField('start game')
    join_game: SubmitField = SubmitField('join game')


def __create_game() -> None:
    '''Create a new game.'''
    print('no game found - creating one')
    game = Game()
    games.append(game.add_player(Player(current_user.username)))


@main.route('/')
def index() -> str:
    '''Provide start page.'''
    return flask.render_template('index.html')


@main.route('/lobby', methods=['GET', 'POST'])
@login_required
def lobby() -> str:
    '''Provide lobby to coordinate new games.'''
    form = LobbyForm()
    if form.validate_on_submit():
        if form.join_game.data:
            print('join game')
            for game in games:
                if hasattr(game, 'state') and game.state == 'waiting':
                    if not game.get_player_by_username(current_user.username):
                        game.add_player(Player(current_user.username))
                        if game.check_player_count():
                            game.start_game()
                        break
                else:
                    __create_game()
            return flask.redirect(url_for('main.gameboard'))
        if form.start_game.data:
            print('start game')
            __create_game()
    print('games', games)
    if games != []:
        return flask.render_template('lobby.html', form=form, games=mock_names)
    return flask.render_template('lobby.html', form=form)


@main.route('/play', methods=['POST'])
@login_required
def play():
    '''Publish card play for user.'''
    username = flask.request.form['username']
    rank = flask.request.form['rank']
    suit = flask.request.form['suit']
    card_played = {'username': username, 'rank': rank, 'suit': suit}
    # TODO: submit card to game
    sse.publish(card_played, type='play-card')
    return card_played


@main.route('/gameboard')
@login_required
def gameboard() -> Union[Response, str]:
    '''Provide gameboard.'''
    # Setup mock players - less than four fail
    for player in mock_names:
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
            'username': 'test',
            'active': 'true',
            'hand': player.hand.to_json
        }, {
            'username': 'John',
            'active': 'false',
            'card_count': 13
        },
    ]
    if hasattr(player, 'hand'):
        print('hand')
        return flask.render_template('gameboard.html', data=players)
    else:
        print('no hand')
        return flask.render_template('gameboard.html')
