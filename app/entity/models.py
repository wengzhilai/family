# coding: utf-8
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String, Table, Text, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class FaAppVersion(Base):
    __tablename__ = 'fa_app_version'

    ID = Column(Integer, primary_key=True)
    IS_NEW = Column(Numeric(1, 0), nullable=False)
    TYPE = Column(String(20), nullable=False)
    REMARK = Column(String(1000))
    UPDATE_TIME = Column(DateTime)
    UPDATE_URL = Column(String(200))


class FaBulletin(Base):
    __tablename__ = 'fa_bulletin'

    ID = Column(Integer, primary_key=True)
    TITLE = Column(String(255), nullable=False)
    PIC = Column(String(255))
    TYPE_CODE = Column(String(50))
    CONTENT = Column(Text)
    USER_ID = Column(Integer)
    PUBLISHER = Column(String(255), nullable=False)
    ISSUE_DATE = Column(DateTime, nullable=False)
    IS_SHOW = Column(Numeric(1, 0), nullable=False)
    IS_IMPORT = Column(Numeric(1, 0), nullable=False)
    IS_URGENT = Column(Numeric(1, 0), nullable=False)
    AUTO_PEN = Column(Numeric(1, 0), nullable=False)
    CREATE_TIME = Column(DateTime, nullable=False)
    UPDATE_TIME = Column(DateTime, nullable=False)
    REGION = Column(String(10), nullable=False)

    fa_files = relationship(u'FaFile', secondary='fa_bulletin_file')
    fa_role = relationship(u'FaRole', secondary='fa_bulletin_role')


t_fa_bulletin_file = Table(
    'fa_bulletin_file', metadata,
    Column('BULLETIN_ID', ForeignKey(u'fa_bulletin.ID'), primary_key=True, nullable=False),
    Column('FILE_ID', ForeignKey(u'fa_files.ID'), primary_key=True, nullable=False)
)


class FaBulletinLog(Base):
    __tablename__ = 'fa_bulletin_log'

    ID = Column(Integer, primary_key=True)
    BULLETIN_ID = Column(ForeignKey(u'fa_bulletin.ID'), nullable=False)
    USER_ID = Column(Integer, nullable=False)
    LOOK_TIME = Column(DateTime, nullable=False)

    fa_bulletin = relationship(u'FaBulletin')


class FaBulletinReview(Base):
    __tablename__ = 'fa_bulletin_review'

    ID = Column(Integer, primary_key=True)
    PARENT_ID = Column(ForeignKey(u'fa_bulletin_review.ID'))
    BULLETIN_ID = Column(ForeignKey(u'fa_bulletin.ID'), nullable=False)
    NAME = Column(String(50))
    CONTENT = Column(Text)
    USER_ID = Column(Integer, nullable=False)
    ADD_TIME = Column(DateTime, nullable=False)
    STATUS = Column(String(10), nullable=False)
    STATUS_TIME = Column(DateTime, nullable=False)

    fa_bulletin = relationship(u'FaBulletin')
    parent = relationship(u'FaBulletinReview', remote_side=[ID])


t_fa_bulletin_role = Table(
    'fa_bulletin_role', metadata,
    Column('BULLETIN_ID', ForeignKey(u'fa_bulletin.ID'), primary_key=True, nullable=False),
    Column('ROLE_ID', ForeignKey(u'fa_role.ID'), primary_key=True, nullable=False)
)


class FaBulletinType(Base):
    __tablename__ = 'fa_bulletin_type'

    ID = Column(Integer, primary_key=True)
    NAME = Column(String(80))


class FaConfig(Base):
    __tablename__ = 'fa_config'

    ID = Column(Integer, primary_key=True)
    TYPE = Column(String(10))
    CODE = Column(String(32), nullable=False)
    NAME = Column(String(50))
    VALUE = Column(String(300))
    REMARK = Column(String(500))
    REGION = Column(String(10), nullable=False)
    ADD_USER_ID = Column(Integer)
    ADD_TIEM = Column(DateTime)


class FaDbServer(Base):
    __tablename__ = 'fa_db_server'

    ID = Column(Integer, primary_key=True)
    DB_TYPE_ID = Column(ForeignKey(u'fa_db_server_type.ID'), nullable=False)
    TYPE = Column(String(10), nullable=False)
    IP = Column(String(20), nullable=False)
    PORT = Column(Integer, nullable=False)
    DBNAME = Column(String(20))
    DBUID = Column(String(20), nullable=False)
    PASSWORD = Column(String(32), nullable=False)
    REMARK = Column(String(500))
    DB_LINK = Column(String(200))
    NICKNAME = Column(String(32))
    TO_PATH_M = Column(String(300))
    TO_PATH_D = Column(String(300))

    fa_db_server_type = relationship(u'FaDbServerType')


class FaDbServerType(Base):
    __tablename__ = 'fa_db_server_type'

    ID = Column(Integer, primary_key=True)
    NAME = Column(String(20))
    REMARK = Column(String(500))


class FaDistrict(Base):
    __tablename__ = 'fa_district'

    ID = Column(Integer, primary_key=True)
    PARENT_ID = Column(ForeignKey(u'fa_district.ID'))
    NAME = Column(String(255), nullable=False)
    CODE = Column(String(50))
    IN_USE = Column(Numeric(1, 0), nullable=False)
    LEVEL_ID = Column(Integer, nullable=False)
    ID_PATH = Column(String(200))
    REGION = Column(String(10), nullable=False)

    parent = relationship(u'FaDistrict', remote_side=[ID])
    fa_user = relationship(u'FaUser', secondary='fa_user_district')


class FaDynasty(Base):
    __tablename__ = 'fa_dynasty'

    ID = Column(Integer, primary_key=True)
    NAME = Column(String(20), nullable=False)


class FaElder(Base):
    __tablename__ = 'fa_elder'

    ID = Column(Integer, primary_key=True)
    FAMILY_ID = Column(ForeignKey(u'fa_family.ID'))
    NAME = Column(String(2), nullable=False)
    SORT = Column(Integer)

    fa_family = relationship(u'FaFamily')


t_fa_event_files = Table(
    'fa_event_files', metadata,
    Column('EVENT_ID', ForeignKey(u'fa_user_event.ID'), primary_key=True, nullable=False),
    Column('FILES_ID', ForeignKey(u'fa_files.ID'), primary_key=True, nullable=False)
)


class FaExportLog(Base):
    __tablename__ = 'fa_export_log'

    ID = Column(Integer, primary_key=True)
    USER_ID = Column(Integer)
    LOGIN_NAME = Column(String(50))
    NAME = Column(String(50))
    SQL_CONTENT = Column(Text)
    EXPORT_TIME = Column(DateTime)
    REMARK = Column(String(100))


class FaFamily(Base):
    __tablename__ = 'fa_family'

    ID = Column(Integer, primary_key=True)
    NAME = Column(String(20), nullable=False)


class FaFile(Base):
    __tablename__ = 'fa_files'

    ID = Column(Integer, primary_key=True)
    NAME = Column(String(50), nullable=False)
    PATH = Column(String(200), nullable=False)
    USER_ID = Column(Integer)
    LENGTH = Column(Integer, nullable=False)
    UPLOAD_TIME = Column(DateTime)
    REMARK = Column(String(2000))
    URL = Column(String(254))
    FILE_TYPE = Column(String(50))

    fa_task_flow_handle = relationship(u'FaTaskFlowHandle', secondary='fa_task_flow_handle_files')


class FaFlow(Base):
    __tablename__ = 'fa_flow'

    ID = Column(Integer, primary_key=True)
    NAME = Column(String(100), nullable=False)
    FLOW_TYPE = Column(String(20), nullable=False)
    REMARK = Column(String(100))
    X_Y = Column(String(500))
    REGION = Column(String(10))


class FaFlowFlownode(Base):
    __tablename__ = 'fa_flow_flownode'

    ID = Column(Integer, primary_key=True)
    NAME = Column(String(100), nullable=False)
    HANDLE_URL = Column(String(200))
    SHOW_URL = Column(String(200))


class FaFlowFlownodeFlow(Base):
    __tablename__ = 'fa_flow_flownode_flow'

    ID = Column(Integer, primary_key=True)
    FLOW_ID = Column(ForeignKey(u'fa_flow.ID'), nullable=False)
    FROM_FLOWNODE_ID = Column(ForeignKey(u'fa_flow_flownode.ID'), nullable=False)
    TO_FLOWNODE_ID = Column(Integer, nullable=False)
    HANDLE = Column(Numeric(1, 0), nullable=False)
    ASSIGNER = Column(Numeric(1, 0), nullable=False)
    STATUS = Column(String(20))
    REMARK = Column(String(20))
    EXPIRE_HOUR = Column(Integer, nullable=False)

    fa_flow = relationship(u'FaFlow')
    fa_flow_flownode = relationship(u'FaFlowFlownode')
    fa_role = relationship(u'FaRole', secondary='fa_flow_flownode_role')


t_fa_flow_flownode_role = Table(
    'fa_flow_flownode_role', metadata,
    Column('FLOW_ID', ForeignKey(u'fa_flow_flownode_flow.ID'), primary_key=True, nullable=False),
    Column('ROLE_ID', ForeignKey(u'fa_role.ID'), primary_key=True, nullable=False)
)


class FaFunction(Base):
    __tablename__ = 'fa_function'

    ID = Column(Integer, primary_key=True)
    REMARK = Column(String(100))
    FULL_NAME = Column(String(100))
    NAMESPACE = Column(String(100))
    CLASS_NAME = Column(String(100))
    METHOD_NAME = Column(String(100))
    DLL_NAME = Column(String(100))
    XML_NOTE = Column(String(254))

    fa_role = relationship(u'FaRole', secondary='fa_role_function')


class FaLog(Base):
    __tablename__ = 'fa_log'

    ID = Column(Integer, primary_key=True)
    ADD_TIME = Column(DateTime, nullable=False)
    MODULE_NAME = Column(String(100), nullable=False)
    USER_ID = Column(Integer, nullable=False)


class FaLogin(Base):
    __tablename__ = 'fa_login'

    ID = Column(Integer, primary_key=True)
    LOGIN_NAME = Column(String(20))
    PASSWORD = Column(String(255))
    PHONE_NO = Column(String(20))
    EMAIL_ADDR = Column(String(255))
    VERIFY_CODE = Column(String(10))
    VERIFY_TIME = Column(DateTime)
    IS_LOCKED = Column(Integer)
    PASS_UPDATE_DATE = Column(DateTime)
    LOCKED_REASON = Column(String(255))
    REGION = Column(String(10), nullable=False)
    FAIL_COUNT = Column(Integer)

    fa_oauth = relationship(u'FaOauth', secondary='fa_oauth_login')


class FaLoginHistory(Base):
    __tablename__ = 'fa_login_history'

    ID = Column(Integer, primary_key=True)
    USER_ID = Column(Integer)
    LOGIN_TIME = Column(DateTime)
    LOGIN_HOST = Column(String(255))
    LOGOUT_TIME = Column(DateTime)
    LOGIN_HISTORY_TYPE = Column(Integer)
    MESSAGE = Column(String(255))


class FaMessage(Base):
    __tablename__ = 'fa_message'

    ID = Column(Integer, primary_key=True)
    MESSAGE_TYPE_ID = Column(ForeignKey(u'fa_message_type.ID'))
    KEY_ID = Column(Integer)
    TITLE = Column(String(100))
    CONTENT = Column(String(500))
    CREATE_TIME = Column(DateTime)
    CREATE_USERNAME = Column(String(50))
    CREATE_USERID = Column(Integer)
    STATUS = Column(String(10))
    PUSH_TYPE = Column(String(10))
    DISTRICT_ID = Column(Integer)
    ALL_ROLE_ID = Column(String(500))

    fa_message_type = relationship(u'FaMessageType')


class FaMessageType(Base):
    __tablename__ = 'fa_message_type'

    ID = Column(Integer, primary_key=True)
    NAME = Column(String(50))
    TABLE_NAME = Column(String(50))
    IS_USE = Column(Integer)
    REMARK = Column(String(500))


class FaModule(Base):
    __tablename__ = 'fa_module'

    ID = Column(Integer, primary_key=True)
    PARENT_ID = Column(ForeignKey(u'fa_module.ID'))
    NAME = Column(String(60))
    LOCATION = Column(String(2000))
    CODE = Column(String(20))
    IS_DEBUG = Column(Numeric(1, 0), nullable=False)
    IS_HIDE = Column(Numeric(1, 0), nullable=False)
    SHOW_ORDER = Column(Numeric(2, 0), nullable=False)
    DESCRIPTION = Column(String(2000))
    IMAGE_URL = Column(String(2000))
    DESKTOP_ROLE = Column(String(200))
    W = Column(Integer)
    H = Column(Integer)

    parent = relationship(u'FaModule', remote_side=[ID])
    fa_role = relationship(u'FaRole', secondary='fa_role_module')
    fa_user = relationship(u'FaUser', secondary='fa_user_module')


class FaOauth(Base):
    __tablename__ = 'fa_oauth'

    ID = Column(Integer, primary_key=True)
    NAME = Column(String(50))
    REG_URL = Column(String(500))
    LOGIN_URL = Column(String(500))
    REMARK = Column(String(500))


t_fa_oauth_login = Table(
    'fa_oauth_login', metadata,
    Column('OAUTH_ID', ForeignKey(u'fa_oauth.ID'), primary_key=True, nullable=False),
    Column('LOGIN_ID', ForeignKey(u'fa_login.ID'), primary_key=True, nullable=False)
)


class FaQuery(Base):
    __tablename__ = 'fa_query'

    ID = Column(Integer, primary_key=True)
    NAME = Column(String(50), nullable=False)
    CODE = Column(String(20), nullable=False)
    AUTO_LOAD = Column(Numeric(1, 0), nullable=False)
    PAGE_SIZE = Column(Integer, nullable=False)
    SHOW_CHECKBOX = Column(Numeric(1, 0), nullable=False)
    IS_DEBUG = Column(Numeric(1, 0), nullable=False)
    FILTR_LEVEL = Column(Numeric(1, 0))
    DB_SERVER_ID = Column(Integer)
    QUERY_CONF = Column(Text)
    QUERY_CFG_JSON = Column(Text)
    IN_PARA_JSON = Column(Text)
    JS_STR = Column(Text)
    ROWS_BTN = Column(Text)
    HEARD_BTN = Column(Text)
    REPORT_SCRIPT = Column(Text)
    CHARTS_CFG = Column(Text)
    CHARTS_TYPE = Column(String(50))
    FILTR_STR = Column(Text)
    REMARK = Column(Text)
    NEW_DATA = Column(String(50))


class FaRole(Base):
    __tablename__ = 'fa_role'

    ID = Column(Integer, primary_key=True)
    NAME = Column(String(80))
    REMARK = Column(String(255))
    TYPE = Column(Integer)

    fa_user = relationship(u'FaUser', secondary='fa_user_role')


class FaRoleConfig(Base):
    __tablename__ = 'fa_role_config'

    ID = Column(Integer, primary_key=True)
    ROLE_ID = Column(ForeignKey(u'fa_role.ID'), nullable=False)
    TYPE = Column(String(10))
    NAME = Column(String(50), nullable=False)
    VALUE = Column(String(300))
    REMARK = Column(String(500))

    fa_role = relationship(u'FaRole')


t_fa_role_function = Table(
    'fa_role_function', metadata,
    Column('FUNCTION_ID', ForeignKey(u'fa_function.ID'), primary_key=True, nullable=False),
    Column('ROLE_ID', ForeignKey(u'fa_role.ID'), primary_key=True, nullable=False)
)


t_fa_role_module = Table(
    'fa_role_module', metadata,
    Column('ROLE_ID', ForeignKey(u'fa_role.ID'), primary_key=True, nullable=False),
    Column('MODULE_ID', ForeignKey(u'fa_module.ID'), primary_key=True, nullable=False)
)


class FaRoleQueryAuthority(Base):
    __tablename__ = 'fa_role_query_authority'

    ROLE_ID = Column(ForeignKey(u'fa_role.ID'), primary_key=True, nullable=False)
    QUERY_ID = Column(ForeignKey(u'fa_query.ID'), primary_key=True, nullable=False)
    NO_AUTHORITY = Column(String(200))

    fa_query = relationship(u'FaQuery')
    fa_role = relationship(u'FaRole')


class FaScript(Base):
    __tablename__ = 'fa_script'

    ID = Column(Integer, primary_key=True)
    CODE = Column(String(20), nullable=False)
    NAME = Column(String(255), nullable=False)
    BODY_TEXT = Column(Text, nullable=False)
    BODY_HASH = Column(String(255), nullable=False)
    RUN_WHEN = Column(String(30))
    RUN_ARGS = Column(String(255))
    RUN_DATA = Column(String(20), nullable=False, server_default=text("'0'"))
    STATUS = Column(String(10))
    DISABLE_REASON = Column(String(50))
    SERVICE_FLAG = Column(String(50))
    REGION = Column(String(10))
    IS_GROUP = Column(Numeric(1, 0), nullable=False)


class FaScriptGroupList(Base):
    __tablename__ = 'fa_script_group_list'

    SCRIPT_ID = Column(Integer, primary_key=True, nullable=False)
    GROUP_ID = Column(ForeignKey(u'fa_script.ID'), primary_key=True, nullable=False)
    ORDER_INDEX = Column(Integer, nullable=False)

    fa_script = relationship(u'FaScript')


class FaScriptTask(Base):
    __tablename__ = 'fa_script_task'

    ID = Column(Integer, primary_key=True)
    SCRIPT_ID = Column(ForeignKey(u'fa_script.ID'), nullable=False)
    BODY_TEXT = Column(Text, nullable=False)
    BODY_HASH = Column(String(255), nullable=False)
    RUN_STATE = Column(String(10), nullable=False, server_default=text("'0'"))
    RUN_WHEN = Column(String(30))
    RUN_ARGS = Column(String(255))
    RUN_DATA = Column(String(20), nullable=False, server_default=text("'0'"))
    LOG_TYPE = Column(Numeric(1, 0), server_default=text("'0'"))
    DSL_TYPE = Column(String(255))
    RETURN_CODE = Column(String(10), server_default=text("'0'"))
    START_TIME = Column(DateTime)
    END_TIME = Column(DateTime)
    DISABLE_DATE = Column(DateTime)
    DISABLE_REASON = Column(String(50))
    SERVICE_FLAG = Column(String(50))
    REGION = Column(String(10))
    GROUP_ID = Column(Integer)

    fa_script = relationship(u'FaScript')


class FaScriptTaskLog(Base):
    __tablename__ = 'fa_script_task_log'

    ID = Column(Integer, primary_key=True)
    SCRIPT_TASK_ID = Column(ForeignKey(u'fa_script_task.ID'), nullable=False)
    LOG_TIME = Column(DateTime, nullable=False)
    LOG_TYPE = Column(Numeric(1, 0), nullable=False, server_default=text("'1'"))
    MESSAGE = Column(Text)
    SQL_TEXT = Column(Text)

    fa_script_task = relationship(u'FaScriptTask')


class FaSmsSend(Base):
    __tablename__ = 'fa_sms_send'

    GUID = Column(String(32), primary_key=True)
    MESSAGE_ID = Column(Integer)
    PHONE_NO = Column(String(50), nullable=False)
    ADD_TIME = Column(DateTime)
    SEND_TIME = Column(DateTime)
    CONTENT = Column(String(500), nullable=False)
    STAUTS = Column(String(15))
    TRY_NUM = Column(Integer, nullable=False, server_default=text("'0'"))


class FaTask(Base):
    __tablename__ = 'fa_task'

    ID = Column(Integer, primary_key=True)
    FLOW_ID = Column(ForeignKey(u'fa_flow.ID'))
    TASK_NAME = Column(String(50))
    CREATE_TIME = Column(DateTime)
    CREATE_USER = Column(Integer)
    CREATE_USER_NAME = Column(String(50))
    STATUS = Column(String(50))
    STATUS_TIME = Column(DateTime)
    REMARK = Column(Text)
    REGION = Column(String(10))
    KEY_ID = Column(String(32))
    START_TIME = Column(DateTime)
    END_TIME = Column(DateTime)
    DEAL_TIME = Column(DateTime)
    ROLE_ID_STR = Column(String(200))

    fa_flow = relationship(u'FaFlow')


class FaTaskFlow(Base):
    __tablename__ = 'fa_task_flow'

    ID = Column(Integer, primary_key=True)
    PARENT_ID = Column(ForeignKey(u'fa_task_flow.ID'))
    TASK_ID = Column(ForeignKey(u'fa_task.ID'), nullable=False)
    LEVEL_ID = Column(Integer)
    FLOWNODE_ID = Column(Integer)
    EQUAL_ID = Column(Integer)
    IS_HANDLE = Column(Integer, nullable=False)
    NAME = Column(String(100))
    HANDLE_URL = Column(String(200))
    SHOW_URL = Column(String(200))
    EXPIRE_TIME = Column(DateTime)
    START_TIME = Column(DateTime, nullable=False)
    DEAL_STATUS = Column(String(50))
    ROLE_ID_STR = Column(String(200))
    HANDLE_USER_ID = Column(Integer)
    DEAL_TIME = Column(DateTime)
    ACCEPT_TIME = Column(DateTime)

    parent = relationship(u'FaTaskFlow', remote_side=[ID])
    fa_task = relationship(u'FaTask')


class FaTaskFlowHandle(Base):
    __tablename__ = 'fa_task_flow_handle'

    ID = Column(Integer, primary_key=True)
    TASK_FLOW_ID = Column(ForeignKey(u'fa_task_flow.ID'), nullable=False)
    DEAL_USER_ID = Column(Integer, nullable=False)
    DEAL_USER_NAME = Column(String(50), nullable=False)
    DEAL_TIME = Column(DateTime, nullable=False)
    CONTENT = Column(String(2000), nullable=False)

    fa_task_flow = relationship(u'FaTaskFlow')


t_fa_task_flow_handle_files = Table(
    'fa_task_flow_handle_files', metadata,
    Column('FLOW_HANDLE_ID', ForeignKey(u'fa_task_flow_handle.ID'), primary_key=True, nullable=False),
    Column('FILES_ID', ForeignKey(u'fa_files.ID'), primary_key=True, nullable=False)
)


class FaTaskFlowHandleUser(Base):
    __tablename__ = 'fa_task_flow_handle_user'

    TASK_FLOW_ID = Column(ForeignKey(u'fa_task_flow.ID'), primary_key=True, nullable=False)
    HANDLE_USER_ID = Column(Integer, primary_key=True, nullable=False)

    fa_task_flow = relationship(u'FaTaskFlow')


class FaUpdataLog(Base):
    __tablename__ = 'fa_updata_log'

    ID = Column(Integer, primary_key=True)
    CREATE_TIME = Column(DateTime)
    CREATE_USER_NAME = Column(String(50))
    CREATE_USER_ID = Column(Integer)
    OLD_CONTENT = Column(Text)
    NEW_CONTENT = Column(Text)
    TABLE_NAME = Column(String(50))


class FaUser(Base):
    __tablename__ = 'fa_user'

    ID = Column(Integer, primary_key=True)
    NAME = Column(String(80))
    LOGIN_NAME = Column(String(20))
    ICON_FILES_ID = Column(Integer)
    DISTRICT_ID = Column(ForeignKey(u'fa_district.ID'), nullable=False)
    IS_LOCKED = Column(Numeric(1, 0))
    CREATE_TIME = Column(DateTime)
    LOGIN_COUNT = Column(Integer)
    LAST_LOGIN_TIME = Column(DateTime)
    LAST_LOGOUT_TIME = Column(DateTime)
    LAST_ACTIVE_TIME = Column(DateTime)
    REMARK = Column(String(2000))
    REGION = Column(String(10), nullable=False)

    fa_district = relationship(u'FaDistrict')
    fa_user_info = relationship(u'FaUserInfo', secondary='fa_user_friend')


class FaUserInfo(FaUser):
    __tablename__ = 'fa_user_info'

    ID = Column(ForeignKey(u'fa_user.ID'), primary_key=True)
    LEVEL_ID = Column(Integer)
    FAMILY_ID = Column(ForeignKey(u'fa_family.ID'))
    ELDER_ID = Column(ForeignKey(u'fa_elder.ID'))
    LEVEL_NAME = Column(String(2))
    FATHER_ID = Column(ForeignKey(u'fa_user_info.ID'))
    MOTHER_ID = Column(Integer)
    BIRTHDAY_TIME = Column(DateTime)
    BIRTHDAY_PLACE = Column(String(500))
    IS_LIVE = Column(Numeric(1, 0))
    DIED_TIME = Column(DateTime)
    DIED_PLACE = Column(String(500))
    REMARK = Column(String(500))
    SEX = Column(String(2))
    YEARS_TYPE = Column(String(10))
    CONSORT_ID = Column(Integer)
    STATUS = Column(String(10), nullable=False, server_default=text("'??'"))
    CREATE_TIME = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    CREATE_USER_NAME = Column(String(50), nullable=False, server_default=text("'admin'"))
    CREATE_USER_ID = Column(Integer, nullable=False, server_default=text("'1'"))
    UPDATE_TIME = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    UPDATE_USER_NAME = Column(String(50), nullable=False, server_default=text("'admin'"))
    UPDATE_USER_ID = Column(Integer, nullable=False, server_default=text("'1'"))

    fa_elder = relationship(u'FaElder')
    fa_family = relationship(u'FaFamily')
    parent = relationship(u'FaUserInfo', remote_side=[ID])


t_fa_user_district = Table(
    'fa_user_district', metadata,
    Column('USER_ID', ForeignKey(u'fa_user.ID'), primary_key=True, nullable=False),
    Column('DISTRICT_ID', ForeignKey(u'fa_district.ID'), primary_key=True, nullable=False)
)


class FaUserEvent(Base):
    __tablename__ = 'fa_user_event'

    ID = Column(Integer, primary_key=True)
    USER_ID = Column(ForeignKey(u'fa_user_info.ID'))
    NAME = Column(String(50))
    HAPPEN_TIME = Column(DateTime)
    CONTENT = Column(String(500))
    ADDRESS = Column(String(500))

    fa_user_info = relationship(u'FaUserInfo')
    fa_files = relationship(u'FaFile', secondary='fa_event_files')


t_fa_user_friend = Table(
    'fa_user_friend', metadata,
    Column('USER_ID', ForeignKey(u'fa_user_info.ID'), primary_key=True, nullable=False),
    Column('FRIEND_ID', ForeignKey(u'fa_user.ID'), primary_key=True, nullable=False)
)


class FaUserMessage(Base):
    __tablename__ = 'fa_user_message'

    MESSAGE_ID = Column(ForeignKey(u'fa_message.ID'), primary_key=True, nullable=False)
    USER_ID = Column(Integer, primary_key=True, nullable=False)
    PHONE_NO = Column(String(20))
    STATUS = Column(String(10))
    STATUS_TIME = Column(DateTime, nullable=False)
    REPLY = Column(String(500))
    PUSH_TYPE = Column(String(10))

    fa_message = relationship(u'FaMessage')


t_fa_user_module = Table(
    'fa_user_module', metadata,
    Column('USER_ID', ForeignKey(u'fa_user.ID'), primary_key=True, nullable=False),
    Column('MODULE_ID', ForeignKey(u'fa_module.ID'), primary_key=True, nullable=False)
)


t_fa_user_role = Table(
    'fa_user_role', metadata,
    Column('ROLE_ID', ForeignKey(u'fa_role.ID'), primary_key=True, nullable=False),
    Column('USER_ID', ForeignKey(u'fa_user.ID'), primary_key=True, nullable=False)
)


class Sequence(Base):
    __tablename__ = 'sequence'

    seq_name = Column(String(50), primary_key=True)
    current_val = Column(Integer, nullable=False)
    increment_val = Column(Integer, nullable=False, server_default=text("'1'"))
