# file: example1.py
'''首页'''
import app.core.Fun
from app import app, auth
from flask_login import login_required
from flask import make_response, request, g
from functools import wraps
from app.entity.dal.UserDal import UserDal

@auth.verify_token
def verify_token(token):
    '''验证toke'''
    print('verify_token')
    print(token)
    msg, user=UserDal.verify_auth_token(token)
    if msg.is_success:
        g.current_user = user
        return True
    return False


@app.route('/', methods=['GET', 'POST'])
@auth.login_required
def index():
    return "Hello, %s!" % 22