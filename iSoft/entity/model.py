# coding: utf-8
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String, Table, Text
from sqlalchemy.orm import relationship
from sqlalchemy.schema import FetchedValue
from flask_sqlalchemy import SQLAlchemy
from iSoft import db

class FaAppVersion(db.Model):
    __tablename__ = 'fa_app_version'

    ID = db.Column(db.Integer, primary_key=True)
    IS_NEW = db.Column(db.Numeric(1, 0), nullable=False)
    TYPE = db.Column(db.String(20), nullable=False)
    REMARK = db.Column(db.String(1000))
    UPDATE_TIME = db.Column(db.DateTime)
    UPDATE_URL = db.Column(db.String(200))



class FaBulletin(db.Model):
    __tablename__ = 'fa_bulletin'

    ID = db.Column(db.Integer, primary_key=True)
    TITLE = db.Column(db.String(255), nullable=False)
    PIC = db.Column(db.String(255))
    TYPE_CODE = db.Column(db.String(50))
    CONTENT = db.Column(db.Text)
    USER_ID = db.Column(db.Integer)
    PUBLISHER = db.Column(db.String(255), nullable=False)
    ISSUE_DATE = db.Column(db.DateTime, nullable=False)
    IS_SHOW = db.Column(db.Numeric(1, 0), nullable=False)
    IS_IMPORT = db.Column(db.Numeric(1, 0), nullable=False)
    IS_URGENT = db.Column(db.Numeric(1, 0), nullable=False)
    AUTO_PEN = db.Column(db.Numeric(1, 0), nullable=False)
    CREATE_TIME = db.Column(db.DateTime, nullable=False)
    UPDATE_TIME = db.Column(db.DateTime, nullable=False)
    REGION = db.Column(db.String(10), nullable=False)

    fa_files = db.relationship(u'FaFile', secondary=u'fa_bulletin_file', backref=u'fa_bulletins')
    fa_role = db.relationship(u'FaRole', secondary=u'fa_bulletin_role', backref=u'fa_bulletins')



t_fa_bulletin_file = db.Table(
    'fa_bulletin_file',
    db.Column('BULLETIN_ID', db.ForeignKey(u'fa_bulletin.ID'), primary_key=True, nullable=False),
    db.Column('FILE_ID', db.ForeignKey(u'fa_files.ID'), primary_key=True, nullable=False)
)



class FaBulletinLog(db.Model):
    __tablename__ = 'fa_bulletin_log'

    ID = db.Column(db.Integer, primary_key=True)
    BULLETIN_ID = db.Column(db.ForeignKey(u'fa_bulletin.ID'), nullable=False)
    USER_ID = db.Column(db.Integer, nullable=False)
    LOOK_TIME = db.Column(db.DateTime, nullable=False)

    fa_bulletin = db.relationship(u'FaBulletin', primaryjoin='FaBulletinLog.BULLETIN_ID == FaBulletin.ID', backref=u'fa_bulletin_logs')



class FaBulletinReview(db.Model):
    __tablename__ = 'fa_bulletin_review'

    ID = db.Column(db.Integer, primary_key=True)
    PARENT_ID = db.Column(db.ForeignKey(u'fa_bulletin_review.ID'))
    BULLETIN_ID = db.Column(db.ForeignKey(u'fa_bulletin.ID'), nullable=False)
    NAME = db.Column(db.String(50))
    CONTENT = db.Column(db.Text)
    USER_ID = db.Column(db.Integer, nullable=False)
    ADD_TIME = db.Column(db.DateTime, nullable=False)
    STATUS = db.Column(db.String(10), nullable=False)
    STATUS_TIME = db.Column(db.DateTime, nullable=False)

    fa_bulletin = db.relationship(u'FaBulletin', primaryjoin='FaBulletinReview.BULLETIN_ID == FaBulletin.ID', backref=u'fa_bulletin_reviews')
    parent = db.relationship(u'FaBulletinReview', remote_side=[ID], primaryjoin='FaBulletinReview.PARENT_ID == FaBulletinReview.ID', backref=u'fa_bulletin_reviews')



t_fa_bulletin_role = db.Table(
    'fa_bulletin_role',
    db.Column('BULLETIN_ID', db.ForeignKey(u'fa_bulletin.ID'), primary_key=True, nullable=False),
    db.Column('ROLE_ID', db.ForeignKey(u'fa_role.ID'), primary_key=True, nullable=False)
)



class FaBulletinType(db.Model):
    __tablename__ = 'fa_bulletin_type'

    ID = db.Column(db.Integer, primary_key=True)
    NAME = db.Column(db.String(80))



class FaConfig(db.Model):
    __tablename__ = 'fa_config'

    ID = db.Column(db.Integer, primary_key=True)
    TYPE = db.Column(db.String(10))
    CODE = db.Column(db.String(32), nullable=False)
    NAME = db.Column(db.String(50))
    VALUE = db.Column(db.String(300))
    REMARK = db.Column(db.String(500))
    REGION = db.Column(db.String(10), nullable=False)
    ADD_USER_ID = db.Column(db.Integer)
    ADD_TIEM = db.Column(db.DateTime)



class FaDbServer(db.Model):
    __tablename__ = 'fa_db_server'

    ID = db.Column(db.Integer, primary_key=True)
    DB_TYPE_ID = db.Column(db.ForeignKey(u'fa_db_server_type.ID'), nullable=False)
    TYPE = db.Column(db.String(10), nullable=False)
    IP = db.Column(db.String(20), nullable=False)
    PORT = db.Column(db.Integer, nullable=False)
    DBNAME = db.Column(db.String(20))
    DBUID = db.Column(db.String(20), nullable=False)
    PASSWORD = db.Column(db.String(32), nullable=False)
    REMARK = db.Column(db.String(500))
    DB_LINK = db.Column(db.String(200))
    NICKNAME = db.Column(db.String(32))
    TO_PATH_M = db.Column(db.String(300))
    TO_PATH_D = db.Column(db.String(300))

    fa_db_server_type = db.relationship(u'FaDbServerType', primaryjoin='FaDbServer.DB_TYPE_ID == FaDbServerType.ID', backref=u'fa_db_servers')



class FaDbServerType(db.Model):
    __tablename__ = 'fa_db_server_type'

    ID = db.Column(db.Integer, primary_key=True)
    NAME = db.Column(db.String(20))
    REMARK = db.Column(db.String(500))



class FaDistrict(db.Model):
    __tablename__ = 'fa_district'

    ID = db.Column(db.Integer, primary_key=True)
    PARENT_ID = db.Column(db.ForeignKey(u'fa_district.ID'))
    NAME = db.Column(db.String(255), nullable=False)
    CODE = db.Column(db.String(50))
    IN_USE = db.Column(db.Numeric(1, 0), nullable=False)
    LEVEL_ID = db.Column(db.Integer, nullable=False)
    ID_PATH = db.Column(db.String(200))
    REGION = db.Column(db.String(10), nullable=False)

    parent = db.relationship(u'FaDistrict', remote_side=[ID], primaryjoin='FaDistrict.PARENT_ID == FaDistrict.ID', backref=u'fa_districts')
    fa_user = db.relationship(u'FaUser', secondary=u'fa_user_district', backref=u'fa_districts')



class FaDynasty(db.Model):
    __tablename__ = 'fa_dynasty'

    ID = db.Column(db.Integer, primary_key=True)
    NAME = db.Column(db.String(20), nullable=False)



class FaElder(db.Model):
    __tablename__ = 'fa_elder'

    ID = db.Column(db.Integer, primary_key=True)
    FAMILY_ID = db.Column(db.ForeignKey(u'fa_family.ID'))
    NAME = db.Column(db.String(2), nullable=False)
    SORT = db.Column(db.Integer)

    fa_family = db.relationship(u'FaFamily', primaryjoin='FaElder.FAMILY_ID == FaFamily.ID', backref=u'fa_elders')



t_fa_event_files = db.Table(
    'fa_event_files',
    db.Column('EVENT_ID', db.ForeignKey(u'fa_user_event.ID'), primary_key=True, nullable=False),
    db.Column('FILES_ID', db.ForeignKey(u'fa_files.ID'), primary_key=True, nullable=False)
)



class FaExportLog(db.Model):
    __tablename__ = 'fa_export_log'

    ID = db.Column(db.Integer, primary_key=True)
    USER_ID = db.Column(db.Integer)
    LOGIN_NAME = db.Column(db.String(50))
    NAME = db.Column(db.String(50))
    SQL_CONTENT = db.Column(db.Text)
    EXPORT_TIME = db.Column(db.DateTime)
    REMARK = db.Column(db.String(100))



class FaFamily(db.Model):
    __tablename__ = 'fa_family'

    ID = db.Column(db.Integer, primary_key=True)
    NAME = db.Column(db.String(20), nullable=False)



class FaFile(db.Model):
    __tablename__ = 'fa_files'

    ID = db.Column(db.Integer, primary_key=True)
    NAME = db.Column(db.String(50), nullable=False)
    PATH = db.Column(db.String(200), nullable=False)
    USER_ID = db.Column(db.Integer)
    LENGTH = db.Column(db.Integer, nullable=False)
    UPLOAD_TIME = db.Column(db.DateTime)
    REMARK = db.Column(db.String(2000))
    URL = db.Column(db.String(254))
    FILE_TYPE = db.Column(db.String(50))

    fa_task_flow_handle = db.relationship(u'FaTaskFlowHandle', secondary=u'fa_task_flow_handle_files', backref=u'fa_files')



class FaFlow(db.Model):
    __tablename__ = 'fa_flow'

    ID = db.Column(db.Integer, primary_key=True)
    NAME = db.Column(db.String(100), nullable=False)
    FLOW_TYPE = db.Column(db.String(20), nullable=False)
    REMARK = db.Column(db.String(100))
    X_Y = db.Column(db.String(500))
    REGION = db.Column(db.String(10))



class FaFlowFlownode(db.Model):
    __tablename__ = 'fa_flow_flownode'

    ID = db.Column(db.Integer, primary_key=True)
    NAME = db.Column(db.String(100), nullable=False)
    HANDLE_URL = db.Column(db.String(200))
    SHOW_URL = db.Column(db.String(200))



class FaFlowFlownodeFlow(db.Model):
    __tablename__ = 'fa_flow_flownode_flow'

    ID = db.Column(db.Integer, primary_key=True)
    FLOW_ID = db.Column(db.ForeignKey(u'fa_flow.ID'), nullable=False)
    FROM_FLOWNODE_ID = db.Column(db.ForeignKey(u'fa_flow_flownode.ID'), nullable=False)
    TO_FLOWNODE_ID = db.Column(db.Integer, nullable=False)
    HANDLE = db.Column(db.Numeric(1, 0), nullable=False)
    ASSIGNER = db.Column(db.Numeric(1, 0), nullable=False)
    STATUS = db.Column(db.String(20))
    REMARK = db.Column(db.String(20))
    EXPIRE_HOUR = db.Column(db.Integer, nullable=False)

    fa_flow = db.relationship(u'FaFlow', primaryjoin='FaFlowFlownodeFlow.FLOW_ID == FaFlow.ID', backref=u'fa_flow_flownode_flows')
    fa_flow_flownode = db.relationship(u'FaFlowFlownode', primaryjoin='FaFlowFlownodeFlow.FROM_FLOWNODE_ID == FaFlowFlownode.ID', backref=u'fa_flow_flownode_flows')
    fa_role = db.relationship(u'FaRole', secondary=u'fa_flow_flownode_role', backref=u'fa_flow_flownode_flows')



t_fa_flow_flownode_role = db.Table(
    'fa_flow_flownode_role',
    db.Column('FLOW_ID', db.ForeignKey(u'fa_flow_flownode_flow.ID'), primary_key=True, nullable=False),
    db.Column('ROLE_ID', db.ForeignKey(u'fa_role.ID'), primary_key=True, nullable=False)
)



class FaFunction(db.Model):
    __tablename__ = 'fa_function'

    ID = db.Column(db.Integer, primary_key=True)
    REMARK = db.Column(db.String(100))
    FULL_NAME = db.Column(db.String(100))
    NAMESPACE = db.Column(db.String(100))
    CLASS_NAME = db.Column(db.String(100))
    METHOD_NAME = db.Column(db.String(100))
    DLL_NAME = db.Column(db.String(100))
    XML_NOTE = db.Column(db.String(254))

    fa_role = db.relationship(u'FaRole', secondary=u'fa_role_function', backref=u'fa_functions')



class FaLog(db.Model):
    __tablename__ = 'fa_log'

    ID = db.Column(db.Integer, primary_key=True)
    ADD_TIME = db.Column(db.DateTime, nullable=False)
    MODULE_NAME = db.Column(db.String(100), nullable=False)
    USER_ID = db.Column(db.Integer, nullable=False)



class FaLogin(db.Model):
    __tablename__ = 'fa_login'

    ID = db.Column(db.Integer, primary_key=True)
    LOGIN_NAME = db.Column(db.String(20))
    PASSWORD = db.Column(db.String(255))
    PHONE_NO = db.Column(db.String(20))
    EMAIL_ADDR = db.Column(db.String(255))
    VERIFY_CODE = db.Column(db.String(10))
    VERIFY_TIME = db.Column(db.DateTime)
    IS_LOCKED = db.Column(db.Integer)
    PASS_UPDATE_DATE = db.Column(db.DateTime)
    LOCKED_REASON = db.Column(db.String(255))
    FAIL_COUNT = db.Column(db.Integer)

    fa_oauth = db.relationship(u'FaOauth', secondary=u'fa_oauth_login', backref=u'fa_logins')



class FaLoginHistory(db.Model):
    __tablename__ = 'fa_login_history'

    ID = db.Column(db.Integer, primary_key=True)
    USER_ID = db.Column(db.Integer)
    LOGIN_TIME = db.Column(db.DateTime)
    LOGIN_HOST = db.Column(db.String(255))
    LOGOUT_TIME = db.Column(db.DateTime)
    LOGIN_HISTORY_TYPE = db.Column(db.Integer)
    MESSAGE = db.Column(db.String(255))



class FaMessage(db.Model):
    __tablename__ = 'fa_message'

    ID = db.Column(db.Integer, primary_key=True)
    MESSAGE_TYPE_ID = db.Column(db.ForeignKey(u'fa_message_type.ID'))
    KEY_ID = db.Column(db.Integer)
    TITLE = db.Column(db.String(100))
    CONTENT = db.Column(db.String(500))
    CREATE_TIME = db.Column(db.DateTime)
    CREATE_USERNAME = db.Column(db.String(50))
    CREATE_USERID = db.Column(db.Integer)
    STATUS = db.Column(db.String(10))
    PUSH_TYPE = db.Column(db.String(10))
    DISTRICT_ID = db.Column(db.Integer)
    ALL_ROLE_ID = db.Column(db.String(500))

    fa_message_type = db.relationship(u'FaMessageType', primaryjoin='FaMessage.MESSAGE_TYPE_ID == FaMessageType.ID', backref=u'fa_messages')



class FaMessageType(db.Model):
    __tablename__ = 'fa_message_type'

    ID = db.Column(db.Integer, primary_key=True)
    NAME = db.Column(db.String(50))
    TABLE_NAME = db.Column(db.String(50))
    IS_USE = db.Column(db.Integer)
    REMARK = db.Column(db.String(500))



class FaModule(db.Model):
    __tablename__ = 'fa_module'

    ID = db.Column(db.Integer, primary_key=True)
    PARENT_ID = db.Column(db.ForeignKey(u'fa_module.ID'))
    NAME = db.Column(db.String(60))
    LOCATION = db.Column(db.String(2000))
    CODE = db.Column(db.String(20))
    IS_DEBUG = db.Column(db.Numeric(1, 0), nullable=False)
    IS_HIDE = db.Column(db.Numeric(1, 0), nullable=False)
    SHOW_ORDER = db.Column(db.Numeric(2, 0), nullable=False)
    DESCRIPTION = db.Column(db.String(2000))
    IMAGE_URL = db.Column(db.String(2000))
    DESKTOP_ROLE = db.Column(db.String(200))
    W = db.Column(db.Integer)
    H = db.Column(db.Integer)

    parent = db.relationship(u'FaModule', remote_side=[ID], primaryjoin='FaModule.PARENT_ID == FaModule.ID', backref=u'fa_modules')
    fa_role = db.relationship(u'FaRole', secondary=u'fa_role_module', backref=u'fa_modules')
    fa_user = db.relationship(u'FaUser', secondary=u'fa_user_module', backref=u'fa_modules')



class FaOauth(db.Model):
    __tablename__ = 'fa_oauth'

    ID = db.Column(db.Integer, primary_key=True)
    NAME = db.Column(db.String(50))
    REG_URL = db.Column(db.String(500))
    LOGIN_URL = db.Column(db.String(500))
    REMARK = db.Column(db.String(500))



t_fa_oauth_login = db.Table(
    'fa_oauth_login',
    db.Column('OAUTH_ID', db.ForeignKey(u'fa_oauth.ID'), primary_key=True, nullable=False),
    db.Column('LOGIN_ID', db.ForeignKey(u'fa_login.ID'), primary_key=True, nullable=False)
)



class FaQuery(db.Model):
    __tablename__ = 'fa_query'

    ID = db.Column(db.Integer, primary_key=True)
    NAME = db.Column(db.String(50), nullable=False)
    CODE = db.Column(db.String(20), nullable=False)
    AUTO_LOAD = db.Column(db.Numeric(1, 0), nullable=False)
    PAGE_SIZE = db.Column(db.Integer, nullable=False)
    SHOW_CHECKBOX = db.Column(db.Numeric(1, 0), nullable=False)
    IS_DEBUG = db.Column(db.Numeric(1, 0), nullable=False)
    FILTR_LEVEL = db.Column(db.Numeric(1, 0))
    DB_SERVER_ID = db.Column(db.Integer)
    QUERY_CONF = db.Column(db.Text)
    QUERY_CFG_JSON = db.Column(db.Text)
    IN_PARA_JSON = db.Column(db.Text)
    JS_STR = db.Column(db.Text)
    ROWS_BTN = db.Column(db.Text)
    HEARD_BTN = db.Column(db.Text)
    REPORT_SCRIPT = db.Column(db.Text)
    CHARTS_CFG = db.Column(db.Text)
    CHARTS_TYPE = db.Column(db.String(50))
    FILTR_STR = db.Column(db.Text)
    REMARK = db.Column(db.Text)
    NEW_DATA = db.Column(db.String(50))



class FaRole(db.Model):
    __tablename__ = 'fa_role'

    ID = db.Column(db.Integer, primary_key=True)
    NAME = db.Column(db.String(80))
    REMARK = db.Column(db.String(255))
    TYPE = db.Column(db.Integer)

    fa_user = db.relationship(u'FaUser', secondary=u'fa_user_role', backref=u'fa_roles')



class FaRoleConfig(db.Model):
    __tablename__ = 'fa_role_config'

    ID = db.Column(db.Integer, primary_key=True)
    ROLE_ID = db.Column(db.ForeignKey(u'fa_role.ID'), nullable=False)
    TYPE = db.Column(db.String(10))
    NAME = db.Column(db.String(50), nullable=False)
    VALUE = db.Column(db.String(300))
    REMARK = db.Column(db.String(500))

    fa_role = db.relationship(u'FaRole', primaryjoin='FaRoleConfig.ROLE_ID == FaRole.ID', backref=u'fa_role_configs')



t_fa_role_function = db.Table(
    'fa_role_function',
    db.Column('FUNCTION_ID', db.ForeignKey(u'fa_function.ID'), primary_key=True, nullable=False),
    db.Column('ROLE_ID', db.ForeignKey(u'fa_role.ID'), primary_key=True, nullable=False)
)



t_fa_role_module = db.Table(
    'fa_role_module',
    db.Column('ROLE_ID', db.ForeignKey(u'fa_role.ID'), primary_key=True, nullable=False),
    db.Column('MODULE_ID', db.ForeignKey(u'fa_module.ID'), primary_key=True, nullable=False)
)



class FaRoleQueryAuthority(db.Model):
    __tablename__ = 'fa_role_query_authority'

    ROLE_ID = db.Column(db.ForeignKey(u'fa_role.ID'), primary_key=True, nullable=False)
    QUERY_ID = db.Column(db.ForeignKey(u'fa_query.ID'), primary_key=True, nullable=False)
    NO_AUTHORITY = db.Column(db.String(200))

    fa_query = db.relationship(u'FaQuery', primaryjoin='FaRoleQueryAuthority.QUERY_ID == FaQuery.ID', backref=u'fa_role_query_authorities')
    fa_role = db.relationship(u'FaRole', primaryjoin='FaRoleQueryAuthority.ROLE_ID == FaRole.ID', backref=u'fa_role_query_authorities')



class FaScript(db.Model):
    __tablename__ = 'fa_script'

    ID = db.Column(db.Integer, primary_key=True)
    CODE = db.Column(db.String(20), nullable=False)
    NAME = db.Column(db.String(255), nullable=False)
    BODY_TEXT = db.Column(db.Text, nullable=False)
    BODY_HASH = db.Column(db.String(255), nullable=False)
    RUN_WHEN = db.Column(db.String(30))
    RUN_ARGS = db.Column(db.String(255))
    RUN_DATA = db.Column(db.String(20), nullable=False, server_default=db.FetchedValue())
    STATUS = db.Column(db.String(10))
    DISABLE_REASON = db.Column(db.String(50))
    SERVICE_FLAG = db.Column(db.String(50))
    REGION = db.Column(db.String(10))
    IS_GROUP = db.Column(db.Numeric(1, 0), nullable=False)



class FaScriptGroupList(db.Model):
    __tablename__ = 'fa_script_group_list'

    SCRIPT_ID = db.Column(db.Integer, primary_key=True, nullable=False)
    GROUP_ID = db.Column(db.ForeignKey(u'fa_script.ID'), primary_key=True, nullable=False)
    ORDER_INDEX = db.Column(db.Integer, nullable=False)

    fa_script = db.relationship(u'FaScript', primaryjoin='FaScriptGroupList.GROUP_ID == FaScript.ID', backref=u'fa_script_group_lists')



class FaScriptTask(db.Model):
    __tablename__ = 'fa_script_task'

    ID = db.Column(db.Integer, primary_key=True)
    SCRIPT_ID = db.Column(db.ForeignKey(u'fa_script.ID'), nullable=False)
    BODY_TEXT = db.Column(db.Text, nullable=False)
    BODY_HASH = db.Column(db.String(255), nullable=False)
    RUN_STATE = db.Column(db.String(10), nullable=False, server_default=db.FetchedValue())
    RUN_WHEN = db.Column(db.String(30))
    RUN_ARGS = db.Column(db.String(255))
    RUN_DATA = db.Column(db.String(20), nullable=False, server_default=db.FetchedValue())
    LOG_TYPE = db.Column(db.Numeric(1, 0), server_default=db.FetchedValue())
    DSL_TYPE = db.Column(db.String(255))
    RETURN_CODE = db.Column(db.String(10), server_default=db.FetchedValue())
    START_TIME = db.Column(db.DateTime)
    END_TIME = db.Column(db.DateTime)
    DISABLE_DATE = db.Column(db.DateTime)
    DISABLE_REASON = db.Column(db.String(50))
    SERVICE_FLAG = db.Column(db.String(50))
    REGION = db.Column(db.String(10))
    GROUP_ID = db.Column(db.Integer)

    fa_script = db.relationship(u'FaScript', primaryjoin='FaScriptTask.SCRIPT_ID == FaScript.ID', backref=u'fa_script_tasks')



class FaScriptTaskLog(db.Model):
    __tablename__ = 'fa_script_task_log'

    ID = db.Column(db.Integer, primary_key=True)
    SCRIPT_TASK_ID = db.Column(db.ForeignKey(u'fa_script_task.ID'), nullable=False)
    LOG_TIME = db.Column(db.DateTime, nullable=False)
    LOG_TYPE = db.Column(db.Numeric(1, 0), nullable=False, server_default=db.FetchedValue())
    MESSAGE = db.Column(db.Text)
    SQL_TEXT = db.Column(db.Text)

    fa_script_task = db.relationship(u'FaScriptTask', primaryjoin='FaScriptTaskLog.SCRIPT_TASK_ID == FaScriptTask.ID', backref=u'fa_script_task_logs')



class FaSmsSend(db.Model):
    __tablename__ = 'fa_sms_send'

    GUID = db.Column(db.String(32), primary_key=True)
    MESSAGE_ID = db.Column(db.Integer)
    PHONE_NO = db.Column(db.String(50), nullable=False)
    ADD_TIME = db.Column(db.DateTime)
    SEND_TIME = db.Column(db.DateTime)
    CONTENT = db.Column(db.String(500), nullable=False)
    STAUTS = db.Column(db.String(15))
    TRY_NUM = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())



class FaTask(db.Model):
    __tablename__ = 'fa_task'

    ID = db.Column(db.Integer, primary_key=True)
    FLOW_ID = db.Column(db.ForeignKey(u'fa_flow.ID'))
    TASK_NAME = db.Column(db.String(50))
    CREATE_TIME = db.Column(db.DateTime)
    CREATE_USER = db.Column(db.Integer)
    CREATE_USER_NAME = db.Column(db.String(50))
    STATUS = db.Column(db.String(50))
    STATUS_TIME = db.Column(db.DateTime)
    REMARK = db.Column(db.Text)
    REGION = db.Column(db.String(10))
    KEY_ID = db.Column(db.String(32))
    START_TIME = db.Column(db.DateTime)
    END_TIME = db.Column(db.DateTime)
    DEAL_TIME = db.Column(db.DateTime)
    ROLE_ID_STR = db.Column(db.String(200))

    fa_flow = db.relationship(u'FaFlow', primaryjoin='FaTask.FLOW_ID == FaFlow.ID', backref=u'fa_tasks')



class FaTaskFlow(db.Model):
    __tablename__ = 'fa_task_flow'

    ID = db.Column(db.Integer, primary_key=True)
    PARENT_ID = db.Column(db.ForeignKey(u'fa_task_flow.ID'))
    TASK_ID = db.Column(db.ForeignKey(u'fa_task.ID'), nullable=False)
    LEVEL_ID = db.Column(db.Integer)
    FLOWNODE_ID = db.Column(db.Integer)
    EQUAL_ID = db.Column(db.Integer)
    IS_HANDLE = db.Column(db.Integer, nullable=False)
    NAME = db.Column(db.String(100))
    HANDLE_URL = db.Column(db.String(200))
    SHOW_URL = db.Column(db.String(200))
    EXPIRE_TIME = db.Column(db.DateTime)
    START_TIME = db.Column(db.DateTime, nullable=False)
    DEAL_STATUS = db.Column(db.String(50))
    ROLE_ID_STR = db.Column(db.String(200))
    HANDLE_USER_ID = db.Column(db.Integer)
    DEAL_TIME = db.Column(db.DateTime)
    ACCEPT_TIME = db.Column(db.DateTime)

    parent = db.relationship(u'FaTaskFlow', remote_side=[ID], primaryjoin='FaTaskFlow.PARENT_ID == FaTaskFlow.ID', backref=u'fa_task_flows')
    fa_task = db.relationship(u'FaTask', primaryjoin='FaTaskFlow.TASK_ID == FaTask.ID', backref=u'fa_task_flows')



class FaTaskFlowHandle(db.Model):
    __tablename__ = 'fa_task_flow_handle'

    ID = db.Column(db.Integer, primary_key=True)
    TASK_FLOW_ID = db.Column(db.ForeignKey(u'fa_task_flow.ID'), nullable=False)
    DEAL_USER_ID = db.Column(db.Integer, nullable=False)
    DEAL_USER_NAME = db.Column(db.String(50), nullable=False)
    DEAL_TIME = db.Column(db.DateTime, nullable=False)
    CONTENT = db.Column(db.String(2000), nullable=False)

    fa_task_flow = db.relationship(u'FaTaskFlow', primaryjoin='FaTaskFlowHandle.TASK_FLOW_ID == FaTaskFlow.ID', backref=u'fa_task_flow_handles')



t_fa_task_flow_handle_files = db.Table(
    'fa_task_flow_handle_files',
    db.Column('FLOW_HANDLE_ID', db.ForeignKey(u'fa_task_flow_handle.ID'), primary_key=True, nullable=False),
    db.Column('FILES_ID', db.ForeignKey(u'fa_files.ID'), primary_key=True, nullable=False)
)



class FaTaskFlowHandleUser(db.Model):
    __tablename__ = 'fa_task_flow_handle_user'

    TASK_FLOW_ID = db.Column(db.ForeignKey(u'fa_task_flow.ID'), primary_key=True, nullable=False)
    HANDLE_USER_ID = db.Column(db.Integer, primary_key=True, nullable=False)

    fa_task_flow = db.relationship(u'FaTaskFlow', primaryjoin='FaTaskFlowHandleUser.TASK_FLOW_ID == FaTaskFlow.ID', backref=u'fa_task_flow_handle_users')



class FaUpdataLog(db.Model):
    __tablename__ = 'fa_updata_log'

    ID = db.Column(db.Integer, primary_key=True)
    CREATE_TIME = db.Column(db.DateTime)
    CREATE_USER_NAME = db.Column(db.String(50))
    CREATE_USER_ID = db.Column(db.Integer)
    OLD_CONTENT = db.Column(db.Text)
    NEW_CONTENT = db.Column(db.Text)
    TABLE_NAME = db.Column(db.String(50))



class FaUser(db.Model):
    __tablename__ = 'fa_user'

    ID = db.Column(db.Integer, primary_key=True)
    NAME = db.Column(db.String(80))
    LOGIN_NAME = db.Column(db.String(20))
    ICON_FILES_ID = db.Column(db.Integer)
    DISTRICT_ID = db.Column(db.ForeignKey(u'fa_district.ID'), nullable=False)
    IS_LOCKED = db.Column(db.Numeric(1, 0))
    CREATE_TIME = db.Column(db.DateTime)
    LOGIN_COUNT = db.Column(db.Integer)
    LAST_LOGIN_TIME = db.Column(db.DateTime)
    LAST_LOGOUT_TIME = db.Column(db.DateTime)
    LAST_ACTIVE_TIME = db.Column(db.DateTime)
    REMARK = db.Column(db.String(2000))

    fa_district = db.relationship(u'FaDistrict', primaryjoin='FaUser.DISTRICT_ID == FaDistrict.ID', backref=u'fa_users')
    fa_user_info = db.relationship(u'FaUserInfo', secondary=u'fa_user_friend', backref=u'fa_users', lazy="select")


class FaUserInfo(FaUser):
    __tablename__ = 'fa_user_info'

    ID = db.Column(db.ForeignKey(u'fa_user.ID'), primary_key=True)
    LEVEL_ID = db.Column(db.Integer)
    FAMILY_ID = db.Column(db.ForeignKey(u'fa_family.ID'))
    ELDER_ID = db.Column(db.ForeignKey(u'fa_elder.ID'))
    LEVEL_NAME = db.Column(db.String(2))
    FATHER_ID = db.Column(db.ForeignKey(u'fa_user_info.ID'))
    MOTHER_ID = db.Column(db.Integer)
    BIRTHDAY_TIME = db.Column(db.DateTime)
    BIRTHDAY_PLACE = db.Column(db.String(500))
    IS_LIVE = db.Column(db.Numeric(1, 0))
    DIED_TIME = db.Column(db.DateTime)
    DIED_PLACE = db.Column(db.String(500))
    SEX = db.Column(db.String(2))
    YEARS_TYPE = db.Column(db.String(10))
    CONSORT_ID = db.Column(db.Integer)
    STATUS = db.Column(db.String(10), nullable=False, server_default=db.FetchedValue())
    CREATE_USER_NAME = db.Column(db.String(50), nullable=False, server_default=db.FetchedValue())
    CREATE_USER_ID = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    UPDATE_TIME = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    UPDATE_USER_NAME = db.Column(db.String(50), nullable=False, server_default=db.FetchedValue())
    UPDATE_USER_ID = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())

    fa_elder = db.relationship(u'FaElder', primaryjoin='FaUserInfo.ELDER_ID == FaElder.ID', backref=u'fa_user_infos')
    fa_family = db.relationship(u'FaFamily', primaryjoin='FaUserInfo.FAMILY_ID == FaFamily.ID', backref=u'fa_user_infos')
    parent = db.relationship(u'FaUserInfo', remote_side=[ID], primaryjoin='FaUserInfo.FATHER_ID == FaUserInfo.ID', backref=u'fa_user_infos')



t_fa_user_district = db.Table(
    'fa_user_district',
    db.Column('USER_ID', db.ForeignKey(u'fa_user.ID'), primary_key=True, nullable=False),
    db.Column('DISTRICT_ID', db.ForeignKey(u'fa_district.ID'), primary_key=True, nullable=False)
)



class FaUserEvent(db.Model):
    __tablename__ = 'fa_user_event'

    ID = db.Column(db.Integer, primary_key=True)
    USER_ID = db.Column(db.ForeignKey(u'fa_user_info.ID'))
    NAME = db.Column(db.String(50))
    HAPPEN_TIME = db.Column(db.DateTime)
    CONTENT = db.Column(db.String(500))
    ADDRESS = db.Column(db.String(500))

    fa_user_info = db.relationship(u'FaUserInfo', primaryjoin='FaUserEvent.USER_ID == FaUserInfo.ID', backref=u'fa_user_events')
    fa_files = db.relationship(u'FaFile', secondary=u'fa_event_files', backref=u'fa_user_events')



t_fa_user_friend = db.Table(
    'fa_user_friend',
    db.Column('USER_ID', db.ForeignKey(u'fa_user_info.ID'), primary_key=True, nullable=False),
    db.Column('FRIEND_ID', db.ForeignKey(u'fa_user.ID'), primary_key=True, nullable=False)
)



class FaUserMessage(db.Model):
    __tablename__ = 'fa_user_message'

    MESSAGE_ID = db.Column(db.ForeignKey(u'fa_message.ID'), primary_key=True, nullable=False)
    USER_ID = db.Column(db.Integer, primary_key=True, nullable=False)
    PHONE_NO = db.Column(db.String(20))
    STATUS = db.Column(db.String(10))
    STATUS_TIME = db.Column(db.DateTime, nullable=False)
    REPLY = db.Column(db.String(500))
    PUSH_TYPE = db.Column(db.String(10))

    fa_message = db.relationship(u'FaMessage', primaryjoin='FaUserMessage.MESSAGE_ID == FaMessage.ID', backref=u'fa_user_messages')



t_fa_user_module = db.Table(
    'fa_user_module',
    db.Column('USER_ID', db.ForeignKey(u'fa_user.ID'), primary_key=True, nullable=False),
    db.Column('MODULE_ID', db.ForeignKey(u'fa_module.ID'), primary_key=True, nullable=False)
)



t_fa_user_role = db.Table(
    'fa_user_role',
    db.Column('ROLE_ID', db.ForeignKey(u'fa_role.ID'), primary_key=True, nullable=False),
    db.Column('USER_ID', db.ForeignKey(u'fa_user.ID'), primary_key=True, nullable=False)
)



class Sequence(db.Model):
    __tablename__ = 'sequence'

    seq_name = db.Column(db.String(50), primary_key=True)
    current_val = db.Column(db.Integer, nullable=False)
    increment_val = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
