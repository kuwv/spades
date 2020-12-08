'''Provide account management for app.'''

from typing import Optional, Union

import flask
from flask import Blueprint, url_for
from flask_login import current_user, login_required, login_user, logout_user
from flask_wtf import FlaskForm
from werkzeug.wrappers import Response
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Length, Regexp

from spades import db, login_manager
from spades.models.user import User

auth = Blueprint('auth', __name__)


class LoginForm(FlaskForm):
    username: StringField = StringField(
        'Username',
        validators=[
            DataRequired(),
            Length(min=4, max=25),
            Regexp('^[a-zA-Z][a-zA-Z0-9._]+[a-zA-Z0-9]$')
        ]
    )
    password: PasswordField = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=8, max=25)
        ]
    )
    submit: SubmitField = SubmitField('login')


class RegistrationForm(LoginForm):
    confirm: PasswordField = PasswordField(
        'Confirm', validators=[
            DataRequired(),
            EqualTo('password', message='passwords must match'),
            Length(min=8, max=25)
        ]
    )
    submit: SubmitField = SubmitField('register')


@auth.route('/register', methods=['GET', 'POST'])
def register() -> Union[Response, str]:
    if not current_user.is_authenticated:
        form = RegistrationForm(flask.request.form)
        if form.validate_on_submit():
            # check if username is already in use
            if User.query.filter_by(username=form.username.data).first():
                flask.flash('please choose another username')
                return flask.redirect(url_for('auth.register'))

            # create a new user with the form data
            user = User(username=form.username.data)
            user.set_password(form.password.data)

            # add the new user to the database
            db.session.add(user)
            db.session.commit()

            return flask.redirect(url_for('auth.login'))
        return flask.render_template('register.html', form=form)
    else:
        flask.flash('cannot register during active session')
        return flask.redirect(url_for('main.lobby'))


@auth.route('/login', methods=['GET', 'POST'])
def login() -> Union[Response, str]:
    '''Provide user login.'''
    if not current_user.is_authenticated:
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                flask.flash('successfull login')
                return flask.redirect(url_for('main.lobby'))
            else:
                flask.flash('Error: invalid credentials')
                return flask.redirect(url_for('auth.login'))
        return flask.render_template('login.html', form=form)
    return flask.redirect(url_for('main.lobby'))


@auth.route('/logout')
@login_required
def logout() -> Response:
    '''Provide user logout.'''
    logout_user()
    return flask.redirect(url_for('auth.login'))


@login_manager.user_loader
def load_user(user_id: int) -> Optional[User]:
    '''Check user login.'''
    if user_id is not None:
        return User.query.get(user_id)
    return None
