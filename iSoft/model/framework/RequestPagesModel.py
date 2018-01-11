from .PostBaseModel import PostBaseModel
class RequestPagesModel(PostBaseModel):
    PageIndex=1
    PageSize=10
    AttachParams=[]
    SearchKey=[]
    OrderBy=[]
    Data=None
    def __init__(self,jsonObj):
        self.__dict__=jsonObj
        