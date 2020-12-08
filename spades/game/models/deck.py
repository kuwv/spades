# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Provide card package.'''

from secrets import choice

from spades import db
from spades.game.models.card import Card


cards = db.Table(
    'deck_of_cards',
    db.Column(
        'card_id', db.Integer, db.ForeignKey('card.id'), primary_key=True
    ),
    db.Column(
        'deck_id', db.Integer, db.ForeignKey('deck.id'), primary_key=True
    )
    # db.Column('card_rank', db.String(1)),
    # db.Column('card_suit', db.String(1)),
    # db.ForeignKeyConstraint(
    #     ['card_rank', 'card_suit'], ['card.rank', 'card.suit']
    # )
)


class Deck(db.Model):
    '''Provide deck object.'''

    id = db.Column(db.Integer, primary_key=True)
    cards = db.relationship(
        'Card',
        secondary=cards,
        lazy='subquery',
        backref=db.backref('deck_of_cards', lazy=True)
    )
    max_size = 52

    def __init__(self) -> None:
        '''Initialize Deck.'''
        for rank in Card.ranks:
            for suit in Card.suits:
                self.cards.append(Card(rank, suit))

    def __iter__(self) -> 'Deck':
        '''Return deck itself as iterator.'''
        return self

    def __next__(self) -> Card:
        '''Get next card instance.'''
        if len(self.cards) <= 0:
            raise StopIteration()
        card = choice(self.cards)
        self.cards.remove(card)
        return card
