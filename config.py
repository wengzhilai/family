import os
basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True
# Flask-WTF 使用这个密钥生成加密令牌
SECRET_KEY = 'you-will-never-guess'

OPENID_PROVIDERS = [
    { 'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id' },
    { 'name': 'Yahoo', 'url': 'https://me.yahoo.com' },
    { 'name': 'AOL', 'url': 'http://openid.aol.com/<username>' },
    { 'name': 'Flickr', 'url': 'http://www.flickr.com/<username>' },
    { 'name': 'MyOpenID', 'url': 'https://www.myopenid.com' }]
    
# SQLALCHEMY_DATABASE_URI = 'mssql+pymssql://sa:sa@192.168.0.110:1433/Tmp'
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://FA:FA@139.129.194.140:3306/FA'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = False
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')