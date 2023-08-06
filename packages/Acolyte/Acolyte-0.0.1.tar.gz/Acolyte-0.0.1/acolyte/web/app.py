import os
import jinja2
from tornado_jinja2 import Jinja2Loader
from acolyte.web import BaseWebHandler
from acolyte.web.route import URL_MAPPING
from acolyte.core.bootstrap import EasemobFlowBootstrap
from acolyte.util.tornado_base import TornadoApplicationLauncher
from acolyte.util.conf import load_from_py_module
from acolyte.util.time import (
    is_current_year,
    is_current_month,
    is_current_day,
    current_year,
    simple_fmt_dt,
    get_timedelta_desc
)
from acolyte.util.json import to_json
from acolyte.util.lang import trim_paragraph


def load_config():
    return load_from_py_module(
        os.environ.get("ACOLYTE_PRO_CONFIG", "config/acolyte_pro_config.py"))


config = load_config()
bootstrap = EasemobFlowBootstrap()
BaseWebHandler.service_container = bootstrap.service_container

jinja2_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader('resource/web_templates'),
    autoescape=True
)

jinja2_env.tests['current_year'] = is_current_year
jinja2_env.tests['current_month'] = is_current_month
jinja2_env.tests['current_day'] = is_current_day

jinja2_env.globals['get_current_year'] = current_year
jinja2_env.globals["simple_fmt_dt"] = simple_fmt_dt
jinja2_env.globals["timedelta"] = get_timedelta_desc

jinja2_env.filters["pretty_json"] = lambda obj: to_json(
    obj, ensure_ascii=False)
jinja2_env.filters["trim_paragraph"] = lambda text: trim_paragraph(text)

tornado_app_launcher = TornadoApplicationLauncher(
    identity="web_ui",
    config=config,
    route=URL_MAPPING,
    core_bootstrap=bootstrap,
    app_settings={
        "template_loader": Jinja2Loader(jinja2_env),
        "cookie_secret": "papapa",
        "debug": True,
        "static_path": "resource/web_static",
    }
)

tornado_app_launcher.start_core()

# 公开wsgi钩子
wsgi_app = tornado_app_launcher.wsgi_application


if __name__ == "__main__":
    tornado_app_launcher.start_application()
