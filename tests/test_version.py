# type: ignore
'''Test version.'''
from __version__ import __version__


def test_version():
    '''Test version.'''
    assert __version__ == "0.1.0"