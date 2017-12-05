'''用户'''
from app.core.Fun import Fun 
from app.entity.dal.UserDal import UserDal
from app import auth, login_manager, app
from flask import g,json
from app.core.AlchemyEncoder import AlchemyEncoder
from app.core.model.AppReturnDTO import AppReturnDTO

@app.route('/User/List', methods=['GET', 'POST'])
@auth.login_required
def user_lsit():
    userlist=UserDal.single_user(1)
    re_ent=AppReturnDTO(False, "密码复杂度不够", userlist);
    return json.dumps(Fun.convert_to_dict(re_ent), ensure_ascii=False)
