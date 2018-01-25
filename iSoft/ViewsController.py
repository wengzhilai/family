# file: view.py
# -*- coding: utf-8 -*-
'''首页'''
import iSoft.core.Fun
from iSoft import app, auth
from flask_login import login_required
from flask import make_response, request, g
from functools import wraps
from iSoft.dal.UserDal import UserDal
import json


@auth.verify_token
def verify_token(token):
    '''验证toke'''
    print('verify_token')
    print(token)
    msg, user = UserDal.verify_auth_token(token)
    if msg.is_success:
        g.current_user = user
        return True
    return False


@app.route('/', methods=['GET', 'POST'])
@auth.login_required
def index():
    if g == None:
        return "Hellow"
    return "Hello, %s!" % g.current_user.ID


@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username


@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id


@app.route('/projects/', methods=['GET', 'POST'])
def projects():
    h = request.headers
    j = request.json
    b = request.get_data()

    j_data = json.loads(str(b, encoding = "utf-8"))#-----load将字符串解析成json
    
    # print(j_data)
    return j.__str__()


@app.route('/about')
def about():
    return 'The about page'


# @app.errorhandler(404)
# def internal_error(error):
#     return "render_template('404.html')", 404

# @app.errorhandler(500)
# def internal_error(error):
#     db.session.rollback()
#     return "render_template('500.html')", 500
