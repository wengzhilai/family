'''配制文件'''
import os

BASE = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True
# Flask-WTF 使用这个密钥生成加密令牌
SECRET_KEY = 'you-will-never-guess'
# SQLALCHEMY_DATABASE_URI = 'mssql+pymssql://sa:sa@192.168.0.110:1433/Tmp'
# SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://FA:FA@139.129.194.140:3306/FA'
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://FA:abcdef123@47.254.16.126:3306/fa'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = False

SQLALCHEMY_MIGRATE_REPO = os.path.join(BASE, 'db_repository')

# 密码复杂度
PASSWORD_COMPLEXITY = 2
# 短信验证码
VERIFY_CODE = True
