'''Provide pytest fixture for flask.'''

import pytest

from spades import create_app


@pytest.fixture
def app():
    '''Retrieve flask instance.'''
    app = create_app()
    return app
