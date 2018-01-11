from iSoft.entity.model import FaModule
from iSoft import db
import math

class module(FaModule):
    
    def __init__(self, in_dict):
        pass

    def module_findall(pageIndex, pageSize, criterion, *where):
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
        max_page = math.ceil(num / pageSize)  #向上取整
        if pageIndex > max_page:
            return None
        relist = relist.paginate(pageIndex, per_page=pageSize)
        return relist
    
    def module_Save(self,in_dict, saveKeys):
        # for item in in_dict:
        #     eval("FaModule."+item+"=\""+in_dict[item]+"\"")

        db_ent=FaModule.query.filter_by(ID=in_dict["ID"]).first()
        
        if db_ent is None:
            for item in in_dict:
                setattr(self, item, in_dict[item])
            db.session.add(self)
        else:
            for item in saveKeys:
                setattr(db_ent,item,in_dict[item])

        db.session.commit()
        return True
            
        
        
        

