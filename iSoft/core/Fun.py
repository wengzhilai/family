'''静态类'''
import re
import math
import json
from iSoft.entity.model import db
from iSoft.model.AppReturnDTO import AppReturnDTO
from iSoft import app
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer,
                          SignatureExpired, BadSignature)
import hashlib


class Fun(object):
    '''静态方法'''
    @staticmethod
    def convert_to_dict(obj):
        '''把Object对象转换成Dict对象'''
        re_dict = {}
        if obj is None:
            return re_dict
        for k in obj.__dict__.keys():
            if obj.__dict__[k] != None and obj.__dict__[k] != '':
                re_dict[k] = obj.__dict__[k]
        return re_dict

    @staticmethod
    def convert_to_dicts(objs):
        '''把对象列表转换为字典列表'''
        obj_arr = []
        for obj in objs:
            # 把Object对象转换成Dict对象
            re_dict = {}
            re_dict.update(obj.__dict__)
            obj_arr.append(re_dict)
        return obj_arr

    @staticmethod
    def class_to_dict(obj):
        '''把对象(支持单个对象、list、set)转换成字典'''
        is_list = obj.__class__ == [].__class__
        is_set = obj.__class__ == set().__class__
        if is_list or is_set:
            obj_arr = []
            for obj1 in obj:
                # 把Object对象转换成Dict对象
                re_dict = {}
                re_dict.update(obj1.__dict__)
                obj_arr.append(re_dict)
            return obj_arr
        else:
            re_dict = {}
            re_dict.update(obj.__dict__)
            return re_dict

    @staticmethod
    def class_to_JsonStr(obj):
        '''把对类转成JSon字符串'''
        return json.dumps(Fun.convert_to_dict(obj), ensure_ascii=False)

    @staticmethod
    def class_to_class(inClass, outClass):
        '''把对类转成JSon字符串'''
        return outClass

    @staticmethod
    def is_phonenum(phone_num):
        '''检测电否为电话号码'''
        rep = re.compile(r'^0\d{2,3}\d{7,8}$|^1[358]\d{9}$|^147\d{8}')
        phonematch = rep.match(phone_num)
        if phonematch:
            return True
        else:
            return False

    @staticmethod
    def password_complexity(passwd):
        '''检测密码复杂度'''
        _re_int = 0
        if re.match(r'^.*[a-z]+.*$', passwd) is not None:
            _re_int += 1
        if re.match(r'^.*[A-Z]+.*$', passwd) is not None:
            _re_int += 1
        if re.match(r'^.*\d+.*$', passwd) is not None:
            _re_int += 1
        if re.match(r'^.*(?=([\x21-\x7e]+)[^a-zA-Z0-9]).*$', passwd) is not None:
            _re_int += 1
        return _re_int

    @staticmethod
    def GetSeqId(model):
        '''获取表的自增ID'''
        return db.session.execute('select nextval("{}_seq") seq'.format(model.__tablename__)).fetchall()[0][0]

    @staticmethod
    def model_save(model, self, in_dict, saveKeys):

        if 'ID' not in in_dict:
            in_dict["ID"] = 0
        db_ent = model.query.filter(model.ID == in_dict["ID"]).first()
        if db_ent is None:
            db_ent = self
            for item in in_dict:
                setattr(db_ent, item, in_dict[item])
            if db_ent.ID is None or db_ent.ID == "" or db_ent.ID == 0 or db_ent.ID == '0':
                db_ent.ID = Fun.GetSeqId(model)
            db.session.add(db_ent)
        else:
            for item in saveKeys:
                if item in in_dict:
                    setattr(db_ent, item, in_dict[item])
        db.session.commit()
        return db_ent, AppReturnDTO(True)

    @staticmethod
    def model_findall(model, pageIndex, pageSize, criterion, where):
        relist = model.query
        if criterion is None:
            criterion = []
        if where is None:
            where = []
        for item in where:
            relist = relist.filter(item)

        for item in criterion:
            relist = relist.order_by(item)
        num = relist.count()
        if pageIndex < 1:
            pageSize = 1
        if pageSize < 1:
            pageSize = 10
        # 最大页码
        max_page = math.ceil(num / pageSize)  # 向上取整
        if pageIndex > max_page:
            return None, AppReturnDTO(True, num)
        relist = relist.paginate(pageIndex, per_page=pageSize).items
        return relist, AppReturnDTO(True, num)

    @staticmethod
    def model_delete(model, key):
        '删除记录，并返回删除的条数'
        try:
            delMode = model.query.filter(model.ID == key).delete(synchronize_session=False)
            db.session.commit()
            return delMode,AppReturnDTO(True)
        except:
            return None,AppReturnDTO(False,'删除失败')
        

    @staticmethod
    def model_single(model, key):
        db_ent = model.query.filter(model.ID == key).first()
        return db_ent, AppReturnDTO(True)

    @staticmethod
    def generate_auth_token(userId, expiration=60000):
        '''获取用户的token'''
        ser = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        token = ser.dumps({'ID': userId})
        return token.decode('utf-8')

    @staticmethod
    def verify_auth_token(token):
        '''根据token获取用户'''
        ser = Serializer(app.config['SECRET_KEY'])
        try:
            data = ser.loads(token)
            if data is None:
                return AppReturnDTO(False, "数据不存在"), None  # invalid token
            user = {'ID': int(data['ID'])}
        except SignatureExpired:
            # valid token, but expired
            return AppReturnDTO(False, "token已经过期"), None
        except BadSignature:
            return AppReturnDTO(False, "token无效"), None  # invalid token
        except BaseException:
            return AppReturnDTO(False, "错误"), None
        if user is None:
            return AppReturnDTO(False, "用户不存在"), None
        return AppReturnDTO(True), user

    @staticmethod
    def sql_to_dict(sql):
        """
        将SQL 执行成 dict
        """
        relist = db.session.execute(sql)
        allData = []
        for row in relist:
            tmpDic = {}
            for dic in row.items():
                tmpDic[dic[0]] = dic[1]

            allData.append(tmpDic)
        return allData, AppReturnDTO(True)

    @staticmethod
    def post_to_dict(request):
        '''把请求的数据，转换成dict'''
        j_data = request.json
        if j_data is None:
            return None, AppReturnDTO(False, "参数有误")
        return j_data, AppReturnDTO(True)

    @staticmethod
    def IsNullOrEmpty(_instr):
        '''判断值是否是空'''
        if _instr is None or not str(_instr).strip():
            return True
        return False

    @staticmethod
    def md5(_instr):
        '''md5加密字符串 '''
        return hashlib.md5(_instr.encode('utf-8')).hexdigest()