# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Implement spaces package.'''

from flask import Flask
# from flask_cors import CORS
from flask_login import LoginManager
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
login_manager = LoginManager()
session = Session()


def create_app() -> Flask:
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

        db.create_all()
        return app
