'''用户业务处理'''

from iSoft.entity.model import db, FaUser, FaModule, FaRole, FaLogin
import math
from iSoft.model.AppReturnDTO import AppReturnDTO
from iSoft.core.Fun import Fun
import numpy
from iSoft.model.LogingModel import LogingModel
import hashlib
from sqlalchemy import and_
from iSoft.core.Fun import Fun
from config import PASSWORD_COMPLEXITY, VERIFY_CODE
from sqlalchemy import or_, and_, create_engine
from iSoft import db
from iSoft.entity.model import FaUser, FaModule, FaUserInfo, FaLogin
from iSoft.dal.LoginDal import LoginDal
import datetime
from iSoft.core.AlchemyEncoder import AlchemyEncoder
import json
from iSoft.model.AppRegisterModel import AppRegisterModel
from .LoginDal import LoginDal


class UserInfoDal(FaUserInfo):
    FatherName = ""

    def userInfo_findall(self, pageIndex, pageSize, criterion, where):
        relist, is_succ = Fun.model_findall(
            FaUserInfo, pageIndex, pageSize, criterion, where)
        return relist, is_succ

    def userInfo_Save(self, in_dict, saveKeys):
        relist, is_succ = Fun.model_save(FaUserInfo, self, in_dict, saveKeys)

        return relist, is_succ

    def userInfo_delete(self, key):
        is_succ = Fun.model_delete(FaUserInfo, self, key)
        return is_succ, is_succ

    def userInfo_single(self, key):
        '''查询一用户'''
        relist, is_succ = Fun.model_single(FaUserInfo, key)
        return relist, is_succ

    def userInfo_SingleByName(self, name):
        relist = FaUserInfo.query.filter(
            FaUserInfo.NAME.like("%{}%".format(name)))
        relist = relist.paginate(1, per_page=10).items
        relistNew = []
        for item in relist:
            tmp = UserInfoDal()
            tmp.__dict__ = item.__dict__
            tmp.FatherName = item.parent.NAME
            relistNew.append(tmp)
        return relistNew, AppReturnDTO(True)

    def userInfo_register(self, _inDict):
        '''
        注册用户
        用于APP注册
        '''

        in_ent = AppRegisterModel(_inDict)
        # 检测电话号码是否合法
        if in_ent.loginName is None or in_ent.loginName == '':
            return AppReturnDTO(False, "电话号码不能为空")
        if not Fun.is_phonenum(in_ent.loginName):
            return AppReturnDTO(False, "电话号码格式不正确")
        # 验证密码复杂度
        complexity = Fun.password_complexity(in_ent.password)
        if complexity < PASSWORD_COMPLEXITY:
            return AppReturnDTO(False, "密码复杂度不够:" + str(complexity))
        # 检测短信代码
        checkOutPwd, msg = LoginDal().CheckOutPassword(in_ent.code, in_ent.loginName)
        # 失败则退出
        if not msg.IsSuccess or not checkOutPwd:
            return msg
        if len(in_ent.parentArr) < 2:
            return AppReturnDTO(False, "你节点有问题")
        # 表示添加已经存在的用户，只需完善资料，并添加登录账号
        loginDal = LoginDal()

        if "K" in in_ent.parentArr[0] and "V" in in_ent.parentArr[0]:
            # 添加登录账号
            loginDal.LOGIN_NAME = in_ent.loginName
            loginDal.PASSWORD = in_ent.password
            loginDal.PHONE_NO = in_ent.loginName
            # 获取添加成功后的Login实体
            loginEng, msg = loginDal.AddLoginName()
            if not msg.IsSuccess:
                return msg

            userInfoEnt = FaUserInfo.query.filter(
                FaUserInfo.ID == int(in_ent.parentArr[0]["K"])).first()
            userInfoEnt = FaUserInfo()
            if userInfoEnt is None:
                return AppReturnDTO(False, "用户的ID有误")
            userInfoEnt.LOGIN_NAME = in_ent.loginName
            userInfoEnt.UPDATE_TIME = datetime.datetime.now()
            userInfoEnt.NAME = in_ent.parentArr[0]["V"]
            userInfoEnt.LEVEL_ID = in_ent.level_id
            userInfoEnt.SEX = in_ent.sex
            userInfoEnt.YEARS_TYPE = in_ent.YEARS_TYPE
            userInfoEnt.BIRTHDAY_TIME = datetime.datetime.strptime(in_ent.BIRTHDAY_TIME, '%Y-%m-%dT%H:%M:%SZ')
            userInfoEnt.BIRTHDAY_PLACE = in_ent.birthday_place

            db.session.commit()
            return AppReturnDTO(True)
            pass

        # 如果有多个父级，都需要每一个每一个用户的添加
        for i, item in in_ent.parentArr[0]:
            pass

        return AppReturnDTO(False, "暂不开放注册")
