'''Provide game capabilities.'''

# from typing import List, Optional

from .deck import Deck
from .player import Hand, Player


class Rules:
    '''Provide game rules object.'''


class Game(Rules):
    '''Provide game object.'''

    player_max = 4
    player_min = 2

    def __init__(
        self,
        starting_player: int = None,
    ) -> None:
        '''Initialize game.'''
        self.turn = 0
        self.deck = Deck()
        self.players = []
        self.deal()

    @property
    def player_count(self):
        return len(self.__players)

    @player_count.setter
    def player_count(self, count):
        if not self.__player_count:
            self.__player_count = count

    @property
    def current_player(self):
        '''Get current player.'''
        return self.players[self.turn % len(self.players)]

    def deal(self):
        piles = []
        for hand in range(0, self.player_count):
            piles.append(Hand())

        turn = 0
        for card in self.deck:
            piles[self.turn % len(piles)].add_card(card)
            turn += 1

        for hand in piles:
            self.add_player(Player(hand))

    def add_book(self, book):
        self.books.append(book)

    def add_player(self, player: Player):
        if self.player_count < Game.player_max:
            self.players.append(player)
        else:
            print('except on max number of players')
