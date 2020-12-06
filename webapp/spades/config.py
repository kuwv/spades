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
db_port: int = os.getenv('POSTGRESQL_PORT', 5432)
db_user: str = os.getenv('POSTGRESQL_USER', 'spades')
db_pass: str = os.getenv('POSTGRESQL_PASSWORD', 'password')
db_name: str = os.getenv('POSTGRESQL_DATABASE', 'spades')
session_type: str = os.getenv('SESSION_TYPE', 'redis')

# f"redis://:{session_password}@{session_host}:{session_port}"
session = {
    'host': os.getenv('REDIS_HOST', 'localhost'),
    'port': os.getenv('REDIS_PORT', 6379),
    'password': os.getenv('REDIS_PASSWORD', 'password'),
    'socket_timeout': os.getenv('REDIS_TIMEOUT', 300),
    # 'db': 0,
    # 'socket_connect_timeout': None,
    # 'socket_keepalive': None,
    # 'socket_keepalive_options': None,
    # 'connection_pool': None,
    # 'unix_socket_path': None,
    # 'encoding': 'utf-8',
    # 'encoding_errors': 'strict',
    # 'charset': None,
    # 'errors': None,
    # 'decode_responses': False,
    # 'retry_on_timeout': False,
    'ssl': os.getenv('REDIS_TLS', False),
    'ssl_keyfile': os.getenv('REDIS_KEYFILE', None),
    'ssl_certfile': os.getenv('REDIS_CERTFILE', None),
    'ssl_cert_reqs': os.getenv('REDIS_CERT_REQS', 'required'),
    'ssl_ca_certs': os.getenv('REDIS_CA_CERTS', None),
    'ssl_check_hostname': os.getenv('REDIS_CERT_CHECK', False),
    # 'max_connections': None,
    # 'single_connection_client': False,
    # 'health_check_interval': 0,
    # 'client_name': None,
    # 'username': None
}


class Config:
    '''Provide Flask configuration.'''

    SQLALCHEMY_DATABASE_URI: str = os.getenv(
        'SQLALCHEMY_DATABASE_URI',
        f"{db_type}://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
    )
    SQLALCHEMY_ECHO: bool = os.getenv('SQLALCHEMY_ECHO', True)
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = os.getenv(
        'SQLALCHEMY_TRACK_MODIFICATIONS',
        False
    )

    SESSION_COOKIE_SECURE: bool = True
    SESSION_COOKIE_HTTPONLY: bool = True
    SESSION_COOKIE_SAMESITE: str = 'Lax'

    SECRET_KEY: str = genword(entropy=56, length=128)
    WTF_CSRF_SECRET_KEY: str = genword(entropy=56, length=128)

    SESSION_TYPE: str = session_type
    SESSION_PERMANENT: bool = True
    SESSION_USE_SIGNER: bool = True
    SESSION_REDIS = Redis(**session)
    SSE_REDIS_URL = "redis://:{p}@{h}:{s}".format(
        p=session['password'], h=session['host'], s=session['port']
    )
