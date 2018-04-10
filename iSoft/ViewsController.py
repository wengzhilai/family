# file: view.py
# -*- coding: utf-8 -*-
'''首页'''
from iSoft.core.Fun import Fun
from iSoft import app, auth
from flask_login import login_required
from flask import send_file, make_response, send_from_directory, request, g
from functools import wraps
from iSoft.dal.UserDal import UserDal
from iSoft.dal.AuthDal import AuthDal
import json
import os
import sys
import iSoft.core.Office as Of

from iSoft.dal.QueryDal import QueryDal
from iSoft.model.framework.RequestPagesModel import RequestPagesModel
from iSoft.model.AppReturnDTO import AppReturnDTO


@auth.verify_token
def verify_token(token):
    '''验证toke'''
    print('verify_token')
    print(token)
    msg, user = AuthDal.verify_auth_token(token)
    if msg.IsSuccess:
        g.current_user = user
        return True
    return False


@app.route('/view/export_query', methods=['GET', 'POST'])
@auth.login_required
def view_export():
    """
    导出EXCEL文件
    """
    j_data = request.json
    if j_data is None:
        return Fun.class_to_JsonStr(AppReturnDTO(False, "参数有误"))
    in_ent = RequestPagesModel(j_data)

    _modele = QueryDal()
    sql, cfg, message = _modele.query_GetSqlByCode(in_ent.Key, in_ent.SearchKey,
                                                   in_ent.OrderBy)
    if not message.IsSuccess:
        return Fun.class_to_JsonStr(message)

    _dict, message = Fun.sql_to_dict(sql)
    if not message.IsSuccess:
        return Fun.class_to_JsonStr(message)

    dirpath = os.path.join(app.root_path, 'download')
    file_name = "query_{0}.xlsx".format(in_ent.Key)

    Of.Office.ExportToXls(_dict, cfg, dirpath + "\\" + file_name)
    # directory = os.getcwd()  # 假设在当前目录
    # response = make_response(
    #     send_from_directory(directory, file_name, as_attachment=True))
    # response.headers["Content-Disposition"] = "attachment; filename={}".format(
    #     file_name.encode().decode('latin-1'))

    return Fun.class_to_JsonStr(AppReturnDTO(True,"{0}/{1}".format('download',file_name)))


@app.route("/download/<path:filename>")
def downloader(filename):
    '查看static下所有文件'
    dirpath = os.path.join(app.root_path, '../static')
    return send_from_directory(dirpath, filename, as_attachment=True)


@app.route('/', methods=['GET', 'POST'])
@auth.login_required
def index():
    if g == None:
        return "Hellow"
    return "Hello, %s!" % g.current_user.ID




@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username


@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id


@app.route('/projects/', methods=['GET', 'POST'])
def projects():
    h = request.headers
    j = request.json
    b = request.get_data()

    j_data = json.loads(str(b, encoding="utf-8"))  # -----load将字符串解析成json

    # print(j_data)
    return j.__str__()


@app.route('/about')
def about():
    return 'The about page'


# @app.errorhandler(404)
# def internal_error(error):
#     return "render_template('404.html')", 404

# @app.errorhandler(500)
# def internal_error(error):
#     db.session.rollback()
#     return "render_template('500.html')", 500
