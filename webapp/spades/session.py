# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Provide session package.'''

from redis import Redis

from spades import config


class Session(Redis):
    '''Provide session object.'''

    def __init__(self, db=0) -> None:
        '''Initialize session.'''
        super().__init__(
            self,
            host=config.redis_host,
            port=config.redis_port,
            db=db,
            password=config.redis_password,
            socket_timeout=config.redis_timeout
        )
