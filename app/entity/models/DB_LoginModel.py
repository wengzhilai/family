'''
使用账号
'''
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature
from app import db,app

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

    def generate_auth_token(self, expiration = 600):
        s = Serializer(app.config['SECRET_KEY'], expires_in = expiration)
        return s.dumps({ 'ID': self.ID })

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token
        user = LOGIN.query.filter_by(ID=data['ID'])
        return user

    def can(self, permission):
        '''判断用户是否具备某权限'''
        return True

    def is_adminstractor(self):
        '''判断用户是否具备管理员权限'''
        return self.can(True)