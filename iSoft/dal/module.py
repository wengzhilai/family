from iSoft.entity.model import FaModule
from iSoft import db
import math
from iSoft.core.model.AppReturnDTO import AppReturnDTO


class module(FaModule):

    def __init__(self):
        pass

    def module_findall(self,pageIndex, pageSize, criterion, *where):
        relist = FaModule.query
        for item in where:
            relist = relist.filter(item)

        for item in criterion:
            relist = relist.order_by(item)
        num = relist.count()
        if pageIndex < 1:
            pageSize = 1
        if pageSize < 1:
            pageSize = 10
        # 最大页码
        max_page = math.ceil(num / pageSize)  # 向上取整
        if pageIndex > max_page:
            return None
        relist = relist.paginate(pageIndex, per_page=pageSize).items
        return relist,AppReturnDTO(True)

    # {
    #     "SaveKeys":["NAME","CODE","IS_DEBUG","SHOW_ORDER"],
    #     "Data":{
    #         "ID":"1",
    #         "NAME":"系统管理",
    #         "IS_DEBUG":0,
    #         "IS_HIDE":0,
    #         "SHOW_ORDER":3,
    #         "CODE":"aaaaa"
    #     }
    # }
    def module_Save(self, in_dict, saveKeys):
        db_ent = FaModule.query.filter(FaModule.ID == in_dict["ID"]).first()
        if db_ent is None:
            db_ent=self
            for item in in_dict:
                setattr(db_ent, item, in_dict[item])
            db.session.add(db_ent)

        else:
            for item in saveKeys:
                setattr(db_ent, item, in_dict[item])

        db.session.commit()
        return db_ent,AppReturnDTO(True)


    def module_delete(self, key):
        db_ent = FaModule.query.filter(FaModule.ID == key).first()
        if db_ent is not None:
            db.session.delete(db_ent)
        db.session.commit()
        return True,AppReturnDTO(True)
            
