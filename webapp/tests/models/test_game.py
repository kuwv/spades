# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Provide tests for game.'''

from spades.game import Game
from spades.player import Player


def test_game() -> None:
    '''Test game.'''
    game = Game()
    assert game.state == 'waiting'  # type: ignore
    game.add_player(Player('Jim'))
    game.add_player(Player('Mike'))
    game.add_player(Player('Jill'))
    game.add_player(Player('Kim'))
    game.start_game()  # type: ignore
    assert game.state == 'bidding'  # type: ignore


def test_game_illegal_player() -> None:
    pass
