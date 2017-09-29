# file: example1.py
'''首页'''
from app.core.Fun import Fun
from app import auth, login_manager, app
from flask import json, request, flash, g
from app.entity.dal.UserDal import UserDal
from flask_login import (LoginManager, login_required, login_user,
                            current_user, logout_user, UserMixin)
from app.entity.models.DB_UserModel import USER
from app.core.model.AppReturnDTO import AppReturnDTO
from app.core.AlchemyEncoder import AlchemyEncoder


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    '''退出登录'''
    re_ent = UserDal.login_out()
    return json.dumps(Fun.convert_to_dict(re_ent))

@app.route('/auth/UserLogin', methods=['GET', 'POST'])
def user_login():
    '''用户登录'''
    j_data = json.loads(request.get_data())#-----load将字符串解析成json
    print(j_data)
    ent = UserDal.user_login(j_data)
    print(ent.__dict__)
    # return json.dumps(ent, cls=AlchemyEncoder)
    return json.dumps(Fun.convert_to_dict(ent), ensure_ascii=False)
