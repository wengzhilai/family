class AppRegisterModel(object):
    #出生日期
    BIRTHDAY_TIME = ""
    #分份类型
    YEARS_TYPE = "选择时间"
    #出生地
    birthday_place = "四川仪陇岐山翁家坝"
    #短信代码
    code = ""
    #排行
    level_id = "1"
    #登录名
    loginName = ""
    #所有的父级节点
    parentArr = []
    #密码
    password = ""
    #推荐码
    pollCode = ""
    #性别
    sex = ""
    def __init__(self,jsonObj):
        self.__dict__=jsonObj