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
            db.session.execute('''
                DELETE
                FROM
                    fa_role_module
                WHERE
                    fa_role_module.ROLE_ID = 1
                AND fa_role_module.MODULE_ID IN (8, 9)
            ''')
            
            db.session.execute('''
                INSERT INTO fa_role_module (ROLE_ID, MODULE_ID) 
                    SELECT
                        {0} ROLE_ID,
                        fa_module.ID MODULE_ID
                    FROM
                        fa_module
                    WHERE
                        fa_module.ID IN ({1})
                    AND NOT EXISTS (
                        SELECT
                            *
                        FROM
                            fa_role_module
                        WHERE
                            ROLE_ID = {0}
                        AND MODULE_ID = fa_module.ID
                    )
             '''.format(relist.ID, in_dict.moduleIdStr)).fetchall()[0][0]

        return relist, is_succ

    def Role_delete(self, key):
        is_succ = Fun.model_delete(FaRole, key)
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
