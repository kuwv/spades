# type: ignore
'''Test hand.'''

from spades import db
from spades.game.models.card import Card
from spades.game.models.player import Hand


def test_hand(app) -> None:
    hand = Hand()
    hand.add_card(Card('A', 'S'))
    db.session.add(hand)
    db.session.commit()

    card = hand.pull_card('A', 'S')
    assert card.rank == 'A'
    assert card.suit == 'S'
