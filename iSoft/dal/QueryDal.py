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

    def query_singleByCode(self, code):
        db_ent = FaQuery.query.filter(FaQuery.CODE == code).first()
        if db_ent is None :
            return db_ent, AppReturnDTO(False,"代码不存在")
        
        return db_ent, AppReturnDTO(True)
    
    #查看数据
    def query_queryByCode(model,code, pageIndex, pageSize, criterion, where):
        
        db_ent = FaQuery.query.filter(FaQuery.CODE == code).first()
        if db_ent is None :
            return db_ent, AppReturnDTO(False,"代码不存在")

        relist= db.session.execute(db_ent.QUERY_CONF)
        allData=[]
        for row in relist:
            allData.append(row.items())

        num = relist.rowcount
        if pageIndex < 1:
            pageSize = 1
        if pageSize < 1:
            pageSize = 10
        # 最大页码
        max_page = math.ceil(num / pageSize)  # 向上取整
        if pageIndex > max_page:
            return None, AppReturnDTO(True, num)
       
        # relist = relist.paginate(pageIndex, per_page=pageSize).items
        return allData, AppReturnDTO(True, num)