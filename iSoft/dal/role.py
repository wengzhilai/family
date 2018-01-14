import math

from iSoft.entity.model import FaRole,Sequence, db
from iSoft.core.model.AppReturnDTO import AppReturnDTO


class Role(FaRole):

    def __init__(self):
        pass

    def Role_findall(self, pageIndex, pageSize, criterion, where):
        relist = FaRole.query
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
            return None
        relist = relist.paginate(pageIndex, per_page=pageSize).items
        return relist, AppReturnDTO(True)

    def Role_Save(self, in_dict, saveKeys):
        db_ent = FaRole.query.filter(FaRole.ID == in_dict["ID"]).first()        
        if db_ent is None:
            db_ent = self
            for item in in_dict:
                setattr(db_ent, item, in_dict[item])
            if db_ent.ID is None or db_ent.ID == 0 or db_ent.ID == '0':
                seq=Sequence.query.filter(Sequence.seq_name=="FA_ROLE_SEQ").first()
                if seq is not None:
                    db_ent.ID=int(seq.current_val) + 1
            db.session.add(db_ent)

        else:
            for item in saveKeys:
                setattr(db_ent, item, in_dict[item])

        db.session.commit()
        return db_ent, AppReturnDTO(True)

    def Role_delete(self, key):
        db_ent = FaRole.query.filter(FaRole.ID == key).first()
        if db_ent is not None:
            db.session.delete(db_ent)
        db.session.commit()
        return True, AppReturnDTO(True)
