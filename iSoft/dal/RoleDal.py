import math
from iSoft.entity.model import FaRole, FaUser, FaModule
from iSoft.model.AppReturnDTO import AppReturnDTO
from iSoft.core.Fun import Fun
from iSoft.entity.model import db
from sqlalchemy.sql import exists
from iSoft.dal.ModuleDal import ModuleDal
import inspect


class RoleDal(FaRole):
    fa_user_arrid = []  # 用于修改角色的用户，多对多的关系
    moduleIdStr = []  # 模块ID字符串

    def __init__(self):
        pass

    def Role_findall(self, pageIndex, pageSize, criterion, where):
        relist, is_succ = Fun.model_findall(
            FaRole, pageIndex, pageSize, criterion, where)
        return relist, is_succ

    def Role_Save(self, in_dict, saveKeys):
        relist, is_succ = Fun.model_save(FaRole, self, in_dict, saveKeys)

        if is_succ.IsSuccess:  # 表示已经添加成功角色
            sqlStr='''
                DELETE
                FROM
                    fa_role_module
                WHERE
                    fa_role_module.ROLE_ID = {0}
            '''.format(relist.ID)
            print(sqlStr)
            execObj = db.session.execute(sqlStr)
            if len(relist.moduleIdStr)>0:
                sqlStr='''
                    INSERT INTO fa_role_module (ROLE_ID, MODULE_ID) 
                        SELECT
                            {0} ROLE_ID,
                            m.ID MODULE_ID
                        FROM
                            fa_module m
                        WHERE
                            m.ID IN ({1})
                '''.format(relist.ID, ','.join(str(i) for i in relist.moduleIdStr))
                print(sqlStr)
                execObj = db.session.execute(sqlStr)
            db.session.commit()
        return relist, is_succ

    def Role_delete(self, key):
        delSql = 'delete from fa_role_module where ROLE_ID IN ({0})'.format(key)
        print(delSql)
        db.session.execute(delSql)
        delSql = 'delete from fa_role where ID IN ({0})'.format(key)
        print(delSql)
        db.session.execute(delSql)
        db.session.commit()
        return AppReturnDTO(True)
        return is_succ

    def Role_single(self, key):
        relist, is_succ = Fun.model_single(FaRole, key)
        tmp = RoleDal()
        tmp.__dict__ = relist.__dict__
        userId = [x.ID for x in relist.fa_user]
        moduleId = [x.ID for x in relist.fa_modules]
        tmp.fa_user_arrid = userId
        tmp.moduleIdStr = moduleId
        return tmp, is_succ
