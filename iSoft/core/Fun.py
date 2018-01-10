'''静态类'''
import re
import json

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
            #把Object对象转换成Dict对象
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
                #把Object对象转换成Dict对象
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
