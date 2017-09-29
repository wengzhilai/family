'''用户业务处理'''
import hashlib
from app.entity.dbModel import db_model
from sqlalchemy import and_
from app.core.model.LogingModel import LogingModel
from app.core.model.AppReturnDTO import AppReturnDTO
from app.core.Fun import Fun
from config import PASSWORD_COMPLEXITY, VERIFY_CODE
from sqlalchemy import or_, and_, create_engine
from app import db
from app.entity.models.DB_UserModel import USER


class UserDal(object):
    '''用户业务处理'''
    @staticmethod
    def user_login(_inent):
        '''用户登录'''
        in_ent = LogingModel()
        in_ent.__dict__ = _inent
        if in_ent.loginName is None or in_ent.loginName == '':
            return AppReturnDTO(False, "用户名和密码不能为空")

        login = db_model.Login.query.filter_by(LOGIN_NAME=in_ent.loginName).first()
        user = db_model.User.query.filter_by(LOGIN_NAME=in_ent.loginName).first()
        # login=db_model.Login
        # user=db_model.User
        if user is None or login is None:
            return AppReturnDTO(False, "用户名有误")

        if login.PASSWORD != hashlib.md5(in_ent.passWord.encode('utf-8')).hexdigest():
            return AppReturnDTO(False, "密码有误")
        token = login.generate_auth_token()
        token = login.generate_auth_token().decode('utf-8')
        return AppReturnDTO(True, "登录成功",user,token)
    
    @staticmethod
    def login_out():
        '''退出登录'''
        return AppReturnDTO(True)

    @staticmethod
    def verify_auth_token(token):
        '''验证token'''
        return db_model.Login.verify_auth_token(token)

    @staticmethod
    def login_reg(_inent):
        '''注册用户'''
        in_ent = LogingModel()
        in_ent.__dict__ = _inent
        if in_ent.loginName is None or in_ent.loginName=='':
            return AppReturnDTO(False, "电话号码不能为空")
        if not Fun.is_phonenum(in_ent.loginName):
            return AppReturnDTO(False, "电话号码格式不正确")
        if Fun.password_complexity(in_ent.passWord) < PASSWORD_COMPLEXITY:
            return AppReturnDTO(False, "密码复杂度不够")

        if VERIFY_CODE:
            user = db_model.User.query.filter_by(and_(PHONE_NO=in_ent.loginName, CONTENT=in_ent.code)).first()
        return user

    @staticmethod
    def single_user(userId):
        '''查询一用户'''
        user=db.Query(USER).all()
        # user=db_model.User.query.filter_by(LAST_LOGIN_TIME='2017-06-01T20:42:46',DISTRICT_ID=1,NAME='翁应吉').all()
        return user

    # @staticmethod
    # def GetAll():
    #     user=db_model.User.query.all()
    #     return user 

 