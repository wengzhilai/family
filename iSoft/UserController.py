'''用户'''
from iSoft.core.Fun import Fun
from iSoft import auth, login_manager, app
from flask import g, json, request
from iSoft.core.AlchemyEncoder import AlchemyEncoder
from iSoft.model.AppReturnDTO import AppReturnDTO
from iSoft.model.framework.RequestPagesModel import RequestPagesModel
from iSoft.model.framework.RequestSaveModel import RequestSaveModel
from iSoft.model.framework.PostBaseModel import PostBaseModel
from iSoft.entity.model import FaUser
from iSoft.dal.UserDal import UserDal

@app.route('/user/list', methods=['GET', 'POST'])
@auth.login_required
def user_list():
    j_data = request.json
    if j_data is None:
        return Fun.class_to_JsonStr(AppReturnDTO(False, "参数有误"))
    in_ent = RequestPagesModel(j_data)
    where = []
    for search in in_ent.SearchKey:
        if search["Type"]=="like" :
            where.append(eval("FaUser.%(Key)s.like('%%%(Value)s%%')" % search))
        else:
            where.append(eval("FaUser.%(Key)s%(Type)s%(Value)s" % search))

    criterion = []
    for search in in_ent.OrderBy:
        search["Value"] = search["Value"].lower()
        criterion.append(eval("FaUser.%(Key)s.%(Value)s()" % search))

    _modele = UserDal()
    re_ent, message = _modele.user_findall(
        in_ent.PageIndex,
        in_ent.PageSize,
        criterion,
        where)

    if message.IsSuccess:
        message.set_data(re_ent)
    return Fun.class_to_JsonStr(message)


@app.route('/user/save', methods=['GET', 'POST'])
@auth.login_required
def user_save():
    j_data = request.json
    if j_data is None:
        return Fun.class_to_JsonStr(AppReturnDTO(False, "参数有误"))
    in_ent = RequestSaveModel(j_data)
    _modele = UserDal()
    re_ent, message = _modele.user_Save(
        in_dict=in_ent.Data, saveKeys=in_ent.SaveKeys)
    if message.IsSuccess:
        message.set_data(re_ent)
    return Fun.class_to_JsonStr(message)


@app.route('/User/Module', methods=['GET', 'POST'])
@auth.login_required
def user_module():
    '''
    获取用户的所有模块
    '''
    j_data = request.json
    if j_data is None:
        return Fun.class_to_JsonStr(AppReturnDTO(False, "参数有误"))
    in_ent = PostBaseModel(j_data)
    _mod = UserDal()
    if g == None:
        return Fun.class_to_JsonStr(AppReturnDTO(False, "没有登录"))

    re_ent, message = _mod.user_all_module(g.current_user['ID'])
    if message.IsSuccess:
        message.set_data(re_ent)

    return Fun.class_to_JsonStr(message)

@app.route('/user/single', methods=['GET', 'POST'])
@auth.login_required
def user_single():
    j_data = request.json
    if j_data is None:
        return Fun.class_to_JsonStr(AppReturnDTO(False, "参数有误"))
    in_ent = PostBaseModel(j_data)
    _modele=UserDal()
    re_ent,message= _modele.user_single(in_ent.Key)
    if message.IsSuccess :
        message.set_data(re_ent)

    return Fun.class_to_JsonStr(message) 