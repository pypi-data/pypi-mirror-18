"""本模块包含了mock相关的工具
"""

from acolyte.testing import test_container
from acolyte.util.json import to_json


def mock_login(account, password):
    """模拟登录操作
    """
    user_service = test_container.get_service("UserService")
    return user_service.login(account, password)


def get_token(account, password):
    """登录并获取token
    """
    login_rs = mock_login(account, password)
    if not login_rs.is_success():
        raise Exception("Login error, result is: {}".format(to_json(login_rs)))
    return login_rs.data["token"]
