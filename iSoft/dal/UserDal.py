'''用户业务处理'''

from iSoft.entity.model import db, FaUser, FaModule, FaRole, FaLogin
import math
from iSoft.model.AppReturnDTO import AppReturnDTO
from iSoft.core.Fun import Fun
import numpy
from iSoft.model.LogingModel import LogingModel
import hashlib
import iSoft.entity.model
from sqlalchemy import and_
from iSoft.core.Fun import Fun
from config import PASSWORD_COMPLEXITY, VERIFY_CODE
from sqlalchemy import or_, and_, create_engine
from iSoft import db
from iSoft.entity.model import FaUser
from iSoft.dal.LoginDal import LoginDal
import datetime




class UserDal(FaUser):
    def user_findall(self, pageIndex, pageSize, criterion, where):
        relist,is_succ=Fun.model_findall(FaUser, self, pageIndex, pageSize, criterion, where)
        return relist, is_succ

    def user_all_module(self,userId):
        db_ent = FaUser.query.filter(FaUser.ID == userId).first()

        if db_ent is not None:
            roleIdList = [item.fa_modules for item in db_ent.fa_roles if len(item.fa_modules)>0]
            moduleIdList =list(numpy.array(roleIdList).flatten())
                    
            return moduleIdList,AppReturnDTO(True)
        return None,AppReturnDTO(True)

    @staticmethod
    def user_login(_inent):
        '''用户登录'''
        in_ent = LogingModel()
        in_ent.__dict__ = _inent
        if in_ent.loginName is None or in_ent.loginName == '':
            return AppReturnDTO(False, "用户名不能为空")
        if in_ent.passWord is None or in_ent.passWord == '':
            return AppReturnDTO(False, "密码不能为空")

        login = FaLogin.query.filter_by(LOGIN_NAME=in_ent.loginName).first()
        user = FaUser.query.filter_by(LOGIN_NAME=in_ent.loginName).first()
        # login=db_model.Login
        # user=db_model.User
        if user is None or login is None:
            return AppReturnDTO(False, "用户名有误")

        if login.PASSWORD != hashlib.md5(
                in_ent.passWord.encode('utf-8')).hexdigest():
            return AppReturnDTO(False, "密码有误")
        token = LoginDal().generate_auth_token()
        token = LoginDal().generate_auth_token().decode('utf-8')
        return AppReturnDTO(True, "登录成功", user, token)

    @staticmethod
    def login_out():
        '''退出登录'''
        return AppReturnDTO(True)

    @staticmethod
    def verify_auth_token(token):
        '''验证token'''
        return LoginDal().verify_auth_token(token)

    @staticmethod
    def login_reg(_inent):
        '''注册用户'''

        in_ent = LogingModel()
        in_ent.__dict__ = _inent
        if in_ent.loginName is None or in_ent.loginName == '':
            return AppReturnDTO(False, "电话号码不能为空")
        if not Fun.is_phonenum(in_ent.loginName):
            return AppReturnDTO(False, "电话号码格式不正确")
        complexity = Fun.password_complexity(in_ent.passWord)
        if complexity < PASSWORD_COMPLEXITY:
            return AppReturnDTO(False, "密码复杂度不够:" + str(complexity))
        # now_time = datetime.datetime.now()
        # if VERIFY_CODE:
        #
        #     _sms_count = db.session.query(db_model.SmsSend).filter(
        #         db_model.SmsSend.ADD_TIME < now_time,
        #         db_model.SmsSend.PHONE_NO==in_ent.loginName,
        #         db_model.SmsSend.CONTENT==in_ent.code
        #         ).count()
        #     if _sms_count==0:
        #         return AppReturnDTO(False, "验证码错误")

        # user = FaUser.query.filter(FaUser.CREATE_TIME > now_time).all()
        return AppReturnDTO(False, "暂不开放注册")

    @staticmethod
    def single_user(userId):
        '''查询一用户'''
        # user=db.Query(USER).all()
        # user=db_model.User.query.filter_by(ID=1).all()
        now_time = datetime.datetime.now()
        user = FaUser.query.filter(FaUser.CREATE_TIME < now_time).all()
        return user

    # @staticmethod
    # def GetAll():
    #     user=db_model.User.query.all()
    #     return user
    
