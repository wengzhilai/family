'''用户业务处理'''
import hashlib
from app import db
from app.entity.dbModel import db_model
from app.core.model.LogingModel import LogingModel
from app.core.model.AppReturnDTO import AppReturnDTO
class UserDal(object):
    '''用户业务处理'''
    @staticmethod
    def user_login(_inent):
        '''用户登录'''
        in_ent = LogingModel()
        in_ent.__dict__ = _inent
        if in_ent.loginName is None or in_ent.loginName == '':
            return AppReturnDTO(False, "用户名和密码不能为空"), None
        
        login=db_model.Login.query.filter_by(LOGIN_NAME=in_ent.loginName).first()
        user=db_model.User.query.filter_by(LOGIN_NAME=in_ent.loginName).first()
        # login=db_model.Login
        # user=db_model.User
        if user is None or login is None:
            return AppReturnDTO(True, "用户名有误")

        if login.PASSWORD != hashlib.md5(in_ent.passWord.encode('utf-8')).hexdigest():
            return AppReturnDTO(True, "密码有误")
        token=login.generate_auth_token()
        token=login.generate_auth_token().decode('utf-8')
        return AppReturnDTO(True, "登录成功",user,token)

        
    @staticmethod
    def single_user(userId):
        user=db_model.User.query.filter_by(ID=userId).first();
        return user
    @staticmethod
    def GetAll():
        user=db_model.User.query.all()
        return user 

    @staticmethod
    def AddEnt(name):
        user=User()
        user.DISTRICT_ID=1
        user.NAME=name
        db.session.add(user)
        return user 