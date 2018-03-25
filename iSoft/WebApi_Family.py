# file: login.py
'''首页'''
from iSoft.core.Fun import Fun
from iSoft import auth, login_manager, app
import iSoft.entity.model
from flask import send_file, make_response, send_from_directory, request, g

from iSoft.dal.FamilyDal import FamilyDal
from iSoft.model.AppReturnDTO import AppReturnDTO
from iSoft.core.AlchemyEncoder import AlchemyEncoder
import json
import random  # 生成随机数
from iSoft.model.framework.RequestSaveModel import RequestSaveModel


@app.route('/Api/Family/UserInfoRelative', methods=['GET', 'POST'])
@auth.login_required
def ApiFamilyUserInfoRelative():
    '''
    重置密码:RequestSaveModel对象，其中Data里包括VerifyCode，LoginName、NewPwd
    '''
    if g is None:
        return Fun.class_to_JsonStr(AppReturnDTO(False, "没有登录"))
    dal=FamilyDal()
    ent,msg= dal.UserInfoRelative(g.current_user.ID)
    return Fun.class_to_JsonStr(msg)