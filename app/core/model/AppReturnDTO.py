#!E:\study\python\app\core\model\AppReturnDTO.py
import json
'''
返回模块
'''
class AppReturnDTO(object):
    '''
    返回对象
    '''
    Data = {}
    Msg = "中国"
    IsSuccess = True
    Code = ""
    def __init__(self, isSuccess=True,msg='',code='',data=None):
        self.Code = code
        self.IsSuccess = isSuccess
        self.Msg = msg
        self.Data = data
        