from iSoft.entity.model import db, FaDistrict
import math
from iSoft.model.AppReturnDTO import AppReturnDTO
from iSoft.core.Fun import Fun


class DistrictDal(FaDistrict):
    def __init__(self):
        pass

    def district_findall(self, pageIndex, pageSize, criterion, where):
        relist, is_succ = Fun.model_findall(FaDistrict, pageIndex, pageSize,
                                            criterion, where)
        return relist, is_succ

    def district_Save(self, in_dict, saveKeys):
        if "PARENT_ID" not in in_dict or in_dict["PARENT_ID"] is None:
            in_dict["LEVEL_ID"] = 0
            in_dict["ID_PATH"] = "."
            in_dict["REGION"] = 0
        else:
            single, is_succ = self.district_single(in_dict["PARENT_ID"])
            if single is None:
                return None, AppReturnDTO(False, "上级节点有误")
            in_dict["LEVEL_ID"] = single.LEVEL_ID + 1
            in_dict["ID_PATH"] = single.ID_PATH + in_dict["PARENT_ID"] + "."
            in_dict["REGION"] = single.REGION
            pass

        relist, is_succ = Fun.model_save(FaDistrict, self, in_dict, saveKeys)
        return relist, is_succ

    def district_delete(self, key):
        is_succ = Fun.model_delete(FaDistrict, key)
        return is_succ

    def district_single(self, key):
        relist, is_succ = Fun.model_single(FaDistrict, key)
        return relist, is_succ
