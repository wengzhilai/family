import math
from iSoft.entity.model import FaRole,FaUser
from iSoft.model.AppReturnDTO import AppReturnDTO
from iSoft.core.Fun import Fun
from iSoft.entity.model import db
from sqlalchemy.sql import exists
import inspect

class RoleDal(FaRole):
    fa_user_arrid=[] #用于修改角色的用户，多对多的关系
    
    moduleIdStr=[] #模块ID字符串
    def __init__(self):
        pass

    def Role_findall(self, pageIndex, pageSize, criterion, where):
        relist,is_succ=Fun.model_findall(FaRole, pageIndex, pageSize, criterion, where)
        return relist, is_succ

    def Role_Save(self, in_dict, saveKeys):
        relist,is_succ=Fun.model_save(FaRole, self, in_dict, saveKeys)
        return relist,is_succ
    

    def Role_delete(self, key):
        is_succ=Fun.model_delete(FaRole, key)
        return is_succ, is_succ

    def Role_single(self, key):
        relist,is_succ=Fun.model_single(FaRole, key)

        tmp=RoleDal()
        tmp.__dict__=relist.__dict__
        userId=[x.ID for x in relist.fa_user]
        tmp.fa_user_arrid=userId
        return tmp,is_succ