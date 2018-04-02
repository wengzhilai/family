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

@app.route('/Api/UserInfo/Delete', methods=['GET', 'POST'])
@auth.login_required
def ApiUserInfoDelete():
    '''
    重置密码:RequestSaveModel对象，其中Data里包括VerifyCode，LoginName、NewPwd
    '''
    if g is None:
        return Fun.class_to_JsonStr(AppReturnDTO(False, "没有登录"))

    j_data, message = Fun.post_to_dict(request)
    if j_data is None:
        return Fun.class_to_JsonStr(message)
    in_ent = PostBaseModel(j_data)
    
    if Fun.IsNullOrEmpty(in_ent.Key):
        return Fun.class_to_JsonStr(AppReturnDTO(False, "参数有问题"))

    dal=UserInfoDal()
    delMode,message= dal.userInfo_delete(in_ent.Key)
    if message.IsSuccess:
        message.Data=delMode
    return Fun.class_to_JsonStr(message)

@app.route('/Api/UserInfo/Single', methods=['GET', 'POST'])
@auth.login_required
def ApiUserInfoSingle():
    '''
    重置密码:RequestSaveModel对象，其中Data里包括VerifyCode，LoginName、NewPwd
    '''
    if g is None:
        return Fun.class_to_JsonStr(AppReturnDTO(False, "没有登录"))

    j_data, message = Fun.post_to_dict(request)
    if j_data is None:
        return Fun.class_to_JsonStr(message)
    in_ent = PostBaseModel(j_data)
    
    if Fun.IsNullOrEmpty(in_ent.Key):
        return Fun.class_to_JsonStr(AppReturnDTO(False, "参数有问题"))

    dal=UserInfoDal()
    delMode,message= dal.userInfo_single(in_ent.Key)
    if message.IsSuccess:
        message.set_data(delMode)
    return Fun.class_to_JsonStr(message)

@app.route('/Api/UserInfo/save', methods=['GET', 'POST'])
@auth.login_required
def ApiUserInfoSave():
    j_data = request.json
    if j_data is None:
        return Fun.class_to_JsonStr(AppReturnDTO(False, "参数有误"))
    in_ent = RequestSaveModel(j_data)
    _modele = UserInfoDal()
    re_ent, message = _modele.userInfo_Save(
        in_dict=in_ent.Data, saveKeys=in_ent.SaveKeys)
    if message.IsSuccess:
        message.set_data(re_ent)
    return Fun.class_to_JsonStr(message)

