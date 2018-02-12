from openpyxl import Workbook


class Office(object):
    @staticmethod
    def ExportToXls(_dictList, _fig, _fileName):
        '''
        把dict格式，保存为excel
        _dictList:格式为：[{"a": 3, "b": 2}, {"a": 2, "b": 4}]
        '''
        wb = Workbook(write_only=True)
        # _dictList = [{"a": 3, "b": 2}, {"a": 2, "b": 4}]
        # _fig = {"a": {"title":"a"}, "b": {"title":"b"}}
        ws = wb.create_sheet()
        # now we'll fill it with 100 rows x 200 columns

        for index, item in enumerate(_dictList):
            if index == 0:
                ws.append([x[1].get("title") for x in _fig.items()])
            ws.append([item.get(x) for x in _fig])
        # save the file
        wb.save(_fileName)
