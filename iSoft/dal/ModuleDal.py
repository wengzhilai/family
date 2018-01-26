from iSoft.entity.model import db, FaModule
import math
from iSoft.model.AppReturnDTO import AppReturnDTO
from iSoft.core.Fun import Fun


class ModuleDal(FaModule):

    def __init__(self):
        pass

    def module_findall(self,pageIndex, pageSize, criterion, where):
        relist,is_succ=Fun.model_findall(FaModule, self, pageIndex, pageSize, criterion, where)
        return relist,is_succ


    def module_Save(self, in_dict, saveKeys):
        relist,is_succ=Fun.model_save(FaModule, self, in_dict, saveKeys)
        return relist,is_succ

    def module_delete(self, key):
        db_ent = FaModule.query.filter(FaModule.ID == key).first()
        if db_ent is not None:
            db.session.delete(db_ent)
        db.session.commit()
        return True,AppReturnDTO(True)
            
