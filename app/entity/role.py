'''
角色
'''
from app.entity.model import FaRole

class RoleDal(object):
    @staticmethod
    def GetAll():
        all = FaRole.query.all()
        return all   
                