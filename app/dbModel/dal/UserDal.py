from app import db
from app.dbModel.models.UserModel import User

def SingleUser(userId):
    user=User.query.filter_by(ID=userId).first();
    return user
def GetAll():
    user=User.query.all()
    return user 

def AddEnt(name):
    user=User()
    user.DISTRICT_ID=1
    user.NAME=name
    db.session.add(user)
    return user 