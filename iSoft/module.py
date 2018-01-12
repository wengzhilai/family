from iSoft.core.Fun import Fun
from iSoft import auth, login_manager, app
from flask import g, json, request
from iSoft.core.AlchemyEncoder import AlchemyEncoder
from iSoft.core.model.AppReturnDTO import AppReturnDTO
from iSoft.model.framework.RequestPagesModel import RequestPagesModel
from iSoft.model.framework.RequestSaveModel import RequestSaveModel
from iSoft.model.framework.PostBaseModel import PostBaseModel
from iSoft.dal.module import module
from iSoft.entity.model import FaModule


@app.route('/module/List', methods=['GET', 'POST'])
@auth.login_required
def module_list():
    j_data = request.json
    if j_data is None:
        return Fun.class_to_JsonStr(AppReturnDTO(False, "参数有误"))
    in_ent = RequestPagesModel(j_data)
    where = []
    for search in in_ent.SearchKey:
        where.append(eval("FaModule.%(Key)s%(Type)s%(Value)s" % search))

    criterion=[]
    for search in in_ent.OrderBy:
        criterion.append(eval("FaModule.%(Key)s.%(Value)s()" % search))

    _modele=module()
    re_ent,message = _modele.module_findall(\
        in_ent.PageIndex, \
        in_ent.PageSize, \
        criterion, \
        *where)

    if message.is_success :
        message.set_data(re_ent)
    return Fun.class_to_JsonStr(message)

@app.route('/module/save', methods=['GET', 'POST'])
@auth.login_required
def module_save():
    j_data = request.json
    if j_data is None:
        return Fun.class_to_JsonStr(AppReturnDTO(False, "参数有误"))
    in_ent = RequestSaveModel(j_data)
    _modele=module()
    re_ent,message= _modele.module_Save(in_dict=in_ent.Data,saveKeys=in_ent.SaveKeys)
    if message.is_success :
        message.set_data(re_ent)
    return Fun.class_to_JsonStr(message)
        
@app.route('/module/delete', methods=['GET', 'POST'])
@auth.login_required
def module_delete():
    j_data = request.json
    if j_data is None:
        return Fun.class_to_JsonStr(AppReturnDTO(False, "参数有误"))
    in_ent = PostBaseModel(j_data)
    _modele=module()
    re_ent,message= _modele.module_delete(in_ent.Key)
    if message.is_success :
        message.set_data(re_ent)

    return Fun.class_to_JsonStr(message)        