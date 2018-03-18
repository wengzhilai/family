from iSoft.entity.model import db, FaLogin, FaUser
from iSoft import app
from iSoft.model.AppReturnDTO import AppReturnDTO
import json


class LoginDal(FaLogin):

    def UpdateCode(self, loginName, verifyCode):
        sql = "update fa_login set VERIFY_CODE='{0}' where LOGIN_NAME='{1}'".format(
            verifyCode, loginName)
        resource=db.session.execute(sql)
        updateNum = resource.rowcount
        db.session.close()
        if updateNum !=1:
            return AppReturnDTO(False, "影响数不为1")
        
        return AppReturnDTO(True, "成功")
