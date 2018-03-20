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
from iSoft.entity.model import FaUser, FaModule, FaUserInfo
from iSoft.dal.LoginDal import LoginDal
import datetime
from iSoft.core.AlchemyEncoder import AlchemyEncoder
import json


class UserInfoDal(FaUserInfo):
    FatherName=""
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

    def userInfo_SingleByName(self,name):
        relist = FaUserInfo.query.filter(FaUserInfo.NAME.like("%{}%".format(name)))
        relist = relist.paginate(1, per_page=10).items
        relistNew=[]
        for item in relist:
            tmp = UserInfoDal()
            tmp.__dict__ = item.__dict__
            tmp.FatherName=item.parent.NAME
            relistNew.append(tmp)
        return relistNew, AppReturnDTO(True)

