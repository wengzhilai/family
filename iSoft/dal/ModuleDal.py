from iSoft.entity.model import db, FaModule
import math
from iSoft.model.AppReturnDTO import AppReturnDTO
from iSoft.core.Fun import Fun


class ModuleDal(FaModule):

    def __init__(self):
        pass

    def module_findall(self,pageIndex, pageSize, criterion, where):
        relist,is_succ=Fun.model_findall(FaModule, pageIndex, pageSize, criterion, where)
        return relist,is_succ


    def module_Save(self, in_dict, saveKeys):
        relist,is_succ=Fun.model_save(FaModule, self, in_dict, saveKeys)
        return relist,is_succ

    def module_delete(self, key):
        is_succ=Fun.model_delete(FaModule, key)
        return is_succ

    def module_single(self, key):
        relist,is_succ=Fun.model_single(FaModule, key)
        return relist,is_succ

            
