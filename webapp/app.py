'''Provide application interface.'''

from flask import Flask
from flask_jwt import JWT, current_identity, jwt_required
from werkzeug.security import safe_str_cmp


class User(object):
    '''Provide abstract user.'''

    def __init__(self, ident, username, password):
        '''Initialize user object.'''
        self.id = ident
        self.username = username
        self.password = password

    def __str__(self):
        '''Retrieve user string.'''
        return "User(id='%s')" % self.id


users = [
    User(1, 'user1', 'abcxyz'),
    User(2, 'user2', 'abcxyz'),
]

username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}


def authenticate(username, password):
    '''Authenticate user.'''
    user = username_table.get(username, None)
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user


def identity(payload):
    '''Retreive user identity.'''
    user_id = payload['identity']
    return userid_table.get(user_id, None)


app = Flask(
    __name__,
    static_url_path='',
    static_folder='static/dist',
    # template_folder='templates'
)
app.debug = True
app.config['SECRET_KEY'] = 'super-secret'

jwt = JWT(app, authenticate, identity)


@app.route('/protected')
@jwt_required()
def protected():
    '''Check protected resource.'''
    return '%s' % current_identity
