# file: login.py
'''首页'''
from iSoft.core.Fun import Fun
from iSoft import auth, login_manager, app
import iSoft.entity.model
from flask import send_file, make_response, send_from_directory, request, g

from iSoft.dal.FamilyDal import FamilyDal
from iSoft.dal.UserInfoDal import UserInfoDal
from iSoft.model.AppReturnDTO import AppReturnDTO
from iSoft.core.AlchemyEncoder import AlchemyEncoder
import json
import random  # 生成随机数
from iSoft.model.framework.RequestSaveModel import RequestSaveModel
from iSoft.model.framework.PostBaseModel import PostBaseModel


@app.route('/Api/Family/UserInfoRelative', methods=['GET', 'POST'])
@auth.login_required
def ApiFamilyUserInfoRelative():
    '''
    重置密码:RequestSaveModel对象，其中Data里包括VerifyCode，LoginName、NewPwd
    '''
    if g is None:
        return Fun.class_to_JsonStr(AppReturnDTO(False, "没有登录"))

    j_data, message = Fun.post_to_dict(request)
    if j_data is None:
        return Fun.class_to_JsonStr(message)
    in_ent = PostBaseModel(j_data)
    
    dal=FamilyDal()
    # 如果没有传值，则显示当前用户的ID
    if Fun.IsNullOrEmpty(in_ent.Key):
        in_ent.Key=g.current_user.ID

    re_ent,message= dal.UserInfoRelative(in_ent.Key)
    if message.IsSuccess:
        message.Data=re_ent.__dict__
    return Fun.class_to_JsonStr(message)

