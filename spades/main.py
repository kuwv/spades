'''Provide interface for game.'''

from typing import Any, Dict, List, Optional, Union

import flask
from flask import Blueprint, url_for
from flask_login import current_user, login_required
from flask_wtf import FlaskForm
from flask_sse import sse
from werkzeug.wrappers import Response
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange

# from spades import exceptions
from spades.game import GameState
from spades.game.models.player import Player

main = Blueprint('main', __name__)

mock_names: List[str] = ['john']
__game: GameState = GameState()


class LobbyForm(FlaskForm):
    start_game: SubmitField = SubmitField('start game')
    join_game: SubmitField = SubmitField('join game')


class BidForm(FlaskForm):
    bid: IntegerField = IntegerField(
        'bid',
        validators=[
            DataRequired(),
            NumberRange(min=1, max=13)
        ]
    )
    submit: SubmitField = SubmitField('bid')


def get_player() -> Optional[Player]:
    player = __game.get_player_by_username(current_user.username)
    if not player:
        __game.add_player(Player(current_user.username))
        player = __game.get_player_by_username(current_user.username)
    return player


def get_turns(players: List[Player]) -> List[Dict[str, Any]]:
    player_turns: List[Dict[str, Any]] = []

    def is_active(turn: int) -> str:
        if __game.state != 'playing':  # type: ignore
            print('gamestate', False)
            return 'false'
        elif __game.current_turn != turn:
            print('turn:', __game.current_turn, turn)
            return 'false'
        else:
            print('active:', True)
            return 'true'

    for n, player in enumerate(players):
        inst = {
            'username': player.username,
            'active': is_active(n)
        }
        if player.username == current_user.username:
            inst['hand'] = player.hand.to_json  # type: ignore
        else:
            inst['card_count'] = len(player.hand)  # type: ignore
        player_turns.append(inst)
    print('player turns', player_turns)
    return player_turns


@main.route('/')
def index() -> str:
    '''Provide start page.'''
    return flask.render_template('index.html')


@main.route('/lobby', methods=['GET', 'POST'])
@login_required
def lobby() -> Union[Response, str]:
    '''Provide lobby to coordinate new games.'''
    form = LobbyForm()
    if form.validate_on_submit():
        if form.join_game.data:
            print('join game')
            if (
                hasattr(__game, 'state') and
                __game.state == 'waiting'  # type: ignore
            ):
                if not __game.get_player_by_username(
                    current_user.username
                ):
                    __game.add_player(Player(current_user.username))
                    if __game.check_player_count():
                        __game.start_game()  # type: ignore
            return flask.redirect(url_for('main.gameboard'))
    # if games != []:
    #     return flask.render_template(
    #         'lobby.html', form=form, games=mock_names
    #     )
    return flask.render_template('lobby.html', form=form)


@main.route('/play', methods=['POST'])
@login_required
def play() -> None:
    '''Publish card play for user.'''
    username = flask.request.form['username']
    rank = flask.request.form['rank']
    suit = flask.request.form['suit']
    card_played = {'username': username, 'rank': rank, 'suit': suit}
    # TODO: submit card to game
    print(
        'turn',
        __game.state,  # type: ignore
        __game.get_player_turn(username),
        __game.current_turn
    )
    __game.make_play(__game.get_player_turn(username), rank, suit)
    sse.publish(card_played, type='play-card')


@main.route('/bids', methods=['GET', 'POST'])
@login_required
def bids() -> Union[Response, str]:
    form = BidForm()
    if form.validate_on_submit():
        player_bid = flask.request.form['bid']
        __game.accept_bid(
            __game.get_player_turn(current_user.username),
            player_bid
        )
        __game.start_turn()  # type: ignore
        return flask.redirect(url_for('main.gameboard'))
    player = get_player()
    return flask.render_template(
        'bid.html', form=form, data=player.hand.to_json  # type: ignore
    )


@main.route('/gameboard')
@login_required
def gameboard() -> Union[Response, str]:
    '''Provide gameboard.'''
    # Setup mock players - less than four fail
    for player_name in mock_names:
        if not __game.get_player_by_username(player_name):
            __game.add_player(Player(player_name))
    # mock end

    players = []
    player = get_player()
    if __game.check_player_count():
        if __game.state == 'waiting':  # type: ignore
            __game.start_game()
            print('starting game', __game.state)
        if __game.state == 'bidding':  # type: ignore
            print('cards', player.hand.to_json)
            print('accepting bids')
            # return flask.redirect(url_for('main.bids'))
        if __game.state == 'playing':  # type: ignore
            print('playing game')
        if __game.state == 'cleanup':  # type: ignore
            print('clean up match')

    players = get_turns(__game.players)

    if hasattr(player, 'hand'):
        print('hand')
        return flask.render_template(
            'gameboard.html', state=__game.state, data=players  # type: ignore
        )
    else:
        print('no hand')
        return flask.render_template('gameboard.html')
