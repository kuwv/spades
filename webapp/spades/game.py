'''Provide game capabilities.'''

from random import randrange
from typing import List, Optional

from transitions import Machine

from spades import config
from spades import exceptions
from spades.bid import BidMixin
from spades.book import Book
# from spades.card import Card
from spades.deck import Deck
from spades.hand import Hand
from spades.player import Player, PlayerTurns


class Game(PlayerTurns, BidMixin):
    '''Provide game object.'''

    player_max = config.player_max
    winning_points = config.winning_points

    states = [
        'waiting',
        'bidding',
        'playing',
        'cleanup',
    ]

    transitions = [
        {
            'trigger': 'start_game',
            'source': 'waiting',
            'before': 'select_dealer',
            'after': 'setup_game',
            'dest': 'bidding',
            'conditions': 'check_player_count'
        }, {
            'trigger': 'start_turn',
            'source': ['bidding', 'cleanup'],
            'before': 'setup_turn',
            'dest': 'playing',
            'conditions': 'check_bids'
        }, {
            'trigger': 'end_turn',
            'after': 'cleanup_turn',
            'source': 'playing',
            'dest': 'cleanup'
        }, {
            'trigger': 'end_match',
            'source': 'cleanup',
            'dest': ['playing', 'waiting'],
            'conditions': 'check_match'
            # }, {
            #     'trigger': 'end_game',
            #     'source': '*',
            #     'dest': 'waiting',
            #     'conditions': 'check_winner'
        }
    ]

    def __init__(self) -> None:
        '''Initialize game.'''
        super().__init__()
        self.__dealer: Optional[int] = None
        self._bid_turn: int = 0
        self._starting_turn: Optional[int] = None
        self.deck: Deck = Deck()
        self.__book: Book = None

        self.machine = Machine(
            model=self,
            states=Game.states,
            transitions=Game.transitions,
            initial='waiting'
        )

    @property
    def dealer(self) -> Optional[int]:
        return self.__dealer

    def select_dealer(self) -> None:
        '''Randomly choose starting player.'''
        if self.player_count == Game.player_max:
            if not self.dealer:
                self.__dealer = randrange(self.player_count)
            else:
                self.__dealer = (self.dealer + 1) % self.player_count
        print('dealer:', self.dealer, self.players[self.dealer].name)

    def deal(self) -> None:
        '''Deal a new game.'''
        if self.state == 'bidding':  # type: ignore
            if self.player_count > 0:
                card_piles: List[Hand] = []
                for hand in range(0, self.player_count):
                    card_piles.append(Hand())
                turn = 0
                for card in self.deck:
                    card_piles[turn % len(card_piles)].add_card(card)
                    turn += 1
                for player in self.players:
                    player.hand = card_piles.pop()
            else:
                raise exceptions.NoPlayerException('no players in game')
        else:
            raise exceptions.IllegalDeckException(
                'cannot deal hand during active game'
            )

    def setup_game(self) -> None:
        '''Setup a new game of spades.'''
        self.deal()
        self.starting_turn = 0

    def add_player(self, player: Player) -> None:
        '''Add player to game.'''
        if self.state == 'waiting':  # type: ignore
            if self.player_count < Game.player_max:
                PlayerTurns.append_player(self, player)
            else:
                raise exceptions.MaxPlayerException(
                    'max number of players registered'
                )
        else:
            raise exceptions.IllegalPlayerException(
                'cannot add player active game'
            )

    def accept_card(self, player_id: str, rank: str, suit: str) -> bool:
        '''Move player card to book.'''
        if self.state == 'playing':
            # TODO: must compare user / turn
            player = self.get_player(player_id)
            if (
                len(self.__book) == 0 or
                suit == self.__book.suit or
                player.hand.list_suit(self.__book.suit) == 0
            ):
                self.__book.add_card(player_id, player.play_card(rank, suit))
            else:
                raise exceptions.IllegalPlayException(
                    'only cards of the same suit or spades may be played'
                )
            print('book', self.__book)
        else:
            raise exceptions.IllegalTurnException(
                'cannot play during this phase'
            )

    def award_book(self, player: Player, book: Book) -> None:
        '''Award book to player with trump or highest trick.'''
        if self.state == 'cleanup':
            pass
        else:
            raise exceptions.IllegalTurnException(
                'cannot award book during this phase'
            )

    # state checks

    def check_player_count(self) -> bool:
        return self.player_count == Game.player_max

    def setup_turn(self) -> None:
        if not self.__book:
            self.__book = Book()

        if not self.starting_turn:
            self.starting_turn = self.dealer
        else:
            self.starting_turn = (
                self.starting_turn + 1
            ) % self.player_count

    def cleanup_turn(self) -> None:
        self.__book = None

    def check_player_turn(self, player_id: str) -> bool:
        return player_id == self.players[player_id]

    def check_hands(self) -> bool:
        '''Check player hands.'''
        count = 0
        for player in self.players:
            if len(player.hand) == 0:
                count += 1
        return count == self.player_count

    def check_match(self) -> bool:
        '''Check if match is finished.'''
        if self.check_hands:
            for player in self.players:
                if len(player.hand) == 0:
                    return True
        return False

    def check_winner(self) -> bool:
        '''Check if number of points is a win.'''
        # for player in self.players:
        #     if player
        return False
