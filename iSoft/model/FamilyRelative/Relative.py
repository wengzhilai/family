import json
from iSoft.core.AlchemyEncoder import AlchemyEncoder
from iSoft.core.DecimalEncoder import DecimalEncoder

class Relative(object):
    ItemList=[] #展示所有用户
    RelativeList={}
    def __init__(self):
        self.ItemList=[]
        self.RelativeList=[]

    def FormatItemList(self):
        temp=[item.__dict__ for item in self.ItemList ]
        self.ItemList=temp