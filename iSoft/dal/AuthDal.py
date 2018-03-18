from iSoft.entity.model import FaLogin,FaUser
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer,
                          SignatureExpired, BadSignature)
from iSoft import app
from iSoft.model.AppReturnDTO import AppReturnDTO
import json

class AuthDal(FaLogin):
    
    @staticmethod
    def generate_auth_token(userObj, expiration=60000):
        '''获取用户的token'''
        ser = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return ser.dumps({'ID':userObj.ID})    

    @staticmethod
    def verify_auth_token(token):
        '''根据token获取用户'''
        ser = Serializer(app.config['SECRET_KEY'])
        try:
            data = ser.loads(token)
            if not isinstance(data['ID'],int) :
                return AppReturnDTO(False, "登录超时"), None # valid token, but expired
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

    @staticmethod
    def login_out():
        '''退出登录'''
        return AppReturnDTO(True)

    @staticmethod
    def verify_auth_token(token):
        '''验证token'''
        return Fun.verify_auth_token(token)

    @staticmethod
    def login_reg(_inent):
        '''注册用户'''

        in_ent = LogingModel()
        in_ent.__dict__ = _inent
        if in_ent.loginName is None or in_ent.loginName == '':
            return AppReturnDTO(False, "电话号码不能为空")
        if not Fun.is_phonenum(in_ent.loginName):
            return AppReturnDTO(False, "电话号码格式不正确")

        complexity = Fun.password_complexity(in_ent.password)
        if complexity < PASSWORD_COMPLEXITY:
            return AppReturnDTO(False, "密码复杂度不够:" + str(complexity))
        return AppReturnDTO(False, "暂不开放注册")