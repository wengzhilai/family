using ProInterface;
using System;
using System.Collections.Generic;
using System.Linq;
using ProInterface.Models;
using System.Reflection;
using System.Data.Entity.Validation;
using AutoMapper;
using System.Web;
using System.Text;
using ProServer.ApiAdmin;

namespace ProServer.ApiWeb
{
    public class UserInfoApi : IUserInfoApi
    {
        ServeWeb api;

        public UserInfoApi(ServeWeb _serveWeb)
        {
            api = _serveWeb;
        }

        public ErrorInfo UserInfoReg(ref ErrorInfo err, ApiRequesSaveEntityBean<FaUserInfo> inEnt)
        {
            if (inEnt.para.Count(x => Convert.ToInt32(x.K) > 0) == 0)
            {
                err.IsError = true;
                err.Message = "参数有误";
                return null;
            }
            using (DBEntities db = new DBEntities())
            {
                //从上往下，有K的排在前面，辈份越高
                #region 判断父亲级是否正常，并添加不存在的用户
                for (var i = 0; i < inEnt.para.Count; i++)
                {
                    var parent = inEnt.para[i];
                    if (string.IsNullOrEmpty(parent.K))
                    {
                        if (i == 0)
                        {
                            err.IsError = true;
                            err.Message = "参数有误,第一条数据的K不能为空";
                            return null;
                        }
                        else
                        {

                            ApiRequesSaveEntityBean<FaUserInfo> tmpEnt = new ApiRequesSaveEntityBean<FaUserInfo>();
                            tmpEnt.authToken = inEnt.authToken;
                            tmpEnt.entity = new FaUserInfo();
                            tmpEnt.entity.NAME = parent.V;
                            tmpEnt.entity.FATHER_ID = Convert.ToInt32(inEnt.para[i - 1].K);
                            tmpEnt.entity.SEX = "汉";

                            var userFather = db.fa_user_info.SingleOrDefault(x => x.ID == tmpEnt.entity.FATHER_ID);
                            if (userFather != null)
                            {
                                tmpEnt.entity.DISTRICT_ID = userFather.fa_user.DISTRICT_ID;
                                tmpEnt.entity.RoleAllIDStr = string.Join(",", userFather.fa_user.fa_role.Select(x => x.ID));
                                tmpEnt.entity.FAMILY_ID = userFather.FAMILY_ID;
                                tmpEnt.entity.ELDER_ID = userFather.ELDER_ID;
                            }

                            var userInfoNow = UserInfoSave(db, ref err, tmpEnt);
                            if (err.IsError)
                            {
                                return null;
                            }
                            parent.K = userInfoNow.ID.ToString();
                        }
                    }
                    else
                    {
                        var id = Convert.ToInt32(parent.K);
                        if (db.fa_user_info.Where(x => x.ID == id && x.fa_user.NAME == parent.V).Count() == 0)
                        {
                            err.IsError = true;
                            err.Message = string.Format("{0}数据有误", parent.V);
                            return null;
                        }
                    }
                }
                #endregion

                inEnt.entity.FATHER_ID = Convert.ToInt32(inEnt.para[inEnt.para.Count() - 1].K);
                var user = UserInfoSave(db, ref err, inEnt);
                if (err.IsError) return err;
                Fun.DBEntitiesCommit(db, ref err);
                if (err.IsError) return err;
                err.Message = user.ID.ToString();
            }
            return new ErrorInfo();
        }
        public ApiPagingDataBean<FaUserInfo> UserInfoList(ref ErrorInfo err, ApiRequesPageBean<ApiPagingDataBean<FaUserInfo>> inEnt)
        {
            GlobalUser gu = Global.GetUser(inEnt.authToken);
            if (gu == null)
            {
                err.IsError = true;
                err.Message = "登录超时";
                return null;
            }
            if (inEnt.pageSize == 0) inEnt.pageSize = 10;
            if (inEnt == null)
            {
                err.IsError = true;
                err.Message = "参数有误";
                return null;
            }
            ApiPagingDataBean<FaUserInfo> reEnt = new ApiPagingDataBean<FaUserInfo>();

            int skip = 0;
            if (inEnt.currentPage > 1)
            {
                skip = (inEnt.currentPage - 1) * inEnt.pageSize;
            }
            using (DBEntities db = new DBEntities())
            {
                var tmpPar = inEnt.para.SingleOrDefault(x => x.K == "keyWord");
                string keyWord = null;
                if (tmpPar == null)
                {
                    return reEnt;
                }
                keyWord = tmpPar.V;


                var allData = db.fa_user_info.OrderByDescending(x => x.ID).ToList().AsEnumerable();
                allData = allData.Where(x =>
                   (x.fa_user.NAME != null && x.fa_user.NAME.IndexOf(keyWord) > -1)
                || (x.fa_user.LOGIN_NAME != null && x.fa_user.LOGIN_NAME.IndexOf(keyWord) > -1)
                ).AsEnumerable();

                #region 过虑条件
                if (inEnt.searchKey != null)
                {
                    foreach (var filter in inEnt.searchKey)
                    {
                        allData = Fun.GetListWhere(allData, filter.K, filter.T, filter.V, ref err);
                    }
                }
                #endregion

                #region 排序

                if (allData == null)
                {
                    err.IsError = true;
                    return null;
                }
                foreach (var filter in inEnt.orderBy)
                {
                    allData = Fun.GetListOrder(allData, filter.K, filter.V, ref err);
                }
                #endregion

                var allList = allData.Skip(skip).Take(inEnt.pageSize).ToList();

                reEnt.currentPage = inEnt.currentPage;
                reEnt.pageSize = inEnt.pageSize;
                reEnt.totalCount = allData.Count();
                reEnt.totalPage = reEnt.totalCount / reEnt.pageSize;
                if (reEnt.totalCount % reEnt.pageSize != 0) reEnt.totalPage++;
                IList<FaUserInfo> reList = new List<FaUserInfo>();
                foreach (var t in allList)
                {
                    var single = Mapper.Map<FaUserInfo>(t);
                    single = Mapper.Map<FaUserInfo>(t);
                    reList.Add(single);
                }
                reEnt.data = reList;
            }
            return reEnt;
        }
        /* 2017-5-7 23:34:16 */
        public FaUserInfo UserInfoAddFriend(ref ErrorInfo err, ApiRequesSaveEntityBean<FaUserInfo> inEnt)
        {
            GlobalUser gu = Global.GetUser(inEnt.authToken);
            if (gu == null)
            {
                err.IsError = true;
                err.Message = "登录超时";
                return null;
            }
            var userInfo = UserInfoSave(ref err, inEnt);
            if (err.IsError)
            {
                return null;
            }
            using (DBEntities db = new DBEntities())
            {
                var info = db.fa_user_info.SingleOrDefault(x => x.ID == userInfo.ID);
                if (info == null)
                {
                    err.IsError = true;
                    err.Message = "保存数据错误";
                    return null;
                }
                info.fa_user1.Add(db.fa_user.SingleOrDefault(x => x.ID == gu.UserId));
                Fun.DBEntitiesCommit(db, ref err);
                return userInfo;
            }
        }


        public FaUserInfoRelative UserInfoRelative(ref ErrorInfo err, ApiRequesEntityBean<FaUserInfoRelative> inEnt)
        {
            GlobalUser gu = Global.GetUser(inEnt.authToken);
            if (gu == null)
            {
                err.IsError = true;
                err.Message = "登录超时";
                return null;
            }
            FaUserInfoRelative reEnt = new FaUserInfoRelative();
            using (DBEntities db = new DBEntities())
            {
                var userInfo = db.fa_user_info.SingleOrDefault(x => x.ID == inEnt.id);
                if (userInfo == null)
                {
                    err.IsError = true;
                    err.Message = "用户ID有误";
                    return null;
                }
                var tmpXY = AddSonItem(reEnt.ItemList, userInfo, 1, 6, new XYZ { X = 0, Y = 0, Z = 0 });
                var nowInfo = InfoToItem(userInfo, (tmpXY[0] + tmpXY[1]) / 2, 0);
                reEnt.ItemList.Add(nowInfo);
                AddFatherItem(reEnt.ItemList, userInfo, 1, 2, new XYZ { X = nowInfo.x, Y = nowInfo.y, Z = userInfo.fa_user_info1.Count() }, tmpXY[0], tmpXY[1]);

                var minX = reEnt.ItemList.Min(x => x.x);
                var minY = reEnt.ItemList.Max(x => x.y);
                minY = -minY;
                if (minX > 0) minX = 0;
                if (minY > 0) minY = 0;
                foreach (var item in reEnt.ItemList)
                {
                    item.y = -item.y;
                    item.y = item.y - minY;
                    item.x = item.x - minX;
                }

                reEnt.RelativeList = reEnt.ItemList.Where(x => x.FatherId != null).Select(x => new KV { K = x.Id.ToString(), V = x.FatherId.ToString() }).ToList();

                return reEnt;
            }
        }
        /// <summary>
        /// 
        /// </summary>
        /// <param name="mainList"></param>
        /// <param name="inSon"></param>
        /// <param name="levelId"></param>
        /// <param name="maxLevelId"></param>
        /// <param name="xyz">z:width</param>
        /// <returns></returns>
        private bool AddFatherItem(IList<FaUserInfoRelativeItem> mainList, fa_user_info inSon, int levelId, int maxLevelId, XYZ xyz, int toLeft, int toRigth)
        {
            if (levelId > maxLevelId) return true;
            if (inSon.fa_user_info2 == null) return true;
            var allSon = inSon.fa_user_info2.fa_user_info1.OrderBy(x => x.LEVEL_ID).ToList();
            var sonList = Mapper.Map<IList<FaUserInfoRelativeItem>>(allSon);
            #region 计算坐标
            var myPlace = 0;
            for (var i = 0; i < sonList.Count; i++)
            {
                if (sonList[i].Id == inSon.ID) myPlace = i;
            }
            //表示开始的位置            
            sonList[myPlace].x = xyz.X;
            sonList[myPlace].y = xyz.Y;
            for (var i = 0; i < myPlace; i++)
            {
                var thisItme = sonList[myPlace - i - 1];
                thisItme.y = xyz.Y;
                thisItme.x = toLeft - i * 2 - 2;
                mainList.Add(thisItme);
            }

            int startX = toRigth + 2;
            for (var i = myPlace + 1; i < sonList.Count; i++)
            {
                var tmpXY = AddSonItem(mainList, allSon[i], 1, 1, new XYZ { X = startX, Y = xyz.Y });
                startX = tmpXY[1] + 2;
                sonList[i].x = (tmpXY[0] + tmpXY[1]) / 2;
                sonList[i].y = xyz.Y;
                mainList.Add(sonList[i]);

            }
            #endregion

            var minX = sonList.Min(x => x.x);
            var maxX = sonList.Max(x => x.x);
            var father = InfoToItem(inSon.fa_user_info2, (minX + maxX) / 2, xyz.Y + 1);
            mainList.Add(father);

            AddFatherItem(mainList, inSon.fa_user_info2, levelId + 1, maxLevelId, new XYZ { X = father.x, Y = father.y }, minX, maxX);
            return true;
        }
        private IList<int> AddSonItem(IList<FaUserInfoRelativeItem> mainList, fa_user_info inFather, int levelId, int maxLevelId, XYZ xyz)
        {
            if (levelId > maxLevelId) return new[] { xyz.X, xyz.X, xyz.X };
            var allSon = inFather.fa_user_info1.OrderBy(x => x.LEVEL_ID).ToList();
            if (allSon.Count() == 0) return new[] { xyz.X, xyz.X, xyz.X };
            var allSonItem = Mapper.Map<IList<FaUserInfoRelativeItem>>(allSon);

            int startX = xyz.X;
            for (var i = 0; i < allSonItem.Count(); i++)
            {
                var tmpXY = AddSonItem(mainList, allSon[i], levelId + 1, maxLevelId, new XYZ { X = startX, Y = xyz.Y - 1 });
                startX = tmpXY[1] + 2;
                if (tmpXY[2] > startX) startX = tmpXY[2];
                allSonItem[i].x = (tmpXY[0] + tmpXY[1]) / 2;
                allSonItem[i].y = xyz.Y - 1;
                mainList.Add(allSonItem[i]);
            }
            var maxX = allSonItem.Max(x => x.x);
            if (maxX < startX) maxX = startX;
            return new[] { allSonItem.Min(x => x.x), allSonItem.Max(x => x.x), maxX };
        }

        private FaUserInfoRelativeItem InfoToItem(fa_user_info userInfo, int x, int y)
        {
            var ent = Mapper.Map<FaUserInfoRelativeItem>(userInfo);
            ent.x = x;
            ent.y = y;
            return ent;
        }

        /* 2017年5月6日16:16:54 */
        public FaUserInfo UserInfoSave(ref ErrorInfo err, ApiRequesSaveEntityBean<FaUserInfo> inEnt)
        {
            GlobalUser gu = Global.GetUser(inEnt.authToken);
            if (gu == null)
            {
                err.IsError = true;
                err.Message = "登录超时";
                return null;
            }
            using (DBEntities db = new DBEntities())
            {
                var reEnt = UserInfoSave(db, ref err, inEnt);
                Fun.DBEntitiesCommit(db, ref err);
                return reEnt;
            }
        }


        /* 2017年5月6日16:16:54 */
        public FaUserInfo UserInfoSave(DBEntities db, ref ErrorInfo err, ApiRequesSaveEntityBean<FaUserInfo> inEnt)
        {
            GlobalUser gu = Global.GetUser(inEnt.authToken);
            if (gu == null)
            {
                err.IsError = true;
                err.Message = "登录超时";
                return null;
            }
            if (string.IsNullOrEmpty(inEnt.saveKeys)) inEnt.saveKeys = "";
            var allPar = inEnt.saveKeys.Split(',');
            //调用用户保存
            var user = api.UserApi.UserSave(db, inEnt.authToken, ref err, inEnt.entity, allPar);
            if (err.IsError)
            {
                return null;
            }
            var userInfo = db.fa_user_info.SingleOrDefault(x => x.ID == user.ID);
            if (userInfo == null)
            {
                userInfo = Mapper.Map<fa_user_info>(inEnt.entity);
                userInfo.ID = user.ID;
                userInfo.STATUS = "正常";
                userInfo.CREATE_TIME = DateTime.Now;
                userInfo.CREATE_USER_ID = gu.UserId;
                userInfo.CREATE_USER_NAME = gu.UserName;
                userInfo.UPDATE_TIME = DateTime.Now;
                userInfo.UPDATE_USER_ID = gu.UserId;
                userInfo.UPDATE_USER_NAME = gu.UserName;
                UpdataLog<FaUserInfo> updataLog = new UpdataLog<FaUserInfo>(db);
                updataLog.UpdataLogSaveCreate(gu, Mapper.Map<FaUserInfo>(userInfo));
                db.fa_user_info.Add(userInfo);
            }
            else
            {
                UpdataLog<FaUserInfo> updataLog = new UpdataLog<FaUserInfo>(db, Mapper.Map<FaUserInfo>(userInfo));
                userInfo = Fun.ClassToCopy<FA_USER_INFO, fa_user_info>(inEnt.entity, userInfo, allPar);
                //userInfo.UPDATE_TIME = DateTime.Now;
                userInfo.UPDATE_USER_ID = gu.UserId;
                userInfo.UPDATE_USER_NAME = gu.UserName;
                updataLog.UpdataLogSaveUdate(gu, Mapper.Map<FaUserInfo>(userInfo));
            }
            return Mapper.Map<FaUserInfo>(userInfo);
        }

        /* 2017-5-6 22:57:48 */
        public FaUserInfo UserInfoSingle(ref ErrorInfo err, ApiRequesEntityBean<FaUserInfo> inEnt)
        {
            GlobalUser gu = Global.GetUser(inEnt.authToken);
            if (gu == null)
            {
                err.IsError = true;
                err.Message = "登录超时";
                return null;
            }
            using (DBEntities db = new DBEntities())
            {
                ApiRequesEntityBean<TUser> userEnt = Fun.ClassToCopy<ApiRequesEntityBean<FaUserInfo>, ApiRequesEntityBean<TUser>>(inEnt);
                var user = api.UserApi.UserSingle(db, inEnt.authToken, ref err, userEnt);
                if (user == null)
                {
                    return null;
                }

                var userInfo = db.fa_user_info.FirstOrDefault(x => x.ID == user.ID);
                if (userInfo == null)
                {
                    return Mapper.Map<FaUserInfo>(user);
                }
                var reEnt = Mapper.Map<FaUserInfo>(user);
                reEnt = Mapper.Map(userInfo, reEnt);
                return reEnt;
            }
        }

        public ApiPagingDataBean<FaUserInfo> UserInfoSingleByName(ref ErrorInfo err, ApiRequesEntityBean<FaUserInfo> inEnt)
        {
            using (DBEntities db = new DBEntities())
            {
                var namePar = inEnt.para.FirstOrDefault(x => x.K == "name");
                if (namePar == null)
                {
                    err.IsError = true;
                    err.Message = "名称不能为空";
                    return null;
                }
                var userInfo = db.fa_user_info.Where(x => x.fa_user.NAME == namePar.V).ToList();
                
                var data = Mapper.Map<IList<FaUserInfo>>(userInfo);
                ApiPagingDataBean<FaUserInfo> reEnt = new ApiPagingDataBean<FaUserInfo>();
                reEnt.data = data;
                reEnt.currentPage = 1;
                reEnt.pageSize = 10;
                reEnt.totalCount = data.Count();
                reEnt.totalPage = 1;
                return reEnt;
            }
        }


        public FaUserInfo UserInfoFatherSingle(ref ErrorInfo err, ApiRequesEntityBean<FaUserInfo> inEnt)
        {
            GlobalUser gu = Global.GetUser(inEnt.authToken);
            if (gu == null)
            {
                err.IsError = true;
                err.Message = "登录超时";
                return null;
            }
            using (DBEntities db = new DBEntities())
            {
                var userId = inEnt.id;
                if (inEnt.id == 0)
                {
                    userId = gu.UserId;
                }

                var ent = db.fa_user_info.SingleOrDefault(x => x.ID == userId);
                if (ent == null)
                {
                    err.IsError = true;
                    err.Message = "用户不存在";
                    return null;
                }
                if (ent.FATHER_ID == null)
                {
                    return new FaUserInfo
                    {
                        BIRTHDAY_TIME = DateTime.Now,
                        DIED_TIME = DateTime.Now,
                        SEX = "男",
                        NAME = ent.fa_user.NAME.Substring(0, 1),
                        IS_LIVE = 1
                    };
                }
                inEnt.id = ent.FATHER_ID.Value;

                return UserInfoSingle(ref err, inEnt);
            }
        }

        public FaUserInfo UserInfoFatherSave(ref ErrorInfo err, ApiRequesSaveEntityBean<FaUserInfo> inEnt)
        {
            GlobalUser gu = Global.GetUser(inEnt.authToken);
            if (gu == null)
            {
                err.IsError = true;
                err.Message = "登录超时";
                return null;
            }
            using (DBEntities db = new DBEntities())
            {
                var reEnt = UserInfoSave(db, ref err, inEnt);
                if (err.IsError) return reEnt;

                var userId = 0;
                var tmp = inEnt.para.FirstOrDefault(x => x.K == "userId");
                if (tmp != null)
                {
                    userId = Convert.ToInt32(tmp.V);
                }

                var ent = db.fa_user_info.SingleOrDefault(x => x.ID == userId);
                if (ent == null)
                {
                    err.IsError = true;
                    err.Message = "用户不存在";
                    return null;
                }
                ent.FATHER_ID = reEnt.ID;

                Fun.DBEntitiesCommit(db, ref err);
                return reEnt;

            }
        }

        public string UserInfoAddMultiSon(ref ErrorInfo err, ApiRequesSaveEntityBean<string> inEnt)
        {
            GlobalUser gu = Global.GetUser(inEnt.authToken);
            if (gu == null)
            {
                err.IsError = true;
                err.Message = "登录超时";
                return null;
            }
            if (string.IsNullOrEmpty(inEnt.entity))
            {
                err.IsError = true;
                err.Message = "参数有误";
                return null;
            }
            //调用用户保存
            using (DBEntities db = new DBEntities())
            {
                var allUserNameArr = inEnt.entity.Split(',').Where(x => !string.IsNullOrWhiteSpace(x)).ToList();

                var parentUser = db.fa_user_info.SingleOrDefault(x => x.ID == inEnt.userId);
                if (parentUser == null)
                {
                    err.IsError = true;
                    err.Message = "当前用户不存在";
                    return null;
                }
                if (string.IsNullOrEmpty(parentUser.fa_user.NAME))
                {
                    err.IsError = true;
                    err.Message = "当前用户不存在";
                    return null;
                }
                var fristName = parentUser.fa_user.NAME.Substring(0, 1);

                foreach (var userName in allUserNameArr)
                {
                    TUser inUser = new TUser();
                    if (userName.Substring(0, 1).Equals(fristName))
                    {
                        inUser.NAME = userName;
                    }
                    else
                    {
                        inUser.NAME = string.Format("{0}{1}", fristName, userName);
                    }
                    inUser.DISTRICT_ID = parentUser.fa_user.DISTRICT_ID;
                    inUser.RoleAllIDStr = string.Join(",", parentUser.fa_user.fa_role.Select(x => x.ID).ToList());
                    var user = api.UserApi.UserSave(db, inEnt.authToken, ref err, inUser, new List<string> { "NAME", "DISTRICT_ID", "RoleAllIDStr" });
                    if (err.IsError)
                    {
                        return null;
                    }
                    var userInfo = db.fa_user_info.SingleOrDefault(x => x.ID == user.ID);
                    if (userInfo == null)
                    {
                        userInfo = new fa_user_info();
                        userInfo.ID = user.ID;
                        userInfo.STATUS = "正常";
                        userInfo.CREATE_TIME = DateTime.Now;
                        userInfo.CREATE_USER_ID = gu.UserId;
                        userInfo.CREATE_USER_NAME = gu.UserName;
                        userInfo.UPDATE_TIME = DateTime.Now;
                        userInfo.UPDATE_USER_ID = gu.UserId;
                        userInfo.UPDATE_USER_NAME = gu.UserName;

                        userInfo.FATHER_ID = parentUser.ID;
                        UpdataLog<FaUserInfo> updataLog = new UpdataLog<FaUserInfo>(db);
                        updataLog.UpdataLogSaveCreate(gu, Mapper.Map<FaUserInfo>(userInfo));
                        db.fa_user_info.Add(userInfo);
                    }
                }
                if (err.IsError)
                {
                    return null;
                }
                Fun.DBEntitiesCommit(db, ref err);
                return allUserNameArr.Count().ToString();

            }
        }

        public ErrorInfo UserInfoDelete(ref ErrorInfo err, ApiRequesEntityBean<ErrorInfo> inEnt)
        {
            GlobalUser gu = Global.GetUser(inEnt.authToken);
            if (gu == null)
            {
                err.IsError = true;
                err.Message = "登录超时";
                return null;
            }
            if (inEnt.id==0)
            {
                err.IsError = true;
                err.Message = "参数有误";
                return null;
            }
            //调用用户保存
            using (DBEntities db = new DBEntities())
            {
                var userInfo = db.fa_user_info.SingleOrDefault(x => x.ID == inEnt.id);
                if (userInfo == null)
                {
                    err.IsError = true;
                    err.Message = "用户不存在";
                    return null;
                }
                if (userInfo.fa_user_info1.Count() > 0)
                {
                    err.IsError = true;
                    err.Message = "该用户已有子女，不能删除";
                    return null;
                }

                if (userInfo.fa_user != null)
                {
                    userInfo.fa_user.fa_district1.Clear();
                    userInfo.fa_user.fa_module.Clear();
                    userInfo.fa_user.fa_role.Clear();
                    userInfo.fa_user.fa_user_info1.Clear();
                    db.fa_user.Remove(userInfo.fa_user);
                }
                userInfo.fa_user1.Clear();
                foreach (var t in userInfo.fa_user_event.ToList())
                {
                    db.fa_user_event.Remove(t);
                }

                db.fa_user_info.Remove(userInfo);

                Fun.DBEntitiesCommit(db, ref err);
                return err;
            }
        }


    }
}
