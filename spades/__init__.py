# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
"""Provide spades webapp package metadata."""

from flask import Flask
# from flask_cors import CORS
from flask_login import LoginManager
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_sse import sse

# from spades import config

__author__ = 'Jesse P. Johnson'
__author_email__ = 'jpj6652@gmail.com'
__title__ = 'spades'
__description__ = 'SWE-681 Final Project - Spades'
__version__ = '0.1.0'
__license__ = 'Apache-2.0'
__copyright__ = 'Copyright 2020 Jesse Johnson.'

db = SQLAlchemy()
login_manager = LoginManager()
session = Session()


def create_app() -> Flask:
    """Create application instance."""
    app = Flask(
        __name__,
        instance_relative_config=False,
        # static_url_path='/css',
        static_folder='static',
        template_folder='templates'
    )
    app.config.from_object('spades.config.Config')

    db.init_app(app)

    # CORS(app, resources={r'/*': {'origins': '*'}})

    login_manager.session_protection = 'strong'
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    session.init_app(app)
    with app.app_context():
        from spades.auth import auth
        from spades.main import main

        app.register_blueprint(auth)
        app.register_blueprint(main)
        app.register_blueprint(sse, url_prefix='/stream')

        db.create_all()
        return app
