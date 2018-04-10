from iSoft.entity.model import db, FaFile
import math
from iSoft.model.AppReturnDTO import AppReturnDTO
from iSoft.core.Fun import Fun


class FileDal(FaFile):

    def __init__(self):
        pass

    def file_findall(self,pageIndex, pageSize, criterion, where):
        relist,is_succ=Fun.model_findall(FaFile, pageIndex, pageSize, criterion, where)
        return relist,is_succ


    def file_Save(self, in_dict, saveKeys):
        reEnt,is_succ=Fun.model_save(FaFile, self, in_dict, saveKeys)
        return reEnt,is_succ

    def file_delete(self, key):
        is_succ=Fun.model_delete(FaFile, key)
        return is_succ

    def file_single(self, key):
        relist,is_succ=Fun.model_single(FaFile, key)
        return relist,is_succ

            
