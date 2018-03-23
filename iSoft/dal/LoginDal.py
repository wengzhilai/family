from iSoft.entity.model import db, FaLogin, FaUser
from iSoft import app
from iSoft.model.AppReturnDTO import AppReturnDTO
import json
import datetime
import hashlib
from iSoft.core.Fun import Fun


class LoginDal(FaLogin):

    def UpdateCode(self, loginName, verifyCode):
        '更新短验证码，如果号码不存在，则添加新有号码'
        loginEnt=FaLogin.query.filter(FaLogin.LOGIN_NAME==loginName).first()
        if loginEnt is None:
            loginEnt=self
            loginEnt.LOGIN_NAME=loginName
            loginEnt.VERIFY_CODE=verifyCode
            loginEnt.ID=Fun.GetSeqId(self)
            loginEnt.FAIL_COUNT=0
            loginEnt.VERIFY_TIME=datetime.datetime.now()
            db.session.add(loginEnt)
        else:
            loginEnt.VERIFY_CODE=verifyCode
            loginEnt.FAIL_COUNT=0
            loginEnt.VERIFY_TIME=datetime.datetime.now()
        db.session.commit()
        db.session.close()
        return AppReturnDTO(True, "成功")

    def CheckOutVerifyCode(self, VerifyCode, LoginName):
        '''验证短信验证码是否正确'''
        if not VerifyCode.strip() or not LoginName.strip():
            return False, AppReturnDTO(False, "参数有误")

        sql = "select ID from fa_login where VERIFY_CODE='{0}' and LOGIN_NAME='{1}' and FAIL_COUNT<5 and TIMESTAMPDIFF(MINUTE,VERIFY_TIME,NOW())<5 ;".format(
            VerifyCode, LoginName)
        print(sql)
        resource = db.session.execute(sql)
        dataListToup = resource.fetchall()

        # 如果只有一条，表示成功，则退出
        if len(dataListToup) == 1:
            return True, AppReturnDTO(True)
        # 失败后添加一条失败记录
        sql = "update fa_login set FAIL_COUNT=FAIL_COUNT+1 where LOGIN_NAME='{0}'".format(
            LoginName)
        print(sql)
        db.session.execute(sql)
        db.session.commit()

        return False, AppReturnDTO(False, "验证码有误请重新获取")

    def ResetPassword(self, VerifyCode, LoginName, NewPwd):
        '重设置密码'
        checkOutPwd, msg = self.CheckOutVerifyCode(VerifyCode, LoginName)
        # 失败则退出
        if not msg.IsSuccess or not checkOutPwd:
            return None, msg

        sql = "update fa_login set PASSWORD='{1}' where LOGIN_NAME='{0}'".format(
            LoginName, hashlib.md5(NewPwd.encode('utf-8')).hexdigest())
        print(sql)
        resource = db.session.execute(sql)

        updateNum = resource.rowcount
        db.session.commit()
        db.session.close()
        if updateNum != 1:
            return None, AppReturnDTO(False, "影响数不为1")

        return None, AppReturnDTO(True, "成功")

    def AddLoginName(self):
        '''添加账号'''
        if self.LOGIN_NAME == None or self.LOGIN_NAME == "":
            return None, AppReturnDTO(False, "账号不能为空")
        if self.PASSWORD == None or self.PASSWORD == "":
            return None, AppReturnDTO(False, "密码不能为空")
        db_ent = FaLogin.query.filter(
            FaLogin.LOGIN_NAME == self.LOGIN_NAME).first()
        if db_ent is not None:
            return db_ent, AppReturnDTO(True, "该登录名已经存在")
        self.IS_LOCKED = 0
        self.ID = Fun.GetSeqId(self)
        self.REGION = 0
        self.FAIL_COUNT = 0
        self.PASSWORD = Fun.md5(self.PASSWORD)
        db.session.add(self)
        return self, AppReturnDTO(True)
