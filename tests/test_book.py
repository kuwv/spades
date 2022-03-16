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
    db.session.add(book)

    # Add test player
    player = Player.query.filter_by(username='test1').first()
    if not player:
        player = Player(username='test1')
        db.session.add(player)

    # Add test card
    card = Card.query.filter(Card.rank == 'K', Card.suit == 'S').first()
    if not card:
        card = Card('K', 'S')
        db.session.add(card)
    db.session.commit()

    play = Play(book=book, card=card, player=player)
    # play = Play(
    #     inspect(book).identity[0],
    #     inspect(player).identity[0],
    #     inspect(card).identity[0]
    # )
    print(play)
    db.session.add(play)
    db.session.commit()
    # book.add_play(play)
    # db.session.add(book)
    # db.session.commit()
    # print('plays:', book.plays)
    # query = db.session.query(Play, Player)\
    #     .filter(Book.id == Play.book_id)\
    #     .filter(Play.player_id == Player.id)\
    #     .filter(Player.username == 'test1')\
    #     .first()
    # print('player', query)
    # assert book.suit == 'S'
    # assert book.high_card == card
    # assert book.broken is True


# def test_book_trump(app):
#     '''Test high card in book.'''
#     book = Book()
#     book.add_play(Play(1, Card('2', 'D')))
#     book.add_play(Play(2, Card('T', 'D')))
#     assert book.trump == Card('T', 'D')


# def test_winner(app):
#     player1 = Player(username='player1')
#     player2 = Player(username='player2')
#     book = Book()
#     book.add_play(player1.id, Play(Card('4', 'S')))
#     book.add_play(player2.id, Play(Card('5', 'S')))
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
#         book.add_play(3, Card('2', 'H'))
#         book.add_play(0, Card('3', 'H'))
