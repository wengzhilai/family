from iSoft.entity.model import db, FaUser, FaModule, FaRole
import math
from iSoft.core.model.AppReturnDTO import AppReturnDTO


class user(object):
    @staticmethod
    def user_findall(pageIndex, pageSize, criterion, *where):

        relist = FaUser.query
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
        return relist, AppReturnDTO(True)

    def user_all_module(self,userId):
        db_ent = FaUser.query.filter(FaUser.ID == userId).first()

        if db_ent is not None:
            allRoleList=FaRole.query.filter(FaRole.fa_user.query.fillter(FaUser.ID==userId)).all()
            roleIdList = [item.ID for item in db_ent.fa_role]
            allModuleList = FaModule.query.filter(FaModule.fa_role.query.filter(FaRole.ID.in_(roleIdList)).count()>0).findall()
            return AppReturnDTO(True,"",allModuleList)
        return AppReturnDTO(True)
