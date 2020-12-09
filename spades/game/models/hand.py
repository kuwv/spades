# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Provide hand capabilities.'''

import json
from typing import List

# from flask import session

from spades import db, exceptions
from spades.game.models.card import Card, CardEncoder


cards = db.Table(
    'hand_of_cards',
    db.Column(
        'card_id', db.Integer, db.ForeignKey('card.id'), primary_key=True
    ),
    db.Column(
        'hand_id', db.Integer, db.ForeignKey('hand.id'), primary_key=True
    )
    # db.Column('card_rank', db.String(1)),
    # db.Column('card_suit', db.String(1)),
    # db.ForeignKeyConstraint(
    #     ['card_rank', 'card_suit'], ['card.rank', 'card.suit']
    # )
)


class Hand(db.Model):
    '''Provide player hand object.'''

    # TODO: lookup stack
    spades_broken = False
    max_size = 13

    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    player = db.relationship('Player', back_populates='hand')
    cards = db.relationship(
        'Card',
        secondary=cards,
        lazy='subquery',
        backref=db.backref('hand_of_cards', lazy=True)
    )

    def __repr__(self) -> str:
        '''Return string representation of card.'''
        return f"{self.__class__.__name__}(hand={self.cards!r})"

    def __len__(self) -> int:
        '''Return number of items.'''
        return len(self.cards)

    def __iter__(self) -> 'Hand':
        '''Return hand itself as iterator.'''
        self.__count = 0
        return self

    def __next__(self) -> Card:
        '''Get next card instance.'''
        if self.__count >= len(self.cards):
            raise StopIteration()
        card: Card = self.cards[self.__count]
        self.__count += 1
        return card

    @property
    def to_json(self):
        '''Get json instance.'''
        return(json.dumps(self.cards, cls=CardEncoder))

    def list_suit(self, suit: str) -> List[str]:
        '''List items of a suit.'''
        return [c.rank for c in self.cards if c.suit == suit]

    def get_suit(self, suit: str) -> List[Card]:
        '''Get all items of a suit.'''
        return [c for c in self.cards if c.suit == suit]

    def playable(self, suit: str = None) -> List[Card]:
        '''Get all playable cards.'''
        if not suit and not Hand.spades_broken:
            hand = [c for c in self.cards if c.suit != 'S']
            return self.cards if hand == [] else hand
        elif suit and len(self.get_suit(suit)) > 0:
            return self.get_suit(suit)
        else:
            return self.cards

    def add_card(self, card: Card) -> None:
        '''Add card to player hand.'''
        if len(self.cards) < Hand.max_size:
            if card not in self.cards:
                self.cards.append(card)
            else:
                exceptions.InvalidDeckException(
                    'duplicate card already in hand'
                )
        else:
            raise exceptions.MaxHandSizeException('maximum hand size')

    def pull_card(self, rank: str, suit: str) -> Card:
        '''Pull card from hand to play.'''
        selection = Card(rank, suit)
        for card in self.cards:
            if selection == card:
                if selection.suit == 'S':
                    Hand.spades_broken = True
                self.cards.remove(card)
                return card
        raise exceptions.IllegalPlayException('player does not hold card')
