#!E:\study\python\app\core\model\AppReturnDTO.py
import json
from iSoft.core.AlchemyEncoder import AlchemyEncoder
from iSoft.core.DecimalEncoder import DecimalEncoder
'''
返回模块
'''
class AppReturnDTO(object):
    '''
    返回对象
    '''
    # 数据 json 格式
    Data = {}
    # 信息
    Msg = ""
    # 是否成功
    IsSuccess = True
    # 代码
    Code = ""
    def __init__(self, isSuccess=True, msg='', data=None, code=""):
        self.Code = code
        self.IsSuccess = isSuccess
        self.Msg = msg
        self.Data = json.loads(json.dumps(data, cls=AlchemyEncoder))

    def set_data(self, data):
        '''设置数据格式为JSON'''
        self.Data = json.loads(json.dumps(data, cls=AlchemyEncoder))
    
    def set_dict_data(self, data):
        '''设置数据格式为JSON'''
        self.Data = json.loads(json.dumps(data, cls=DecimalEncoder))