# file: example1.py
'''首页'''
from app import app,auth,login_manager
from flask import json,request
from app.dbModel.dal.UserDal import UserDal
from app.core.AlchemyEncoder import AlchemyEncoder
from flask_login import (LoginManager, login_required, login_user,
                            current_user, logout_user, UserMixin)
from app.dbModel.models.DB_UserModel import User
from app.core.model.AppReturnDTO import AppReturnDTO
from app.core.Fun import Fun


@app.route('/')
@app.route('/index')
def index():
    ''' 首页 '''
    user = UserDal.SingleUser(1)
    print(user)
    return json.dumps(user, cls=AlchemyEncoder)

# test method
@app.route('/index/test')
@login_required
def test():
    '''测试'''
    print('current_user.NAME')
    return 'Logged in as: '

