# -*- coding: utf-8 -*-
# type: ignore
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Provide tests for game.'''

from random import randrange

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


def generate_bid(game: Game):
    turn = game.current_bidder()
    bid = randrange(0, 13)
    game.accept_bid(turn, bid)
    assert game.get_player(turn).bid == bid


def generate_trick(game: Game):
    turn = game.current_turn
    print('turn:', turn)
    player = game.get_player(turn)
    playable = player.hand.playable(game.stack.suit)
    card = [c for c in playable][0]
    game.play_trick(turn, card.rank, card.suit)
    # print('start hand:', game.get_player(turn).hand)


def test_game_states(game: Game) -> None:
    '''Test game states.'''

    # while not game.check_winner():

    # start the game from waiting state
    assert game.state == 'waiting'
    game.start_game()

    # start accepting bids
    assert game.state == 'bidding'

    # ensure all bidders have been accounted for
    game.start_turn()
    assert game.state != 'playing'

    for _ in [1, 2, 3, 4]:
        generate_bid(game)

    # check that no other bid can be made
    with pytest.raises(exceptions.IllegalBidException):
        game.accept_bid(game.current_bidder(), 2)

    while not game.check_handsize():
        # start player turns
        game.start_turn()
        assert game.state == 'playing'

        # check that all tricks have been accounted for
        game.end_turn()
        assert game.state != 'cleanup'

        for _ in [1, 2, 3, 4]:
            generate_trick(game)

        # TODO: fix exception test; pulls extra card
        # with pytest.raises(exceptions.MaxBookSizeException):
        #     generate_trick(game)

        # end turn
        game.end_turn()
        assert game.state == 'cleanup'

        # ensure match cannot be ended with cards in hand
        game.end_match()
        if not game.check_handsize():
            assert game.state != 'waiting'
        else:
            assert game.state == 'waiting'

# def test_game_illegal_player(game: Game) -> None:
#     '''Test adding over maximum number of players.'''
#     with pytest.raises(exceptions.MaxPlayerException):
#         game.add_player(Player('Jackson'))
