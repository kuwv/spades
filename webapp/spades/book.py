# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Provide book package.'''

from typing import List, Optional

from spades.card import Card
from spades.exceptions import MaxBookSizeException


class Book:
    '''Provide book object.'''

    card_max = 4

    def __init__(self, card_max: Optional[int] = None) -> None:
        '''Initialize book.'''
        if card_max:
            Book.card_max = card_max
        self.__cards: List[Card] = []
        self.__high_card: Optional[Card] = None

    def __repr__(self) -> str:
        '''Return string representation of book.'''
        return (
            f"{self.__class__.__name__}(cards={self.__cards!r})"
        )

    def __len__(self) -> int:
        '''Return length of book.'''
        return len(self.__cards)

    def __contains__(self, card: Card) -> bool:
        '''Check if book conatins card.'''
        return True if card in self.__cards else False

    @property
    def high_card(self) -> Optional[Card]:
        '''Get current high card.'''
        return self.__high_card

    def add_card(self, card: Card) -> None:
        '''Add card to book.'''
        if len(self.__cards) < Book.card_max:
            if self.__high_card:
                if self.__high_card < card:
                    self.__high_card = card
            else:
                self.__high_card = card
            self.__cards.append(card)
        else:
            raise MaxBookSizeException('max book size')
