from .PostBaseModel import PostBaseModel
class RequestSaveModel(PostBaseModel):
    # 参数  list<KeyValuePair>
    Para=[]
    # 需保存的字段 list<string>
    SaveKeys=[]
    # 提交的实体
    Data=None

    def __init__(self,jsonObj):
        self.__dict__=jsonObj

        