# -*- coding: utf-8 -*-
'''__init__.py '''
from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS
from flask_httpauth import HTTPTokenAuth

app = Flask(__name__)
CORS(app)
# url redirect
# auth = Blueprint('auth', __name__)
auth = HTTPTokenAuth(scheme='Bearer')
app.config.from_object('config')
db = SQLAlchemy(app)
app.secret_key = "超级认证字符"

login_manager = LoginManager()
login_manager.login_view = "auth.logout"
login_manager.session_protection = "strong"
login_manager.login_message = "Please login to access this page."
login_manager.login_message_category = "info"

login_manager.init_app(app)

from iSoft import ViewsController, AuthController, UserController, RoleController, ModuleController, QueryController
from iSoft import DistrictController, WebApi, WebApi_Auth, WebApi_Family, WebApi_UserInfo
