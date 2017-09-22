class AppReturnDTO(object):
    Data={}
    Msg=""
    IsSuccess=True;
    Code=""
    def __init__(self, isSuccess=True,msg='',code='',data=None):
        self.Code=code
        self.IsSuccess=isSuccess
        self.Msg=msg
        self.Data=data
    def __repr__(self):
           return 'self.__dir__' 
        