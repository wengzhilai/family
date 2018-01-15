import math
from iSoft.entity.model import FaRole, Sequence, db
from iSoft.core.model.AppReturnDTO import AppReturnDTO
from iSoft.core.Fun import Fun


class Role(FaRole):

    def __init__(self):
        pass

    def Role_findall(self, pageIndex, pageSize, criterion, where):
        relist,is_succ=Fun.model_findall(FaRole, self, pageIndex, pageSize, criterion, where)
        return relist, AppReturnDTO(is_succ)

    def Role_Save(self, in_dict, saveKeys):
        relist,is_succ=Fun.model_save(FaRole, self, in_dict, saveKeys)
        return relist, AppReturnDTO(is_succ)

    def Role_delete(self, key):
        is_succ=Fun.model_delete(FaRole, self, key)
        return is_succ, AppReturnDTO(is_succ)
