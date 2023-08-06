"""本模块包含tornado application对象的创建，
   以及WSGI钩子，您也可以直接通过该模块来启动API服务
"""
import os
from acolyte.api import BaseAPIHandler
from acolyte.api.route import URL_MAPPING
from acolyte.core.bootstrap import EasemobFlowBootstrap
from acolyte.util.tornado_base import TornadoApplicationLauncher
from acolyte.util.conf import load_from_py_module


def load_config():
    return load_from_py_module(
        os.environ.get("ACOLYTE_PRO_CONFIG", "config/acolyte_pro_config.py"))


config = load_config()
bootstrap = EasemobFlowBootstrap()
BaseAPIHandler.service_container = bootstrap.service_container

tornado_app_launcher = TornadoApplicationLauncher(
    identity="rest_api",
    config=config,
    route=URL_MAPPING,
    core_bootstrap=bootstrap,
    app_settings=None
)

tornado_app_launcher.start_core()

# 公开wsgi钩子
wsgi_app = tornado_app_launcher.wsgi_application


if __name__ == "__main__":
    tornado_app_launcher.start_application()
