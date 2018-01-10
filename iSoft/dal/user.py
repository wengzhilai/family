from iSoft.entity.model import FaUser
import math

class user(object):
    @staticmethod
    def user_findall(pageIndex, pageSize, criterion, *where):

        relist = FaUser.query

        for item in where:
            relist = relist.filter(item)

        relist = relist.order_by(criterion)
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
