import pymssql  
from sqlalchemy import Column, String, create_engine  
from sqlalchemy import Table, MetaData, Column, Integer  
  
# engine = create_engine("mssql+pymssql://sa:sa@192.168.0.110:1521/iSoftBS",deprecate_large_types=True) #替换自己的user/pwd/host/db  
  
# m = MetaData()  
# t = Table('t', m, Column('id', Integer, primary_key=True),  
#                 Column('x', Integer))  
  
# m.create_all(engine)  
  
# engine.execute(t.insert(), {'id': 1, 'x':1}, {'id':2, 'x':2}) 

def connDb():
    # 需要用到pymssql组件 该组件下载地址：http://www.lfd.uci.edu/~gohlke/pythonlibs/#pymssql  
    conn = pymssql.connect(host="192.168.0.110",user="sa",password="sa",database="iSoftBS")  
    
    #需要用到端口号时   
    # conn = pymssql.connect(host="127.0.0.1",port="端口号",user="sa",password="123",database="Northwind")  
    
    #获取游标对象  
    cur=conn.cursor()  
    
    # #查询操作  
    sql="select count(*) from [User]"  
    cur.execute(sql)  
    
    list=cur.fetchall()  
  
    # #关闭数据库连接  
    conn.close()  
    return str(list)