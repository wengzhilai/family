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

        nowPlace, msg = self.AddSonItem(reEnt.ItemList, userInfoEnt, 1, 7,
                                        AxisXY(0, 0))

        item = self.UserInfoToRelativeItem(userInfoEnt, nowPlace.Between(), 0)
        msg = self.AddFatherItem(reEnt.ItemList, userInfoEnt, 1, 4,AxisXY(nowPlace.Between(), 0))

        reEnt.ItemList.append(item)
        
        # 求最小值，原理是，不能让坐标出现负数
        minX = min([item.x for item in reEnt.ItemList])
        minY = min([item.y for item in reEnt.ItemList])

        for item in reEnt.ItemList:
            if minX<0 :
                item.x=item.x-minX
            if minY<0:
                item.y=item.y-minY


        allUserId=[item.Id for item in reEnt.ItemList]
        reEnt.RelativeList = [{
            "K": item.Id,
            "V": item.FatherId
        } for item in reEnt.ItemList if item.FatherId is not None and item.FatherId in allUserId]
        reEnt.FormatItemList()
        return reEnt, AppReturnDTO(True)

    def AddFatherItem(self, mainList, inSon, levelId, maxLevelId, inAxisXY):
        if levelId > maxLevelId:
            return True;
        if inSon.FATHER_ID is None:
            return True;
        # 获取父级的所有子，也包括本人，并排序
        father=FaUserInfo.query.filter(FaUserInfo.ID == inSon.FATHER_ID).first()
        sonList=sorted(father.fa_user_infos, key=lambda x: x.LEVEL_ID)
        
        #获取当前传入值的位置
        myPlace = 0;
        myPlace=max(index for index in range(len(sonList)) if sonList[index].ID == inSon.ID)

        brotherXList=[]

        # 添加自己
        brotherXList.append(inAxisXY.X)
        #比传入用的值小的兄弟
        for i in range(0,myPlace):
            nowI= myPlace-i
            x = inAxisXY.X-((i+1)*2)
            brotherXList.append(x)
            item = self.UserInfoToRelativeItem(sonList[nowI-1], x, inAxisXY.Y)
            mainList.append(item)
        # 添加比传入大的兄弟
        for i in range(1,len(sonList)-myPlace):
            nowI= myPlace+i
            x = inAxisXY.X+(i*2)
            brotherXList.append(x)
            item = self.UserInfoToRelativeItem(sonList[nowI], x, inAxisXY.Y)
            mainList.append(item)
        minX=min(brotherXList)
        maxX=max(brotherXList)
        # 添加父亲
        mainList.append(self.UserInfoToRelativeItem(father,  (minX+maxX)/2 , inAxisXY.Y-1))
 
        self.AddFatherItem(mainList, father, levelId+1, maxLevelId,AxisXY((minX+maxX)/2, inAxisXY.Y-1))
        return True

    def AddSonItem(self, mainList, inFather, levelId, maxLevelId, inAxisXY):
        """
        添加子节点，和计算当前坐标HorizonVal
            :param mainList: 
            :param inFather: 
            :param levelId: 
            :param maxLevelId: 
            :param inAxisXY: 
        """

        # 初始化最小值
        reEnt = HorizonVal(inAxisXY.X, inAxisXY.X)

        if levelId > maxLevelId:  # 如果层级过大，则退出
            return reEnt, AppReturnDTO(True)

        # 如果没有子项也退出
        if inFather.fa_user_infos is None or len(inFather.fa_user_infos) == 0:
            return reEnt, AppReturnDTO(True)

        startX = inAxisXY.X
        # 循环所有子项，子项从小到大
        allChildren = sorted(inFather.fa_user_infos, key=lambda x: x.LEVEL_ID)
        allChildXList=[]
        for index, son in enumerate(allChildren):
            #获取子项的
            nowHorizonVal, msg = self.AddSonItem(mainList, son, levelId+1, maxLevelId,
                                                 AxisXY(
                                                     startX, inAxisXY.Y + 1))

            # 该值会传入入下一项兄弟项，加2是因为每个项间隔都是2，在除的时候，才会有整数
            startX = nowHorizonVal.AllMaxHorizon if nowHorizonVal.AllMaxHorizon > nowHorizonVal.RowMaxHorizon + 2 else nowHorizonVal.RowMaxHorizon + 2
            #获取所有子项的中间值
            thisItemX = nowHorizonVal.Between()
            # 保存所有子项的X坐标
            allChildXList.append(thisItemX)

            item = self.UserInfoToRelativeItem(son, thisItemX, inAxisXY.Y + 1)
            mainList.append(item)

        reEnt.RowMaxHorizon = max(allChildXList)
        reEnt.RowMinHorizon = min(allChildXList)
        reEnt.AllMaxHorizon = startX if startX > reEnt.RowMaxHorizon else reEnt.RowMaxHorizon
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