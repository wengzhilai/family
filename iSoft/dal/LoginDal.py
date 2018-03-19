from iSoft.entity.model import db, FaLogin, FaUser
from iSoft import app
from iSoft.model.AppReturnDTO import AppReturnDTO
import json
import datetime
import hashlib


class LoginDal(FaLogin):

    def UpdateCode(self, loginName, verifyCode):
        nowTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sql = "update fa_login set VERIFY_CODE='{0}',VERIFY_TIME='{1}',FAIL_COUNT=0 where LOGIN_NAME='{2}'".format(
            verifyCode,nowTime, loginName)
        resource=db.session.execute(sql)
        print(sql)
        updateNum = resource.rowcount
        db.session.commit()
        db.session.close()
        if updateNum !=1:
            return AppReturnDTO(False, "影响数不为1")
        
        return AppReturnDTO(True, "成功")
    
    def ResetPassword(self, VerifyCode, LoginName, NewPwd):
        if not VerifyCode.strip() or not LoginName.strip() or not NewPwd.strip():
            return None, AppReturnDTO(False, "参数有误")

        sql = "select ID from fa_login where VERIFY_CODE='{0}' and LOGIN_NAME='{1}' and FAIL_COUNT<5 and TIMESTAMPDIFF(MINUTE,VERIFY_TIME,NOW())<5 ;".format(VerifyCode, LoginName)
        print(sql)
        resource=db.session.execute(sql)
        dataListToup = resource.fetchall()
        #如果没有找到数据，则在错误次数加1
        if len(dataListToup)!=1 :
            sql = "update fa_login set FAIL_COUNT=FAIL_COUNT+1 where LOGIN_NAME='{0}'".format(LoginName)
            print(sql)
            db.session.execute(sql)
            return None, AppReturnDTO(False, "验证码有误请重新获取")

        sql = "update fa_login set PASSWORD='{1}' where LOGIN_NAME='{0}'".format(LoginName, hashlib.md5(NewPwd.encode('utf-8')).hexdigest())
        print(sql)
        resource=db.session.execute(sql)
        
        updateNum = resource.rowcount
        db.session.commit()
        db.session.close()
        if updateNum !=1:
            return None, AppReturnDTO(False, "影响数不为1")
        
        return None, AppReturnDTO(True, "成功")