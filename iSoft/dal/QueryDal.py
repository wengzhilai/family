from iSoft.entity.model import db, FaQuery
import math
import json
from iSoft.model.AppReturnDTO import AppReturnDTO
from iSoft.core.Fun import Fun
import re


class QueryDal(FaQuery):
    def __init__(self):
        pass

    def query_findall(self, pageIndex, pageSize, criterion, where):
        relist, is_succ = Fun.model_findall(FaQuery, pageIndex, pageSize,
                                            criterion, where)
        return relist, is_succ

    def query_Save(self, in_dict, saveKeys):

        jsonStr = re.sub(r'\r|\n| ', "", in_dict["QUERY_CFG_JSON"])
        jsonStr = re.sub(r'"onComponentInitFunction"((.|\n)+?)},', "", jsonStr)
        jsonStr = re.sub(r',},', ",", jsonStr)
        try:
            x = json.loads(jsonStr)
        except :
            return None, AppReturnDTO(False, "列配置信息有误")

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
    def query_queryByCode(self, code, pageIndex, pageSize, criterion, where):

        sql, cfg, msg = self.query_GetSqlByCode(code, criterion, where)
        if not msg.IsSuccess:
            return sql, msg
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

        pageSql = "{0} LIMIT {1},{2}".format(sql, (pageIndex - 1) * pageSize,
                                             pageSize)

        allData, msg = Fun.sql_to_dict(pageSql)
        if msg.IsSuccess:
            msg.Msg = num
        # relist = relist.paginate(pageIndex, per_page=pageSize).items
        return allData, msg

    def query_GetSqlByCode(self, code, criterion, where):
        """
        根据查询代码运算出查询的SQL
        用于导出数据，并统一管理配置的SQL
        返回SQL和配置
        """
        db_ent = FaQuery.query.filter(FaQuery.CODE == code).first()
        if db_ent is None:
            return "", "", AppReturnDTO(False, "代码不存在")

        sql = db_ent.QUERY_CONF
        orderArr = []
        for order in criterion:
            orderArr.append("T.%(Key)s %(Value)s" % order)

        whereArr = []
        for search in where:
            if search["Type"] == "like":
                whereArr.append("T.%(Key)s like ('%%%(Value)s%%')" % search)
            else:
                whereArr.append("T.%(Key)s %(Type)s %(Value)s " % search)

        sql = "SELECT * FROM ({0}) T{1}{2}".format(
            sql,
            " WHERE " + " AND ".join(whereArr) if len(whereArr) > 0 else "",
            " ORDER BY " + " , ".join(orderArr) if len(orderArr) > 0 else "",
        )

        jsonStr = re.sub(r'\r|\n| ', "", db_ent.QUERY_CFG_JSON)
        jsonStr = re.sub(r'"onComponentInitFunction"((.|\n)+?)},', "", jsonStr)
        jsonStr = re.sub(r',},', ",", jsonStr)
        return sql, json.loads(jsonStr), AppReturnDTO(True)
