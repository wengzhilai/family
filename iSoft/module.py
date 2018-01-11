from iSoft.core.Fun import Fun
from iSoft import auth, login_manager, app
from flask import g, json, request
from iSoft.core.AlchemyEncoder import AlchemyEncoder
from iSoft.core.model.AppReturnDTO import AppReturnDTO

from iSoft.model.framework.RequestPagesModel import RequestPagesModel
from iSoft.model.framework.RequestSaveModel import RequestSaveModel

from iSoft.dal.module import module

@app.route('/module/save', methods=['GET', 'POST'])
@auth.login_required
def save():
    j_data = request.json
    if j_data is None:
        return Fun.class_to_JsonStr(AppReturnDTO(False, "参数有误"))
    in_ent = RequestSaveModel(j_data)
    
    _modele=module(in_ent.Data)

    _modele.module_Save(in_dict=in_ent.Data,saveKeys=in_ent.SaveKeys)

    return Fun.class_to_JsonStr(AppReturnDTO(True, "成功"))
        