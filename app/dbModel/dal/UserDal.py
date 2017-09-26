from app import db
from app.dbModel.models.DB_UserModel import User
from app.core.model.LogingModel import LogingModel
from app.core.model.AppReturnDTO import AppReturnDTO
class UserDal(object):
    @staticmethod
    def UserLogin(_inEnt):
        inEnt=LogingModel()
        inEnt.__dict__=_inEnt
        if inEnt.loginName==None or inEnt.loginName=='':
            return (AppReturnDTO(False,"用户名和密码不能为空"),None)

        return (AppReturnDTO(True,"登录成功"),None)
        
        
    @staticmethod
    def SingleUser(userId):
        user=User.query.filter_by(ID=userId).first();
        return user
    def GetAll():
        user=User.query.all()
        return user 

    @staticmethod
    def AddEnt(name):
        user=User()
        user.DISTRICT_ID=1
        user.NAME=name
        db.session.add(user)
        return user 