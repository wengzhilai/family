'''用户'''
from app.core.Fun import Fun 
from app.entity.dal.UserDal import UserDal
from app import auth, login_manager, app
from flask import g,json

@app.route('/User/List', methods=['GET', 'POST'])
@auth.login_required
def user_lsit():
    userlist=UserDal.single_user(1)
    print(userlist)
    return 'json.dumps(Fun.convert_to_dict(userlist))'