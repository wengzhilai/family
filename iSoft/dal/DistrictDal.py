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
        newParent = None
        saveKeys.append("ID_PATH")
        saveKeys.append("REGION")
        if "PARENT_ID" not in in_dict or in_dict["PARENT_ID"] is None:
            in_dict["LEVEL_ID"] = 0
            in_dict["ID_PATH"] = "."
            in_dict["REGION"] = 0
        else:
            newParent, is_succ = self.district_single(in_dict["PARENT_ID"])
            if newParent is None:
                return None, AppReturnDTO(False, "上级节点有误")
            in_dict["LEVEL_ID"] = newParent.LEVEL_ID + 1
            in_dict["ID_PATH"] = "{0}{1}.".format(newParent.ID_PATH,in_dict["PARENT_ID"])
            in_dict["REGION"] = newParent.REGION
            pass
        #用于更新所有子节点的ID_PATH,如果修改过parent_id的话
        if "ID" in in_dict and in_dict["ID"] is not None and in_dict["ID"] != 0:
            if str(in_dict["ID"]) == str(in_dict["PARENT_ID"]):
                return None, AppReturnDTO(False, "上级不能选择自己")
            sql = "SELECT ID FROM fa_district WHERE ID_PATH LIKE '%.{0}.%'".format(in_dict["ID"])
            childListTuple = db.session.execute(sql).fetchall()
            childList = [item[0] for item in childListTuple]

            if int(in_dict["PARENT_ID"]) in childList:
                return None, AppReturnDTO(False, "上级不能自己子集")
            nowEnt = FaDistrict.query.filter(
                FaDistrict.ID == in_dict["ID"]).first()

            #如果PARENT_ID没有变化则不执行下面语句
            if nowEnt.PARENT_ID != in_dict["PARENT_ID"]:
                if nowEnt is None:
                    return None, AppReturnDTO(False, "ID有误")

                updateSql = "UPDATE fa_district SET ID_PATH= '{0}{1}.' WHERE ID_PATH LIKE '%{2}{1}.%'"
                updateSql = updateSql.format(in_dict["ID_PATH"], nowEnt.ID,
                                             nowEnt.ID_PATH)
                print(updateSql)
                db.session.execute(updateSql)

        relist, is_succ = Fun.model_save(FaDistrict, self, in_dict, saveKeys)

        return relist, is_succ

    def district_delete(self, key):
        is_succ = Fun.model_delete(FaDistrict, key)
        return is_succ

    def district_single(self, key):
        relist, is_succ = Fun.model_single(FaDistrict, key)
        return relist, is_succ
