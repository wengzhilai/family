# file: login.py
'''首页'''
from iSoft.core.Fun import Fun
from iSoft import auth, login_manager, app
from flask import request, flash, g
from iSoft.dal.LoginDal import LoginDal
from iSoft.dal.UserInfoDal import UserInfoDal
from iSoft.dal.UserDal import UserDal
import iSoft.entity.model
from iSoft.model.AppReturnDTO import AppReturnDTO
from iSoft.core.AlchemyEncoder import AlchemyEncoder
import json
import random  # 生成随机数
from iSoft.model.framework.RequestSaveModel import RequestSaveModel


@app.route('/Api/Login/ResetPassword', methods=['GET', 'POST'])
def ApiResetPassword():
    '''
    重置密码:RequestSaveModel对象，其中Data里包括VerifyCode，LoginName、NewPwd
    '''
    j_data, message = Fun.post_to_dict(request)
    if j_data is None:
        return Fun.class_to_JsonStr(message)

    postEnt = RequestSaveModel(j_data)
    if postEnt is None or postEnt.Data is None:
        return Fun.class_to_JsonStr(AppReturnDTO(False, "参数有问题"))

    dal = LoginDal()
    re_ent, message = dal.ResetPassword(
        postEnt.Data["VerifyCode"], postEnt.Data["LoginName"], postEnt.Data["NewPwd"])

    if message.IsSuccess:
        message.set_data(re_ent)
    return json.dumps(Fun.convert_to_dict(message))

@app.route('/Api/UserInfo/SingleByName', methods=['GET', 'POST'])
def UserInfo_SingleByName():
    '''
    根据用户名查询用户:RequestSaveModel对象，其中Data里包括name
    '''
    j_data, message = Fun.post_to_dict(request)
    if j_data is None:
        return Fun.class_to_JsonStr(message)

    postEnt = RequestSaveModel(j_data)
    if postEnt is None or postEnt.Data is None:
        return Fun.class_to_JsonStr(AppReturnDTO(False, "参数有问题"))

    if "name" not in postEnt.Data or Fun.IsNullOrEmpty(postEnt.Data["name"]):
        return Fun.class_to_JsonStr(AppReturnDTO(False, "没有值"))
        
        
    dal = UserInfoDal()
    re_ent, message = dal.userInfo_SingleByName(postEnt.Data["name"])
    if message.IsSuccess:
        message.set_data(re_ent)
    return json.dumps(Fun.convert_to_dict(message))

@app.route('/Api/UserInfo/Register', methods=['GET', 'POST'])
def UserInfo_Register():
    '''
    用于手机端注册用户
    '''
    j_data, message = Fun.post_to_dict(request)
    if j_data is None:
        return Fun.class_to_JsonStr(message)
    postEnt = RequestSaveModel(j_data)
    if postEnt is None or postEnt.Data is None:
        return Fun.class_to_JsonStr(AppReturnDTO(False, "参数有问题"))
    dal=UserInfoDal()
    postEnt =dal.userInfo_register(postEnt.Data)
    return Fun.class_to_JsonStr(postEnt)

@app.route('/Api/auth/UserLogin', methods=['GET', 'POST'])
def auth_UserLogin():
    '''手机用户登录'''
    j_data = request.json 
    if j_data is None:
        return Fun.class_to_JsonStr(AppReturnDTO(False, "参数有误"))
    _model=UserDal()

    ent = _model.user_login(j_data)
    return Fun.class_to_JsonStr(ent)