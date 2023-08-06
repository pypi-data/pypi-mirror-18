from acolyte.web.user import (
    UserLoginHandler,
    LogoutHandler,
    SettingsHandler,
    ModifyPasswordHandler,
    ProfileHandler
)
from acolyte.web.flow import (
    FlowMetaHandler,
    CreateTemplateHandler,
    ViewTemplateHandler,
    ModifyTemplateHandler,
    ViewFlowInstanceHandler,
    DiscardFlowInstanceHandler,
    ViewFlowGroupDetailsHandler
)
from acolyte.web.job import (
    ViewJobDetailsHandler,
    ViewJobInstanceDetailsHandler,
    JobDecisionHandler
)
from acolyte.web.index import (
    IndexHandler,
    QueryFlowInstanceHandler
)

URL_MAPPING = [

    # 用户相关
    ("/", IndexHandler),
    ("/login", UserLoginHandler),
    ("/logout", LogoutHandler),
    ("/settings", SettingsHandler),
    ("/settings/modify_password", ModifyPasswordHandler),
    ("/profile", ProfileHandler),

    # Index
    ("/index", IndexHandler),
    ("/flow/query_instance_by_date_scope", QueryFlowInstanceHandler),

    # Flow 相关
    (r"/flow/meta/([\w_]+)", FlowMetaHandler),
    ("/flow/template/create", CreateTemplateHandler),
    ("/flow/template/modify", ModifyTemplateHandler),
    (r"/flow/template/(\d+)", ViewTemplateHandler),
    (r"/flow/instance/(\d+)", ViewFlowInstanceHandler),
    (r"/flow/instance/discard", DiscardFlowInstanceHandler),
    (r"/flow/group/(\d+)", ViewFlowGroupDetailsHandler),

    # Job相关
    (r"/job/([\w_\.]+)", ViewJobDetailsHandler),
    (r"/job/instance/(\d+)/decision/(.*)", JobDecisionHandler),
    (r"/job/instance/(\d+)", ViewJobInstanceDetailsHandler),
    (r"/job/instance/(\d+)/(.*)", ViewJobInstanceDetailsHandler),

]
