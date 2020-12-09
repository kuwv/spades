# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Provide book package.'''

import os

from passlib.pwd import genword
from redis import Redis

# logging
loglevel: str = os.getenv('LOGLEVEL', 'INFO').upper()

# spades settings
player_max: int = 2
winning_score: int = 50


def set_player_max(count: int) -> None:
    '''Set player count.'''
    global player_max
    player_max = count


# db settings
db_type: str = os.getenv('DB_TYPE', 'postgres')
db_host: str = os.getenv('POSTGRESQL_HOST', 'localhost')
db_port: int = int(os.getenv('POSTGRESQL_PORT', 5432))
db_user: str = os.getenv('POSTGRESQL_USER', 'spades')
db_pass: str = os.getenv('POSTGRESQL_PASSWORD', 'password')
db_name: str = os.getenv('POSTGRESQL_DATABASE', 'spades')
session_type: str = os.getenv('SESSION_TYPE', 'redis')

# f"redis://:{session_password}@{session_host}:{session_port}"
session = {
    'host': os.getenv('REDIS_HOST', 'localhost'),
    'port': int(os.getenv('REDIS_PORT', 6379)),
    'password': os.getenv('REDIS_PASSWORD', 'password'),
    'socket_timeout': int(os.getenv('REDIS_TIMEOUT', 30)),
}

sqlalchemy_engine_options = {
    'connect_args': {
        'conection_timeout': 30
    }
}


class Config:
    '''Provide Flask configuration.'''

    SQLALCHEMY_DATABASE_URI: str = os.getenv(
        'SQLALCHEMY_DATABASE_URI',
        f"{db_type}://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
    )
    SQLALCHEMY_ECHO: bool = bool(os.getenv('SQLALCHEMY_ECHO', True))
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = bool(
        os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', False)
    )

    SESSION_COOKIE_SECURE: bool = True
    SESSION_COOKIE_HTTPONLY: bool = True
    SESSION_COOKIE_SAMESITE: str = 'Lax'

    SECRET_KEY: str = genword(entropy=56, length=128)
    WTF_CSRF_SECRET_KEY: str = genword(entropy=56, length=128)

    SESSION_TYPE: str = session_type
    SESSION_PERMANENT: bool = True
    SESSION_USE_SIGNER: bool = True
    SESSION_REDIS = Redis(**session)  # type: ignore
    SSE_REDIS_URL = "redis://:{p}@{h}:{s}".format(
        p=session['password'], h=session['host'], s=session['port']
    )
