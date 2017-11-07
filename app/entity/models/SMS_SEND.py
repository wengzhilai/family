'''发送短信'''
from app import db, app
from sqlalchemy import Column, Integer, String, DateTime
class SMS_SEND(db.Model):
    '''发送短信'''
    __tablename__ = 'fa_sms_send'
    GUID = db.Column(String(32), primary_key=True)
    MESSAGE_ID = db.Column(Integer)
    PHONE_NO = db.Column(String(50))
    ADD_TIME = db.Column(DateTime)
    SEND_TIME = db.Column(DateTime)
    CONTENT = db.Column(String(500))
    STAUTS = db.Column(String(15))
    TRY_NUM = db.Column(Integer)
    def __repr__(self):
       return 'self.__dir__'