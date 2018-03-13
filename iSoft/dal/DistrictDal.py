from iSoft.entity.model import db, FaDistrict
import math
from iSoft.model.AppReturnDTO import AppReturnDTO
from iSoft.core.Fun import Fun


class DistrictDal(FaDistrict):

    def __init__(self):
        pass

    def district_findall(self,pageIndex, pageSize, criterion, where):
        relist,is_succ=Fun.model_findall(FaDistrict, pageIndex, pageSize, criterion, where)
        return relist,is_succ


    def district_Save(self, in_dict, saveKeys):
        relist,is_succ=Fun.model_save(FaDistrict, self, in_dict, saveKeys)
        return relist,is_succ

    def district_delete(self, key):
        is_succ=Fun.model_delete(FaDistrict, key)
        return is_succ

    def district_single(self, key):
        relist,is_succ=Fun.model_single(FaDistrict, key)
        return relist,is_succ

            
