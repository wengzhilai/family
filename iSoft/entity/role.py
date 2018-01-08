from iSoft.entity.model import FaUser, FaRole, FaUserInfo

class RoleDal(object):
    @staticmethod
    def GetAll():
        # all = FaRole.query.filter_by(ID=4 , NAME='系统管理员5').all()
        all = FaUser.query.filter(FaUser.ID < 10).all()
        for item in all:
            print(item.fa_district.NAME)
        return all
