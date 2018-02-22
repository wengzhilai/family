from iSoft.core.Fun import Fun
from iSoft import auth, app
from flask import g, request
from iSoft.model.AppReturnDTO import AppReturnDTO
from iSoft.model.framework.RequestPagesModel import RequestPagesModel
from iSoft.model.framework.RequestSaveModel import RequestSaveModel
from iSoft.model.framework.PostBaseModel import PostBaseModel
from iSoft.dal.RoleDal import RoleDal
from iSoft.entity.model import FaRole

@app.route('/role/list', methods=['GET', 'POST'])
@auth.login_required
def role_list():
    j_data = request.json
    if j_data is None:
        return Fun.class_to_JsonStr(AppReturnDTO(False, "参数有误"))
    in_ent = RequestPagesModel(j_data)
    where = []
    for search in in_ent.SearchKey:
        if search["Type"]=="like" :
            where.append(eval("FaRole.%(Key)s.like('%%%(Value)s%%')" % search))
        else:
            where.append(eval("FaRole.%(Key)s%(Type)s%(Value)s" % search))

    criterion = []
    for search in in_ent.OrderBy:
        search["Value"] = search["Value"].lower()
        criterion.append(eval("FaRole.%(Key)s.%(Value)s()" % search))

    _modele = RoleDal()
    re_ent, message = _modele.Role_findall(
        in_ent.PageIndex,
        in_ent.PageSize,
        criterion,
        where)

    if message.IsSuccess:
        message.set_data(re_ent)
    return Fun.class_to_JsonStr(message)


@app.route('/role/save', methods=['GET', 'POST'])
@auth.login_required
def role_save():
    j_data = request.json
    if j_data is None:
        return Fun.class_to_JsonStr(AppReturnDTO(False, "参数有误"))
    in_ent = RequestSaveModel(j_data)
    _modele=RoleDal()
    re_ent,message= _modele.Role_Save(in_dict=in_ent.Data,saveKeys=in_ent.SaveKeys)
    if message.IsSuccess :
        message.set_data(re_ent)
    return Fun.class_to_JsonStr(message)
        
@app.route('/role/delete', methods=['GET', 'POST'])
@auth.login_required
def role_delete():
    j_data = request.json
    if j_data is None:
        return Fun.class_to_JsonStr(AppReturnDTO(False, "参数有误"))
    in_ent = PostBaseModel(j_data)
    _modele=RoleDal()
    message= _modele.Role_delete(in_ent.Key)

    return Fun.class_to_JsonStr(message)        

@app.route('/role/single', methods=['GET', 'POST'])
@auth.login_required
def role_single():
    j_data = request.json
    if j_data is None:
        return Fun.class_to_JsonStr(AppReturnDTO(False, "参数有误"))
    in_ent = PostBaseModel(j_data)
    _modele=RoleDal()
    re_ent,message= _modele.Role_single(in_ent.Key)
    if message.IsSuccess :
        message.set_data(re_ent)

    return Fun.class_to_JsonStr(message)   