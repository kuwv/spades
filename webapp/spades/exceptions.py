# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Provide book package.'''


class GameException(Exception):
    '''Provide exception on game errors.'''


class MaxPlayersException(GameException):
    '''Provide exception on maximum players in game.'''


class MaxHandSizeException(GameException):
    '''Provide exception on maximum hand size.'''


class EmptyHandSizeException(GameException):
    '''Provide exception on empty player hand.'''


class NoPlayersException(GameException):
    '''Provide exception on no players in game.'''


class InvalidComparisonCardException(GameException):
    '''Provide exception on invalid card comparison.'''


class InvalidRankCardException(GameException):
    '''Provide exception on invalid card rank.'''


class InvalidSuitCardException(GameException):
    '''Provide exception on invalid card suit.'''


class MaxCardBookException(GameException):
    '''Provide exception on maximum cards in book.'''
