# -*- coding: utf-8 -*-
# type: ignore
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Provide tests for game.'''

import pytest

from spades import exceptions
from spades.game import Game
from spades.player import Player


@pytest.fixture(name='game')
def setup_game() -> Game:
    game = Game()
    game.add_player(Player('Jim'))
    game.add_player(Player('Mike'))
    game.add_player(Player('Jill'))
    game.add_player(Player('Kim'))
    return game


def test_game_states(game: Game) -> None:
    '''Test game states.'''

    # start the game from waiting state
    assert game.state == 'waiting'
    game.start_game()

    # start accepting bids
    assert game.state == 'bidding'

    # player 1 bid
    p1_turn = game.current_bidder()
    game.take_bid(p1_turn, 4)
    assert game.get_player(p1_turn).bid == 4

    # player 2 bid
    p2_turn = game.current_bidder()
    game.take_bid(p2_turn, 2)
    assert game.get_player(p2_turn).bid == 2

    # player 3 bid
    p3_turn = game.current_bidder()
    game.take_bid(p3_turn, 3)
    assert game.get_player(p3_turn).bid == 3

    # ensure last bidder is accounted for
    game.start_turn()
    assert game.state == 'bidding'

    # player 4 bid
    p4_turn = game.current_bidder()
    game.take_bid(p4_turn, 2)
    assert game.get_player(p4_turn).bid == 2

    # check that no other bid can be made
    with pytest.raises(exceptions.IllegalBidException):
        game.take_bid(game.current_bidder(), 2)

    # Start player turns
    game.start_turn()
    assert game.state == 'playing'

    p1_turn = game.current_leader
    print(p1_turn)
    # print([c for c in game.get_player(p1_turn).hand])
    print(game.get_player(p1_turn).hand)

    # End player turns
    game.end_turn()
    assert game.state == 'cleanup'


def test_game_illegal_player(game: Game) -> None:
    '''Test adding over maximum number of players.'''
    with pytest.raises(exceptions.MaxPlayerException):
        game.add_player(Player('Jackson'))
