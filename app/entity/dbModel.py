'''实体类'''
from app.entity.models.DB_LoginModel import LOGIN
from app.entity.models.DB_UserModel import USER
from app.entity.models.SMS_SEND import SMS_SEND

class db_model(object):
    Login=LOGIN
    User=USER
    SmsSend=SMS_SEND

        