# file: login.py
'''首页'''
from iSoft.core.Fun import Fun
from iSoft import auth, login_manager, app
from flask import request, flash, g
from iSoft.dal.LoginDal import LoginDal
import iSoft.entity.model
from iSoft.model.AppReturnDTO import AppReturnDTO
from iSoft.core.AlchemyEncoder import AlchemyEncoder
import json
import random  # 生成随机数
from iSoft.model.framework.RequestSaveModel import RequestSaveModel


@app.route('/Api/Public/SendCode', methods=['GET', 'POST'])
def Public_SendCode():
    '''
    发送短信:RequestSaveModel对象，其中Data里包括phone
    '''
    j_data = request.json
    if j_data is None:
        return Fun.class_to_JsonStr(AppReturnDTO(False, "参数有误"))
    postEnt = RequestSaveModel(j_data)
    if postEnt is None or postEnt.Data is None:
        return Fun.class_to_JsonStr(AppReturnDTO(False, "参数有问题"))

    if "phoneNum" not in postEnt.Data or postEnt.Data["phoneNum"] is None or postEnt.Data["phoneNum"] =="":
        return Fun.class_to_JsonStr(AppReturnDTO(False, "没有获取phoneNum的值"))
    
    code = random.randint(1000, 9999)
    dal=LoginDal()
    re_ent = dal.UpdateCode(postEnt.Data["phoneNum"],code)
    return json.dumps(Fun.convert_to_dict(re_ent))
