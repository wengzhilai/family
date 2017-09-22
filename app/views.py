"""This script parse the content of a xml file"""
from app import app,auth,login_manager
from flask import render_template,json
from app.dbModel.dal import UserDal
from app.core.AlchemyEncoder import AlchemyEncoder
from flask.ext.login import (LoginManager, login_required, login_user,current_user,
                             logout_user, UserMixin)
from app.dbModel.models.UserModel import User
from app.core.model.AppReturnDTO import AppReturnDTO

@app.route('/')
@app.route('/index')
#dddddd
def index():
    user=UserDal.SingleUser(1)
    # dic=dict(user)
    print(type(user))
    # print(json.dumps(user,cls=AlchemyEncoder))
    # print(json.dumps(dic))
    return json.dumps(user,cls=AlchemyEncoder);
    # return jsonify({"jstt":json.loads(user)});

@login_manager.user_loader
def load_user(user_id):
    # print(user_id)
    user = UserDal.SingleUser(user_id)
    return user

@auth.route('/login', methods=['GET', 'POST'])
def login():
    reEnt=AppReturnDTO(False,U'登录超时');
    print(type(reEnt))
    return json.dumps(reEnt.__dict__,cls=AlchemyEncoder)

@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return "logout page"   

# test method
@app.route('/test')
@login_required
def test():
    print(current_user.NAME)
    return 'Logged in as: '+current_user.NAME


app.register_blueprint(auth, url_prefix='/auth')
