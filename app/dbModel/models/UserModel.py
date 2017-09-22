#!~/app\db\model\UserModel.py
#Filename:UserModel.py
'''
用户对象
'''
from app import db
from flask_login import UserMixin
import datetime
class User(db.Model,UserMixin):
    __tablename__ = 'YL_USER'
    ID = db.Column(db.Integer, primary_key=True)
    NAME = db.Column(db.String)
    LOGIN_NAME = db.Column(db.String)
    ICON_FILES_ID = db.Column(db.Integer)
    DISTRICT_ID = db.Column(db.Integer)
    IS_LOCKED = db.Column(db.Integer)
    CREATE_TIME = db.Column(db.DateTime)
    LOGIN_COUNT = db.Column(db.Integer)
    LAST_LOGIN_TIME = db.Column(db.DateTime)
    LAST_LOGOUT_TIME = db.Column(db.DateTime)
    LAST_ACTIVE_TIME = db.Column(db.DateTime)
    REMARK = db.Column(db.String)
    def __repr__(self):
       return 'self.__dir__'
    def is_authenticated(self):
            return True

    def is_actice(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return "1"
        