from iSoft.entity.model import FaModule


class module(object):
    def module_findall(self, pageIndex, pageSize, whereLambda, orderField, orderBy):
        allData= FaModule.query.paginate(page,per_page=pageSize)
        return allData

