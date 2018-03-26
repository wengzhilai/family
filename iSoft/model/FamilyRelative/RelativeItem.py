class HorizonVal(object):
    '用于添加子行后返回的值'
    RowMinHorizon = 0  #该行最小的值
    RowMaxHorizon = 0  #该行最大的值
    AllMaxHorizon = 0  #所有子行的最大的值

    def __init__(self, _Min, _Max):
        self.RowMinHorizon = _Min
        self.RowMaxHorizon = _Max

    def Between(self):
        '计算中间位置'
        return (self.RowMinHorizon + self.RowMaxHorizon) / 2


class AxisXY(object):
    '用于传值'
    X = 0  #X坐标值
    Y = 0  #Y坐标值
    ChildrenNum = 0  #子项数

    def __init__(self, _X, _Y):
        self.X = _X
        self.Y = _Y


class RelativeItem(object):
    '用于显示关系图的节点'
    Id = 0  #ID
    ElderId = 0  #辈字排号
    ElderName = ""  #辈字
    Name = ""  #姓名
    FatherId = None  #父亲ID
    IcoUrl = ""  #头像图片
    Sex = ""  #性别
    x = 0  #坐标X
    y = 0  #坐标Y
    pass
