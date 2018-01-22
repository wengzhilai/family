'''用户'''
from iSoft.core.Fun import Fun
from iSoft.dal.user import user
from iSoft import auth, login_manager, app
from flask import g, json, request
from iSoft.core.AlchemyEncoder import AlchemyEncoder
from iSoft.core.model.AppReturnDTO import AppReturnDTO
from iSoft.model.framework.RequestPagesModel import RequestPagesModel
from iSoft.model.framework.PostBaseModel import PostBaseModel


@app.route('/User/List', methods=['GET', 'POST'])
@auth.login_required
def user_list():
    j_data = request.json
    if j_data is None:
        return Fun.class_to_JsonStr(AppReturnDTO(False, "参数有误"))
    in_ent = RequestPagesModel(j_data)
    where = []
    for search in in_ent.SearchKey:
        where.append(eval("FaUser.%(Key)s%(Type)s%(Value)s" % search))

    criterion=[]
    for search in in_ent.OrderBy:
        criterion.append(eval("FaUser.%(Key)s.%(Value)s()" % search))

    _modele=user()
    re_ent,message = _modele.user_findall(\
        in_ent.PageIndex, \
        in_ent.PageSize, \
        criterion, \
        where)

    if message.is_success :
        message.set_data(re_ent)
    return Fun.class_to_JsonStr(message)

@app.route('/User/Module', methods=['GET', 'POST'])
@auth.login_required
def user_module():
    j_data = request.json
    if j_data is None:
        return Fun.class_to_JsonStr(AppReturnDTO(False, "参数有误"))
    in_ent = PostBaseModel(j_data)
    _mod=user()
    if g == None:
        return Fun.class_to_JsonStr(AppReturnDTO(False, "没有登录"))

    re_ent,message= _mod.user_all_module(g.current_user.ID)
    if message.is_success :
        message.set_data(re_ent)

    return Fun.class_to_JsonStr(message) 
