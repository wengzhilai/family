#!E:\study\python\app\core\model\AppReturnDTO.py
import json
from iSoft.core.AlchemyEncoder import AlchemyEncoder
'''
返回模块
'''
class AppReturnDTO(object):
    '''
    返回对象
    '''
    # 数据 json 格式
    data = {}
    # 信息
    msg = ""
    # 是否成功
    is_success = True
    # 代码
    code = ""
    def __init__(self, isSuccess=True, msg='', data=None, code=""):
        self.code = code
        self.is_success = isSuccess
        self.msg = msg
        self.data = json.loads(json.dumps(data, cls=AlchemyEncoder))

    def set_data(self, data):
        '''设置数据格式为JSON'''
        self.data = json.loads(json.dumps(data, cls=AlchemyEncoder))
        