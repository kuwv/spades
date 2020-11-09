'''Provide game capabilities.'''

from typing import List

from transitions import Machine

from .book import Book
from .deck import Deck
from .exceptions import MaxPlayersException, NoPlayersException
from .player import Hand, Player


class Game:
    '''Provide game object.'''

    player_max = 4
    player_min = 2

    states = [
        'new_game',
        'new_match',
        'make_bid',
        'player_turn',
        'waiting',
        'end_turn',
        'end_match',
        'end_game'
    ]

    transitions = [
        {'trigger': 'new_game', 'source': 'end_game', 'dest': 'new_match'},
    ]

    def __init__(
        self,
        starting_player: int = None,
    ) -> None:
        '''Initialize game.'''
        self.turn: int = 0
        self.deck: Deck = Deck()
        self.__players: List[Player] = []

        self._machine = Machine(
            model=self,
            states=Game.states,
            transitions=Game.transitions,
            initial='new_game'
        )

    @property
    def player_count(self) -> int:
        return len(self.__players)

    @property
    def current_player(self) -> Player:
        '''Get current player.'''
        return self.__players[self.turn % len(self.__players)]

    def deal(self) -> None:
        if self.player_count > 0:
            card_piles: List[Hand] = []
            for hand in range(0, self.player_count):
                card_piles.append(Hand())

            turn = 0
            for card in self.deck:
                card_piles[self.turn % len(card_piles)].add_card(card)
                turn += 1

            for player in self.__players:
                player.add_hand(card_piles.pop())
        else:
            raise NoPlayersException('no players in game')

    def add_book(self, book: Book) -> None:
        # self.books.append(book)
        pass

    def add_player(self, player: Player) -> None:
        '''Add player to game.'''
        if self.player_count < Game.player_max:
            self.__players.append(player)
        else:
            raise MaxPlayersException('max number of players')
