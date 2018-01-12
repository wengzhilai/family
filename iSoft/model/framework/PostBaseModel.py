class PostBaseModel(object):
    #主键
    Key=None
    Token=None
    def __init__(self,jsonObj):
        self.__dict__=jsonObj