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
from iSoft.entity.model import FaUser, FaModule
from iSoft.dal.LoginDal import LoginDal
from iSoft.dal.AuthDal import AuthDal
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
            # 获取所有 选中的模块,没有隐藏的模块
            roleIdList = [[x for x in item.fa_modules if x.IS_HIDE == 0] for item in db_ent.fa_roles if len(item.fa_modules) > 0]
            moduleList = list(numpy.array(roleIdList).flatten())
            moduleList = sorted(moduleList, key=lambda x: x.SHOW_ORDER)
            moduleIdList = [item.ID for item in moduleList]
            moduleParentIdList = [
                item.PARENT_ID for item in moduleList if item.PARENT_ID not in moduleIdList]

            moduleParentList = FaModule.query.filter(
                FaModule.ID.in_(moduleParentIdList)).all()
            return moduleList + moduleParentList, AppReturnDTO(True)
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
        if in_ent.passWord is None or in_ent.passWord == '':
            return AppReturnDTO(False, "密码不能为空")

        login = FaLogin.query.filter_by(LOGIN_NAME=in_ent.loginName).first()
        user = FaUser.query.filter_by(LOGIN_NAME=in_ent.loginName).first()
        if user is None or login is None:
            return AppReturnDTO(False, "用户名有误")

        if login.PASSWORD != Fun.md5(in_ent.passWord):
            return AppReturnDTO(False, "密码有误")

        tmp = UserDal()
        tmp.__dict__ = user.__dict__
        tmpId = [x.ID for x in user.fa_roles]
        tmp.roleIdList = tmpId

        moduleIdList, msg = self.user_all_module(user.ID)
        # 获取用户模块
        if not msg.IsSuccess:
            return msg

        tmp.moduleList = json.loads(
            json.dumps(moduleIdList, cls=AlchemyEncoder))
        token = AuthDal.generate_auth_token(tmp)
        token = token.decode('utf-8')
        return AppReturnDTO(True, "登录成功", tmp, token)
    
    def user_checkLoginExist(self, loginName):
        '检测登录名是否存在'
        user = FaUser.query.filter_by(LOGIN_NAME=loginName).first()
        if user is None:
            return False
        return True


