'''Test card.'''

from spades.card import Card


def test_card():
    card = Card('K', 'Spades')
    assert card.rank == 'K'
    assert card.suit == 'Spades'
