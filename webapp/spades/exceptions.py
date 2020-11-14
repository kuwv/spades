# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Provide book package.'''


class GameException(Exception):
    '''Provide exception on game errors.'''


class IllegalTurnException(GameException):
    '''Provide exception on unavailable command during phase.'''


class IllegalDeckException(GameException):
    '''Provide exception on dealing deck during current game.'''


class IllegalPlayerException(GameException):
    '''Provide exception on adding players during game.'''


class IllegalBidException(GameException):
    '''Provide exception on bids made out of turn.'''


class IllegalPlayException(GameException):
    '''Provide exception on plays made against rules.'''


class NoPlayerException(GameException):
    '''Provide exception on no players in game.'''


class MaxPlayerException(GameException):
    '''Provide exception on maximum players in game.'''


class MaxHandSizeException(GameException):
    '''Provide exception on maximum hand size.'''


class EmptyHandSizeException(GameException):
    '''Provide exception on empty player hand.'''


class InvalidComparisonCardException(GameException):
    '''Provide exception on invalid card comparison.'''


class InvalidRankCardException(GameException):
    '''Provide exception on invalid card rank.'''


class InvalidSuitCardException(GameException):
    '''Provide exception on invalid card suit.'''


class MaxBookSizeException(GameException):
    '''Provide exception on maximum cards in book.'''
