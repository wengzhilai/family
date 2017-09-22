from flask import Flask,Blueprint
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

app = Flask(__name__)
# url redirect
auth = Blueprint('auth', __name__)
app.config.from_object('config')
db = SQLAlchemy(app)
app.secret_key="超级认证字符"


 


login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.session_protection = "strong"
login_manager.login_message = "Please login to access this page."
login_manager.login_message_category = "info"

login_manager.init_app(app)
from app import views 

