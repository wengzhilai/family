from iSoft.entity.model import db, FaQuery
import math
from iSoft.model.AppReturnDTO import AppReturnDTO
from iSoft.core.Fun import Fun


class QueryDal(FaQuery):

    def __init__(self):
        pass

    def query_findall(self, pageIndex, pageSize, criterion, where):
        relist, is_succ = Fun.model_findall(
            FaQuery, pageIndex, pageSize, criterion, where)
        return relist, is_succ

    def query_Save(self, in_dict, saveKeys):
        relist, is_succ = Fun.model_save(FaQuery, self, in_dict, saveKeys)
        return relist, is_succ

    def query_delete(self, key):
        is_succ = Fun.model_delete(FaQuery, key)
        return is_succ

    def query_single(self, key):
        relist, is_succ = Fun.model_single(FaQuery, key)
        return relist, is_succ

    def query_singleByCode(self, code):
        db_ent = FaQuery.query.filter(FaQuery.CODE == code).first()
        if db_ent is None:
            return db_ent, AppReturnDTO(False, "代码不存在")

        return db_ent, AppReturnDTO(True)

    # 查看数据
    def query_queryByCode(model, code, pageIndex, pageSize, criterion, where):

        db_ent = FaQuery.query.filter(FaQuery.CODE == code).first()
        if db_ent is None:
            return db_ent, AppReturnDTO(False, "代码不存在")

        sql = db_ent.QUERY_CONF
        relist = db.session.execute(sql)
        num = relist.rowcount
        relist.close()
        if pageIndex < 1:
            pageSize = 1
        if pageSize < 1:
            pageSize = 10
        # 最大页码
        max_page = math.ceil(num / pageSize)  # 向上取整
        if pageIndex > max_page:
            return None, AppReturnDTO(True, num)
        orderArr = []
        for order in criterion:
            orderArr.append("T.%(Key)s %(Value)s" % order)

        whereArr = []
        for search in where:
            if search["Type"] == "like":
                whereArr.append("T.%(Key)s like ('%%%(Value)s%%')" % search)
            else:
                whereArr.append("T.%(Key)s %(Type)s %(Value)s " % search)

        sql = "SELECT * FROM ({0}) T{1}{2} LIMIT {3},{4}".format(
            sql,
            " WHERE " + " AND ".join(whereArr) if len(whereArr) > 0 else "",
            " ORDER BY " + " , ".join(orderArr) if len(orderArr) > 0 else "",
            (pageIndex - 1) * pageSize,
            pageSize
        )
        relist = db.session.execute(sql)
        allData = []
        for row in relist:
            tmpDic = {}
            for dic in row.items():
                tmpDic[dic[0]] = dic[1]

            allData.append(tmpDic)

        # relist = relist.paginate(pageIndex, per_page=pageSize).items
        return allData, AppReturnDTO(True, num)
