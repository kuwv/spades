'''provide player features.'''

from typing import List, Optional

from .card import Card


class Player:
    '''provide player object.'''

    def __init__(self, hand: List[Card]) -> None:
        self.tricks: List = []
        self.hand: List[Card] = []
        self.__bid: Optional[int] = None

    @property
    def bid(self) -> Optional[int]:
        return self.__bid

    @bid.setter
    def bid(self, bid) -> None:
        if self.__bid is None:
            self.__bid = bid

    def play(self, card: Card):
        pass

    def add_trick(self, book):
        self.tricks.append(book)
