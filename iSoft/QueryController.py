'''用户'''
from iSoft.core.Fun import Fun
from iSoft import auth, login_manager, app
from flask import g, json, request
from iSoft.core.AlchemyEncoder import AlchemyEncoder
from iSoft.model.AppReturnDTO import AppReturnDTO
from iSoft.model.framework.RequestPagesModel import RequestPagesModel
from iSoft.model.framework.RequestSaveModel import RequestSaveModel
from iSoft.model.framework.PostBaseModel import PostBaseModel
from iSoft.entity.model import FaQuery
from iSoft.dal.QueryDal import QueryDal


@app.route('/query/list', methods=['GET', 'POST'])
@auth.login_required
def query_list():
    j_data = request.json
    if j_data is None:
        return Fun.class_to_JsonStr(AppReturnDTO(False, "参数有误"))
    in_ent = RequestPagesModel(j_data)
    where = []
    for search in in_ent.SearchKey:
        if search["Type"] == "like":
            where.append(
                eval("FaQuery.%(Key)s.like('%%%(Value)s%%')" % search))
        else:
            where.append(eval("FaQuery.%(Key)s%(Type)s%(Value)s" % search))

    criterion = []
    for search in in_ent.OrderBy:
        search["Value"] = search["Value"].lower()
        criterion.append(eval("FaQuery.%(Key)s.%(Value)s()" % search))

    _modele = QueryDal()
    re_ent, message = _modele.query_findall(in_ent.PageIndex, in_ent.PageSize,
                                            criterion, where)

    if message.IsSuccess:
        message.set_data(re_ent)
    return Fun.class_to_JsonStr(message)


@app.route('/query/save', methods=['GET', 'POST'])
@auth.login_required
def query_save():
    j_data = request.json
    if j_data is None:
        return Fun.class_to_JsonStr(AppReturnDTO(False, "参数有误"))
    in_ent = RequestSaveModel(j_data)
    _modele = QueryDal()
    re_ent, message = _modele.query_Save(
        in_dict=in_ent.Data, saveKeys=in_ent.SaveKeys)
    if message.IsSuccess:
        message.set_data(re_ent)
    return Fun.class_to_JsonStr(message)


@app.route('/query/delete', methods=['GET', 'POST'])
@auth.login_required
def query_delete():
    j_data = request.json
    if j_data is None:
        return Fun.class_to_JsonStr(AppReturnDTO(False, "参数有误"))
    in_ent = PostBaseModel(j_data)
    _modele = QueryDal()
    message = _modele.query_delete(in_ent.Key)
    return Fun.class_to_JsonStr(message)


@app.route('/query/single_code', methods=['GET', 'POST'])
@auth.login_required
def query_single_code():
    j_data = request.json
    if j_data is None:
        return Fun.class_to_JsonStr(AppReturnDTO(False, "参数有误"))
    in_ent = PostBaseModel(j_data)
    _modele = QueryDal()
    re_ent, message = _modele.query_singleByCode(in_ent.Key)
    if message.IsSuccess:
        message.set_data(re_ent)
    return Fun.class_to_JsonStr(message)


@app.route('/query/query', methods=['GET', 'POST'])
@auth.login_required
def query_query():
    j_data = request.json
    if j_data is None:
        return Fun.class_to_JsonStr(AppReturnDTO(False, "参数有误"))
    in_ent = RequestPagesModel(j_data)

    _modele = QueryDal()
    re_ent, message = _modele.query_queryByCode(
        in_ent.Key, in_ent.PageIndex, in_ent.PageSize, in_ent.OrderBy, in_ent.SearchKey)

    if message.IsSuccess:
        message.set_dict_data(re_ent)
    return Fun.class_to_JsonStr(message)
