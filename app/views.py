# file: example1.py
'''首页'''
import app.core.Fun
from app import app, auth
from flask_login import login_required

@app.route('/')
@app.route('/index')
def index():
    ''' 首页 '''
    return 'json.dumps(user, cls=AlchemyEncoder)'

# test method
@app.route('/index/test')
@login_required
def test():
    '''测试'''
    print('current_user.NAME')
    return 'Logged in as: '

