# file: login.py
'''首页'''
from iSoft.core.Fun import Fun
from iSoft import auth, login_manager, app
from flask import request, flash, g
from iSoft.dal.LoginDal import LoginDal
from iSoft.dal.FileDal import FileDal
import iSoft.entity.model
from iSoft.model.AppReturnDTO import AppReturnDTO
from iSoft.core.AlchemyEncoder import AlchemyEncoder
import json
import random  # 生成随机数
from iSoft.model.framework.RequestSaveModel import RequestSaveModel
import iSoft.core.LunarDate
import datetime
import time
import os


@app.route('/Api/Public/SendCode', methods=['GET', 'POST'])
def ApiPublicSendCode():
    '''
    发送短信:RequestSaveModel对象，其中Data里包括phone
    '''
    j_data, msg = Fun.post_to_dict(request)
    if j_data is None:
        return Fun.class_to_JsonStr(msg)

    postEnt = RequestSaveModel(j_data)
    if postEnt is None or postEnt.Data is None:
        return Fun.class_to_JsonStr(AppReturnDTO(False, "参数有问题"))

    if "phoneNum" not in postEnt.Data or postEnt.Data["phoneNum"] is None or postEnt.Data["phoneNum"] == "":
        return Fun.class_to_JsonStr(AppReturnDTO(False, "没有获取phoneNum的值"))

    # 生成随机代码
    code = random.randint(1000, 9999)
    dal = LoginDal()
    re_ent = dal.UpdateCode(postEnt.Data["phoneNum"], code)
    re_ent.Data = code
    return json.dumps(Fun.convert_to_dict(re_ent))


@app.route('/Api/Public/GetLunarDate', methods=['GET', 'POST'])
def ApiPublicGetLunarDate():
    j_data, msg = Fun.post_to_dict(request)
    if j_data is None:
        return Fun.class_to_JsonStr(msg)
    postEnt = RequestSaveModel(j_data)
    if postEnt is None or postEnt.Data is None:
        return Fun.class_to_JsonStr(AppReturnDTO(False, "参数有问题"))

    t = time.strptime(postEnt.Data["Data"], "%Y-%m-%d")
    y, m, d = t[0:3]
    reStr = iSoft.core.LunarDate.LunarDate.fromSolarDate(y, m, d)
    reStr = "{0}-{1}-{2}".format(reStr.year, reStr.month, reStr.day)
    return Fun.class_to_JsonStr(AppReturnDTO(True, reStr))


@app.route('/Api/Public/GetSolarDate', methods=['GET', 'POST'])
def ApiPublicGetSolarDate():
    j_data, msg = Fun.post_to_dict(request)
    if j_data is None:
        return Fun.class_to_JsonStr(msg)
    postEnt = RequestSaveModel(j_data)
    if postEnt is None or postEnt.Data is None:
        return Fun.class_to_JsonStr(AppReturnDTO(False, "参数有问题"))

    t = time.strptime(postEnt.Data["Data"], "%Y-%m-%d")
    y, m, d = t[0:3]
    reStr = iSoft.core.LunarDate.LunarDate.fromSolarDate(y, m, d)
    reStr = "{0}-{1}-{2}".format(reStr.year, reStr.month, reStr.day)
    return Fun.class_to_JsonStr(AppReturnDTO(True, reStr))


@app.route('/Api/Public/upload', methods=['POST', 'GET'])
@auth.login_required
def ApiPublicUpload():
    if g == None:
        return Fun.class_to_JsonStr(AppReturnDTO(False,"重新登录"))
    if request.method == 'POST':
        f = request.files['file']
        basepath = os.path.dirname(__file__)
        upload_path = os.path.join(basepath, "../static/uploads", f.filename)
        f.save(upload_path)
        addFile = {
            "NAME": f.filename,
            "URL": 'download/uploads/{0}'.format(f.filename),
            "PATH":upload_path,
            "USER_ID":g.current_user.ID,
            "LENGTH":len(f.read()),
            "UPLOAD_TIME":datetime.datetime.now(),
            }
        dal=FileDal()
        re_ent,message=dal.file_Save(addFile,[])
        if message.IsSuccess:
            message.set_data(re_ent)
        return Fun.class_to_JsonStr(message)
    return Fun.class_to_JsonStr(AppReturnDTO(False))