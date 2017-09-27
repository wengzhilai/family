# file: example1.py
'''首页'''
import hashlib
import app.core.Fun
from app import app, auth
from flask_login import login_required
from flask import make_response, request, g
from functools import wraps



tokens = {
    "secret-token-1": "john",
    "secret-token-2": "susan"
}

@auth.verify_token
def verify_token(token):
    print('verify_token')
    print(token)
    if token in tokens:
        g.current_user = tokens[token]
        return True
    return False


@app.route('/', methods=['GET', 'POST'])
@auth.login_required
def index():
    return "Hello, %s!" % 22