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
import datetime
from iSoft.core.AlchemyEncoder import AlchemyEncoder
import json
from iSoft.model.AppRegisterModel import AppRegisterModel
from .LoginDal import LoginDal
from .UserDal import UserDal


class UserInfoDal(FaUserInfo):
    FatherName = ""

    def userInfo_findall(self, pageIndex, pageSize, criterion, where):
        relist, is_succ = Fun.model_findall(FaUserInfo, pageIndex, pageSize,
                                            criterion, where)
        return relist, is_succ

    def userInfo_Save(self, in_dict, saveKeys):
        relist, is_succ = Fun.model_save(FaUserInfo, self, in_dict, saveKeys)

        return relist, is_succ

    def userInfo_delete(self, key):
        delMode,is_succ = Fun.model_delete(FaUserInfo, key)
        return delMode,is_succ

    def userInfo_single(self, key):
        '''查询一用户'''
        is_succ = Fun.model_single(FaUserInfo, key)
        return is_succ

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

    def userInforegister(self, _inDict):
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
        checkOutPwd, msg = LoginDal().CheckOutVerifyCode(
            in_ent.code, in_ent.loginName)
        # 失败则退出
        if not msg.IsSuccess or not checkOutPwd:
            return msg
        if len(in_ent.parentArr) < 2:
            return AppReturnDTO(False, "你节点有问题")

        userDal = UserDal()
        if userDal.user_checkLoginExist(in_ent.loginName):
            return AppReturnDTO(False, "{0}已经存在".format(in_ent.loginName))

        # 表示添加已经存在的用户，只需完善资料，并添加登录账号
        loginDal = LoginDal()
        # 添加登录账号
        if "K" in in_ent.parentArr[0] and "V" in in_ent.parentArr[0]:
            
            para = {
                        'userId': int(in_ent.parentArr[0]["K"]),
                        'loginName': in_ent.loginName,
                        'password': in_ent.password,
                        'name': in_ent.parentArr[0]["V"],
                        'level_id': in_ent.level_id,
                        'sex': in_ent.sex,
                        'YEARS_TYPE': in_ent.YEARS_TYPE,
                        'BIRTHDAY_TIME': in_ent.BIRTHDAY_TIME,
                        'birthday_place': in_ent.birthday_place
                    }
            self.FinishUserInfoAndLogin(**para)
            db.session.commit()
            return AppReturnDTO(True)

        parentId = 0
        # 如果有多个父级，都需要每一个每一个用户的添加
        for i in range(len(in_ent.parentArr) - 1, -1, -1):
            parentDict = in_ent.parentArr[i]
            # 跳过包含K的项，因为有K的项是已经存在的，有K表示是下一个的父ID
            if "K" in parentDict and not Fun.IsNullOrEmpty(parentDict["K"]):
                parentId = int(parentDict["K"])
            else:
                # 表示是需要添加的当前用户
                if i == 0:
                    para = {
                        'parentId': parentId,
                        'loginName': in_ent.loginName,
                        'password': in_ent.password,
                        'name': parentDict["V"],
                        'level_id': in_ent.level_id,
                        'sex': in_ent.sex,
                        'YEARS_TYPE': in_ent.YEARS_TYPE,
                        'BIRTHDAY_TIME': in_ent.BIRTHDAY_TIME,
                        'birthday_place': in_ent.birthday_place
                    }
                    self.AddUserInfoAndLogin(**para)
                    db.session.commit()
                    pass
                else:  # 只添加用户名
                    parentEnt, msg = self.AddUserInfoSimple(
                        parentDict["V"], parentId)
                    if not msg.IsSuccess:  #如果失败则退出
                        return msg
                    parentId = parentEnt.ID # 用于下次添加的时候
                    in_ent.parentArr[i]["K"]=parentId # 用于更新，该记录是谁添加和修改的

        return AppReturnDTO(True)

    def FinishUserInfoAndLogin(self, userId, loginName, password, name,
                               level_id, sex, YEARS_TYPE, BIRTHDAY_TIME,
                               birthday_place):
        '完善用户的基本资料以及登录账号'
        # <- 获取添加成功后的Login实体
        loginDal = LoginDal()
        loginDal.LOGIN_NAME = loginName
        loginDal.PASSWORD = password
        loginDal.PHONE_NO = loginName
        loginEng, msg = loginDal.AddLoginName()
        if not msg.IsSuccess:
            return msg
        # ->

        # <- 更新用户信息
        userInfoEnt = FaUserInfo.query.filter(
            FaUserInfo.ID == int(userId)).first()
        if userInfoEnt is None:
            return AppReturnDTO(False, "用户的ID有误")
        userInfoEnt.LOGIN_NAME = loginDal.LOGIN_NAME
        userInfoEnt.UPDATE_TIME = datetime.datetime.now()
        userInfoEnt.NAME = name
        # userInfoEnt.NAME = in_ent.parentArr[0]["V"]
        userInfoEnt.LEVEL_ID = level_id
        userInfoEnt.SEX = sex
        userInfoEnt.YEARS_TYPE = YEARS_TYPE
        userInfoEnt.BIRTHDAY_TIME = datetime.datetime.strptime(
            BIRTHDAY_TIME, '%Y-%m-%dT%H:%M:%SZ')
        userInfoEnt.BIRTHDAY_PLACE = birthday_place
        userInfoEnt.DIED_TIME = None
        userInfoEnt.DIED_PLACE = None

    def AddUserInfoAndLogin(self, parentId, loginName, password, name,
                            level_id, sex, YEARS_TYPE, BIRTHDAY_TIME,
                            birthday_place):
        '完善用户的基本资料以及登录账号'

        parentEnt = FaUserInfo.query.filter(FaUserInfo.ID == parentId).first()
        if parentEnt is None:
            return None, AppReturnDTO(False, "父ID有问题")
        # <- 获取添加成功后的Login实体
        loginDal = LoginDal()
        loginDal.LOGIN_NAME = loginName
        loginDal.PASSWORD = password
        loginDal.PHONE_NO = loginName
        loginEng, msg = loginDal.AddLoginName()
        if not msg.IsSuccess:
            return msg
        # ->

        # <- 更新用户信息
        userInfoEnt = FaUserInfo()
        userInfoEnt.ID = Fun.GetSeqId(FaUser)
        userInfoEnt.FATHER_ID = parentId
        userInfoEnt.LOGIN_NAME = loginDal.LOGIN_NAME
        userInfoEnt.UPDATE_TIME = datetime.datetime.now()
        userInfoEnt.NAME = name
        userInfoEnt.LEVEL_ID = level_id
        userInfoEnt.SEX = sex
        userInfoEnt.YEARS_TYPE = YEARS_TYPE
        if not Fun.IsNullOrEmpty(BIRTHDAY_TIME):
            userInfoEnt.BIRTHDAY_TIME = datetime.datetime.strptime(
                BIRTHDAY_TIME, '%Y-%m-%dT%H:%M:%SZ')
        userInfoEnt.BIRTHDAY_PLACE = birthday_place
        userInfoEnt.DIED_TIME = None
        userInfoEnt.DIED_PLACE = None
        userInfoEnt.DISTRICT_ID = parentEnt.DISTRICT_ID
        userInfoEnt.IS_LOCKED = 0
        userInfoEnt.CREATE_TIME = datetime.datetime.now()
        userInfoEnt.LEVEL_ID = 1
        userInfoEnt.STATUS = '正常'
        userInfoEnt.CREATE_USER_NAME = name
        userInfoEnt.CREATE_USER_ID = userInfoEnt.ID
        userInfoEnt.UPDATE_TIME = datetime.datetime.now()
        userInfoEnt.UPDATE_USER_NAME = name
        db.session.add(userInfoEnt)
        return userInfoEnt, AppReturnDTO(True)

    def AddUserInfoSimple(self, name, parentId):
        """
        只添加用户的名称和父节点,不会添加登录账号,没提交事务
            :param name: 用户名
            :param parentId:父ID 
        """
        parentEnt = FaUserInfo.query.filter(FaUserInfo.ID == parentId).first()
        if parentEnt is None:
            return None, AppReturnDTO(False, "父ID有问题")

        userInfoEnt = FaUserInfo()
        userInfoEnt.ID = Fun.GetSeqId(FaUser)
        userInfoEnt.NAME = name
        userInfoEnt.FATHER_ID = parentId
        userInfoEnt.DISTRICT_ID = parentEnt.DISTRICT_ID
        userInfoEnt.IS_LOCKED = 0
        userInfoEnt.CREATE_TIME = datetime.datetime.now()
        userInfoEnt.LEVEL_ID = 1
        userInfoEnt.STATUS = '正常'
        userInfoEnt.CREATE_USER_NAME = '自动'
        userInfoEnt.CREATE_USER_ID = '1'
        userInfoEnt.UPDATE_TIME = datetime.datetime.now()
        userInfoEnt.UPDATE_USER_NAME = 'admin'
        db.session.add(userInfoEnt)
        return userInfoEnt, AppReturnDTO(True)
