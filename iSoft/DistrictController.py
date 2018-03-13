from iSoft.core.Fun import Fun
from iSoft import auth, login_manager, app
from flask import g, json, request
from iSoft.core.AlchemyEncoder import AlchemyEncoder
from iSoft.model.AppReturnDTO import AppReturnDTO
from iSoft.model.framework.RequestPagesModel import RequestPagesModel
from iSoft.model.framework.RequestSaveModel import RequestSaveModel
from iSoft.model.framework.PostBaseModel import PostBaseModel
from iSoft.dal.DistrictDal import DistrictDal
from iSoft.entity.model import FaDistrict



@app.route('/district/list', methods=['GET', 'POST'])
@auth.login_required
def district_list():
    j_data = request.json
    if j_data is None:
        return Fun.class_to_JsonStr(AppReturnDTO(False, "参数有误"))
    in_ent = RequestPagesModel(j_data)
    where = []
    for search in in_ent.SearchKey:
        if search["Type"]=="like" :
            where.append(eval("FaDistrict.%(Key)s.like('%%%(Value)s%%')" % search))
        else:
            where.append(eval("FaDistrict.%(Key)s%(Type)s%(Value)s" % search))

    criterion = []
    for search in in_ent.OrderBy:
        search["Value"] = search["Value"].lower()
        criterion.append(eval("FaDistrict.%(Key)s.%(Value)s()" % search))

    _modele = DistrictDal()
    re_ent, message = _modele.district_findall(
        in_ent.PageIndex,
        in_ent.PageSize,
        criterion,
        where)

    if message.IsSuccess:
        message.set_data(re_ent)
    return Fun.class_to_JsonStr(message)


@app.route('/district/save', methods=['GET', 'POST'])
@auth.login_required
def district_save():
    j_data = request.json
    if j_data is None:
        return Fun.class_to_JsonStr(AppReturnDTO(False, "参数有误"))
    in_ent = RequestSaveModel(j_data)
    _modele=DistrictDal()
    re_ent,message= _modele.district_Save(in_dict=in_ent.Data,saveKeys=in_ent.SaveKeys)
    if message.IsSuccess :
        message.set_data(re_ent)
    return Fun.class_to_JsonStr(message)
        
@app.route('/district/delete', methods=['GET', 'POST'])
@auth.login_required
def district_delete():
    j_data = request.json
    if j_data is None:
        return Fun.class_to_JsonStr(AppReturnDTO(False, "参数有误"))
    in_ent = PostBaseModel(j_data)
    _modele=DistrictDal()
    message= _modele.district_delete(in_ent.Key)
    return Fun.class_to_JsonStr(message)  

@app.route('/district/single', methods=['GET', 'POST'])
@auth.login_required
def district_single():
    j_data = request.json
    if j_data is None:
        return Fun.class_to_JsonStr(AppReturnDTO(False, "参数有误"))
    in_ent = PostBaseModel(j_data)
    _modele=DistrictDal()
    re_ent,message= _modele.district_single(in_ent.Key)
    if message.IsSuccess :
        message.set_data(re_ent)

    return Fun.class_to_JsonStr(message)        

     