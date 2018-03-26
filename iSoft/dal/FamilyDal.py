from iSoft.model.AppReturnDTO import AppReturnDTO
from iSoft.entity.model import db, FaUserInfo
from iSoft.model.FamilyRelative.Relative import Relative
from iSoft.model.FamilyRelative.RelativeItem import RelativeItem
from iSoft.model.FamilyRelative.RelativeItem import RelativeItem, HorizonVal, AxisXY


class FamilyDal(object):
    def UserInfoRelative(self, userId):
        userInfoEnt = FaUserInfo.query.filter(FaUserInfo.ID == userId).first()
        if userInfoEnt is None:
            return None, AppReturnDTO(False, "用户不存在")
        reEnt = Relative()

        nowPlace, msg = self.AddSonItem(reEnt.ItemList, userInfoEnt, 1, 4,AxisXY(0, 0))

        item = self.UserInfoToRelativeItem(userInfoEnt, nowPlace.Between(), 0)
        reEnt.ItemList.append(item)

        # minX = min([item.x for item in reEnt.ItemList])
        # minY = min([item.y for item in reEnt.ItemList])
        # minY = -minY;
        # minX = 0 if minX > 0 else minX
        # minY = 0 if minY > 0 else minY

        # for item in reEnt.ItemList:
        #     item.y = -item.y
        #     item.y = item.y - minY
        #     item.x = item.x - minX     
        reEnt.RelativeList =  [{"K":item.Id,"V":item.FatherId} for item in reEnt.ItemList if item.FatherId is not None]
        reEnt.FormatItemList()
        return reEnt, AppReturnDTO(True)

    def AddSonItem(self, mainList, inFather, levelId, maxLevelId, inAxisXY):
        """
        添加子节点，和计算当前坐标HorizonVal
            :param mainList: 
            :param inFather: 
            :param levelId: 
            :param maxLevelId: 
            :param inAxisXY: 
        """
        reEnt = HorizonVal(inAxisXY.X, inAxisXY.X)

        if levelId > maxLevelId:  # 如果层级过大，则退出
            return reEnt, AppReturnDTO(True)

        # 如果没有子项也退出
        if inFather.fa_user_infos is None or len(inFather.fa_user_infos) == 0:
            return reEnt, AppReturnDTO(True)

        # 循环所有子项，子项从小到大
        startX = inAxisXY.X
        allChildren = sorted(inFather.fa_user_infos, key=lambda x: x.LEVEL_ID)

        for index,son in enumerate(allChildren):
            #获取子项的
            nowHorizonVal, msg = self.AddSonItem(mainList, son, 1, 4,AxisXY(inAxisXY.X, inAxisXY.Y + 1))

            item = self.UserInfoToRelativeItem(son, nowHorizonVal.Between() + (index*2), inAxisXY.Y + 1)
            mainList.append(item)

        if reEnt.RowMaxHorizon > reEnt.AllMaxHorizon:
            reEnt.AllMaxHorizon = reEnt.RowMaxHorizon
        return reEnt, AppReturnDTO(True)

    def UserInfoToRelativeItem(self, faUserInfo, x, y):
        """
        把userinfo转成RelativeItem
            :param self: 
            :param faUserInfo:  要转的实体
            :param x: 坐标x
            :param y: 坐标y
        """
        reEnt = RelativeItem()
        reEnt.ElderId = faUserInfo.ELDER_ID
        if faUserInfo.fa_elder is not None:
            reEnt.ElderName = faUserInfo.fa_elder.NAME
        reEnt.FatherId = faUserInfo.FATHER_ID
        # reEnt.IcoUrl = reEnt
        reEnt.Id = faUserInfo.ID
        reEnt.Name = faUserInfo.NAME
        reEnt.Sex = faUserInfo.SEX
        reEnt.x = x
        reEnt.y = y
        return reEnt