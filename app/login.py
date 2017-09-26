# file: example1.py
'''首页'''
from app.core.Fun import Fun
from app import auth, login_manager
from flask import json, request, flash
from app.entity.dal.UserDal import UserDal
from flask_login import (LoginManager, login_required, login_user,
                            current_user, logout_user, UserMixin)
from app.entity.models.DB_UserModel import USER
from app.core.model.AppReturnDTO import AppReturnDTO
from app.core.model.LogingModel import LogingModel
from app.core.AlchemyEncoder import AlchemyEncoder
 

@login_manager.user_loader
def load_user(user_id):
    ''' 获取用户信息 '''
    user = UserDal.single_user(user_id)
    return json.dumps(Fun.convert_to_dict(user), ensure_ascii=False)

@auth.route('/token', methods=['GET', 'POST'])
def token():
    '''用户登录'''
    # user = User()
    # login_user(user)
    print(request.data)
    a = request.get_data()
    print(a)
    j_data =  json.loads(a) #-----load将字符串解析成json

    class MyClass(object):
        loginName="1"
        password=""
    myclass=MyClass()
    myclass.__dict__=j_data;

    print('JSON:')
    print(myclass.loginName)
    print(myclass.password)
    re_ent = AppReturnDTO(False, '登录超时')
    json_str = Fun.convert_to_dict(re_ent)
    re_str = json.dumps(json_str, ensure_ascii=False)
    return re_str

@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    '''退出登录'''
    flash(u'You have been signed out')
    re_ent = AppReturnDTO(False, U'登录超时')
    return json.dumps(Fun.convert_to_dict(re_ent))

@auth.route('/UserLogin', methods=['GET', 'POST'])
def user_login():
    '''用户登录'''
    j_data = json.loads(request.get_data())#-----load将字符串解析成json
    print(j_data)
    ent = UserDal.user_login(j_data)
    print(ent.__dict__)
    # return json.dumps(ent, cls=AlchemyEncoder)
    return json.dumps(Fun.convert_to_dict(ent), ensure_ascii=False)
