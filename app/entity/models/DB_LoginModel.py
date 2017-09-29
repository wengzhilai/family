'''
使用账号
'''
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer,
                          SignatureExpired, BadSignature)
from app import db, app
from app.core.model.AppReturnDTO import AppReturnDTO

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

    def generate_auth_token(self, expiration=600):
        '''获取用户的token'''
        ser = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return ser.dumps({'ID':self.ID})

    @staticmethod
    def verify_auth_token(token):
        '''根据token获取用户'''
        ser = Serializer(app.config['SECRET_KEY'])
        try:
            data = ser.loads(token)
            user = LOGIN.query.filter_by(ID=data['ID']).first()
        except SignatureExpired:
            return AppReturnDTO(False, "token已经过期"), None # valid token, but expired
        except BadSignature:
            return AppReturnDTO(False, "token无效"), None # invalid token
        except BaseException:
            return AppReturnDTO(False, "错误"), None
        if user is None:
            return AppReturnDTO(False, "用户不存在"), None
        return AppReturnDTO(True), user

    def can(self, permission):
        '''判断用户是否具备某权限'''
        return True, permission

    def is_adminstractor(self):
        '''判断用户是否具备管理员权限'''
        return self.can(True)