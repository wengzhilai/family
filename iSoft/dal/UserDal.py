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
from iSoft.entity.model import FaUser,FaModule
from iSoft.dal.LoginDal import LoginDal
import datetime
from iSoft.core.AlchemyEncoder import AlchemyEncoder
import json

class UserDal(FaUser):
    roleIdList = []
    moduleList = []

    def user_findall(self, pageIndex, pageSize, criterion, where):
        relist, is_succ = Fun.model_findall(
            FaUser, pageIndex, pageSize, criterion, where)
        return relist, is_succ

    def user_Save(self, in_dict, saveKeys):
        relist, is_succ = Fun.model_save(FaUser, self, in_dict, saveKeys)
        if is_succ.IsSuccess:  # 表示已经添加成功角色
            sqlStr = '''
                DELETE
                FROM
                    fa_user_role
                WHERE
                    fa_user_role.USER_ID = {0}
            '''.format(relist.ID)
            print(sqlStr)
            execObj = db.session.execute(sqlStr)
            if len(relist.roleIdList) > 0:
                sqlStr = '''
                    INSERT INTO fa_user_role (ROLE_ID, USER_ID) 
                        SELECT
                            m.ID ROLE_ID,
                            {0}  USER_ID
                        FROM
                            fa_role m
                        WHERE
                            m.ID IN ({1})
                '''.format(relist.ID, ','.join(str(i) for i in relist.roleIdList))
                print(sqlStr)
                execObj = db.session.execute(sqlStr)
            db.session.commit()

        return relist, is_succ

    def user_delete(self, key):
        is_succ = Fun.model_delete(FaUser, self, key)
        return is_succ, is_succ

    def user_all_module(self, userId):
        db_ent = FaUser.query.filter(FaUser.ID == userId).first()
        if db_ent is not None:
            # 获取所有 选中的模块
            roleIdList = [item.fa_modules for item in db_ent.fa_roles if len(item.fa_modules) > 0]
            moduleList = list(numpy.array(roleIdList).flatten())
            moduleIdList = [item.ID for item in moduleList ]
            moduleParentIdList = [item.PARENT_ID for item in moduleList if item.PARENT_ID not in moduleIdList]
            
            moduleParentList = FaModule.filter(FaModule.ID.in_(moduleParentIdList)).all()
            print(moduleParentList)
            return moduleList, AppReturnDTO(True)
        return None, AppReturnDTO(True)

    def user_single(self, key):
        '''查询一用户'''
        relist, is_succ = Fun.model_single(FaUser, key)
        tmp = UserDal()
        tmp.__dict__ = relist.__dict__
        tmpId = [x.ID for x in relist.fa_roles]
        tmp.roleIdList = tmpId
        return tmp, is_succ

    def user_login(self, _inent):
        '''用户登录'''
        in_ent = LogingModel()
        in_ent.__dict__ = _inent
        if in_ent.loginName is None or in_ent.loginName == '':
            return AppReturnDTO(False, "用户名不能为空")
        if in_ent.password is None or in_ent.password == '':
            return AppReturnDTO(False, "密码不能为空")

        login = FaLogin.query.filter_by(LOGIN_NAME=in_ent.loginName).first()
        user = FaUser.query.filter_by(LOGIN_NAME=in_ent.loginName).first()
        if user is None or login is None:
            return AppReturnDTO(False, "用户名有误")

        if login.PASSWORD != hashlib.md5(
                in_ent.password.encode('utf-8')).hexdigest():
            return AppReturnDTO(False, "密码有误")

        tmp = UserDal()
        tmp.__dict__ = user.__dict__
        tmpId = [x.ID for x in user.fa_roles]
        tmp.roleIdList = tmpId

        moduleIdList, msg = self.user_all_module(user.ID)
        # 获取用户模块
        if not msg.IsSuccess:
            return msg
            
        tmp.moduleList = json.loads(json.dumps(moduleIdList, cls=AlchemyEncoder))
        token = LoginDal.generate_auth_token(tmp)
        token = token.decode('utf-8')
        return AppReturnDTO(True, "登录成功", tmp, token)

    @staticmethod
    def login_out():
        '''退出登录'''
        return AppReturnDTO(True)

    @staticmethod
    def verify_auth_token(token):
        '''验证token'''
        return Fun.verify_auth_token(token)

    @staticmethod
    def login_reg(_inent):
        '''注册用户'''

        in_ent = LogingModel()
        in_ent.__dict__ = _inent
        if in_ent.loginName is None or in_ent.loginName == '':
            return AppReturnDTO(False, "电话号码不能为空")
        if not Fun.is_phonenum(in_ent.loginName):
            return AppReturnDTO(False, "电话号码格式不正确")

        complexity = Fun.password_complexity(in_ent.password)
        if complexity < PASSWORD_COMPLEXITY:
            return AppReturnDTO(False, "密码复杂度不够:" + str(complexity))
        return AppReturnDTO(False, "暂不开放注册")
