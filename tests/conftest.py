'''Provide pytest fixture for flask.'''

import pytest

from spades import create_app, db as _db
from spades.game import GameState, Player


@pytest.fixture
def app():
    '''Retrieve flask instance.'''
    app = create_app()
    return app


# @pytest.fixture(scope='module')
# def dbconn():
#     pass


@pytest.fixture(scope='session')
def db(request):
    """Session-wide test database."""
    _db.create_all()
    request.addfinalizer(_db.drop_all())
    return _db


@pytest.fixture(scope='session')
def db_session():
    game = GameState(2)
    game.add_player(Player('Jim'))
    game.add_player(Player('Mike'))
