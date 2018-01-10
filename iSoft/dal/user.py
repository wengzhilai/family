from iSoft.entity.model import FaUser


class user(object):

    def user_findall(self, pageIndex, pageSize):
        relist=FaUser.query.paginate(pageIndex,per_page=pageSize)
        return relist
