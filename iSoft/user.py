'''用户'''
from iSoft.core.Fun import Fun
from iSoft.dal.user import user
from iSoft import auth, login_manager, app
from flask import g, json, request
from iSoft.core.AlchemyEncoder import AlchemyEncoder
from iSoft.core.model.AppReturnDTO import AppReturnDTO
from iSoft.entity.model import FaUser
from iSoft.model.framework.RequesPagesModel import RequesPagesModel


@app.route('/User/List', methods=['GET', 'POST'])
@auth.login_required
def user_list():
    j_data = request.json
    if j_data is None:
        return Fun.class_to_JsonStr(AppReturnDTO(False, "参数有误"))
    in_ent = RequesPagesModel(j_data)
    where = []
    for search in in_ent.SearchKey:
        where.append(eval("FaUser.%(Key)s%(Type)s%(Value)s" % search))
        pass

    criterion = FaUser.ID, FaUser.ID
    userlist = user.user_findall(in_ent.PageIndex, in_ent.PageSize, criterion,
                                 *where)

    if userlist is None:
        return Fun.class_to_JsonStr(AppReturnDTO(True, "", []))
    userlist = userlist.items

    re_ent = AppReturnDTO(True, data=userlist)
    return json.dumps(Fun.convert_to_dict(re_ent), ensure_ascii=False)
