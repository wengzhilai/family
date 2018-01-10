from iSoft.entity.model import FaLogin,FaUser
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer,
                          SignatureExpired, BadSignature)
from iSoft import app
from app.core.model.AppReturnDTO import AppReturnDTO
import json

class Login(FaLogin):
    
    def generate_auth_token(self, expiration=60000):
        '''获取用户的token'''
        ser = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return ser.dumps({'ID':self.ID})    

    @staticmethod
    def verify_auth_token(token):
        '''根据token获取用户'''
        ser = Serializer(app.config['SECRET_KEY'])
        try:
            data = ser.loads(token)
            user = FaUser.query.filter_by(ID=int(data['ID'])).first()
        except SignatureExpired:
            return AppReturnDTO(False, "token已经过期"), None # valid token, but expired
        except BadSignature:
            return AppReturnDTO(False, "token无效"), None # invalid token
        except BaseException:
            return AppReturnDTO(False, "错误"), None
        if user is None:
            return AppReturnDTO(False, "用户不存在"), None
        return AppReturnDTO(True), user    