# -*- coding: utf-8 -*-
# type: ignore
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Test book.'''

# import pytest
from sqlalchemy.inspection import inspect

from spades import db  # , exceptions
from spades.game.models.card import Card
from spades.game.models.book import Book
from spades.game.models.play import Play
from spades.game.models.player import Player


def test_book(app):
    '''Test card in book.'''
    book = Book()
    player = Player.query.filter_by(username='test1').first()
    if not player:
        player = Player(username='test1')
        db.session.add(player)
    card = Card.query.filter(Card.rank == 'K', Card.suit == 'S').first()
    if not card:
        card = Card('K', 'S')
        db.session.add(card)
    db.session.commit()

    player_id = inspect(player).identity[0]
    card_id = inspect(card).identity[0]

    book.add_trick(Play(player_id, card_id))
    db.session.add(card)
    db.session.commit()
    print('plays:', book.plays)
    # if Book.query.filter_by(username=form.username.data).first():
    # assert Card('K', 'S') in book


def test_book_trump(app):
    '''Test high card in book.'''
    book = Book()
    book.add_trick(Play(1, Card('2', 'D')))
    book.add_trick(Play(2, Card('T', 'D')))
    # assert book.trump == Card('T', 'D')


# def test_winner(app):
#     player1 = Player(username='player1')
#     player2 = Player(username='player2')
#     book = Book()
#     book.add_trick(player1.id, Play(Card('4', 'S')))
#     book.add_trick(player2.id, Play(Card('5', 'S')))
#     db.session.add(book)
#     db.session.commit()
#     # print(db.session.query('book_of_cards').all())
#     print(book.cards)
#     print('book', book)
#     print('winner', book.winner)


# def test_book_max():
#     '''Test maximum allowed cards in book.'''
#     book = Book()
#     with pytest.raises(exceptions.MaxBookSizeException):
#         book.add_trick(3, Card('2', 'H'))
#         book.add_trick(0, Card('3', 'H'))
