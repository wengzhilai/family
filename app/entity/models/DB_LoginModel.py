'''
使用账号
'''
from app import db

class LOGIN(db.Model):
    '''user 用户'''
    __tablename__ = 'FA_LOGIN'
    ID = db.Column(db.Integer, primary_key=True)
    LOGIN_NAME = db.Column(db.String)
    PASSWORD = db.Column(db.String)
    PHONE_NO = db.Column(db.String)
    EMAIL_ADDR = db.Column(db.String)
    VERIFY_CODE = db.Column(db.String)
    VERIFY_TIME = db.Column(db.DateTime)
    IS_LOCKED = db.Column(db.Integer)
    PASS_UPDATE_DATE = db.Column(db.DateTime)
    LOCKED_REASON = db.Column(db.String)
    FAIL_COUNT = db.Column(db.Integer)
