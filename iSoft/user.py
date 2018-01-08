'''用户'''
from iSoft.core.Fun import Fun 
from iSoft.entity.dal.UserDal import UserDal
from iSoft import auth, login_manager, app
from flask import g,json
from iSoft.core.AlchemyEncoder import AlchemyEncoder
from iSoft.core.model.AppReturnDTO import AppReturnDTO

@app.route('/User/List', methods=['GET', 'POST'])
@auth.login_required
def user_lsit():
    userlist=UserDal.single_user(1)
    re_ent=AppReturnDTO(False, "密码复杂度不够", userlist);
    return json.dumps(Fun.convert_to_dict(re_ent), ensure_ascii=False)
