from iSoft.entity.model import db, FaQuery
import math
from iSoft.model.AppReturnDTO import AppReturnDTO
from iSoft.core.Fun import Fun


class QueryDal(FaQuery):

    def __init__(self):
        pass

    def query_findall(self,pageIndex, pageSize, criterion, where):
        relist,is_succ=Fun.model_findall(FaQuery, pageIndex, pageSize, criterion, where)
        return relist,is_succ


    def query_Save(self, in_dict, saveKeys):
        relist,is_succ=Fun.model_save(FaQuery, self, in_dict, saveKeys)
        return relist,is_succ

    def query_delete(self, key):
        is_succ=Fun.model_delete(FaQuery, key)
        return is_succ

    def query_single(self, key):
        relist,is_succ=Fun.model_single(FaQuery, key)
        return relist,is_succ

            
