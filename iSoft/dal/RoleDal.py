import math
from iSoft.entity.model import FaRole,FaUser
from iSoft.model.AppReturnDTO import AppReturnDTO
from iSoft.core.Fun import Fun
from iSoft.entity.model import db
from sqlalchemy.sql import exists
import inspect

class RoleDal(FaRole):
    fa_user_arrid=[] #用于修改角色的用户，多对多的关系

    def __init__(self):
        pass

    def Role_findall(self, pageIndex, pageSize, criterion, where):
        relist,is_succ=Fun.model_findall(FaRole, self, pageIndex, pageSize, criterion, where)
        tmplist=[]
        for target_list in relist:
            tmp=RoleDal()
            tmp.__dict__=target_list.__dict__
            userId=[x.ID for x in target_list.fa_user]
            tmp.fa_user_arrid=userId
            tmplist.append(tmp)

        return tmplist, is_succ

    def Role_Save(self, in_dict, saveKeys):
        db_ent = FaRole.query.filter(FaRole.ID == in_dict["ID"]).first()        
        if db_ent is None:
            db_ent = self
            for item in in_dict:
                setattr(db_ent, item, in_dict[item])
            if db_ent.ID is None or db_ent.ID == 0 or db_ent.ID == '0':
                db_ent.ID=db.session.execute('select nextval("fa_role_seq") seq').fetchall()[0][0]
            db.session.add(db_ent)

        else:
            for item in saveKeys:
                setattr(db_ent, item, in_dict[item])
        db_ent.fa_user=FaUser.query.filter(FaUser.ID.in_(db_ent.fa_user_arrid))    

        db.session.commit()
        return db_ent, AppReturnDTO(True)

    def Role_delete(self, key):
        is_succ=Fun.model_delete(FaRole, self, key)
        return is_succ, is_succ
