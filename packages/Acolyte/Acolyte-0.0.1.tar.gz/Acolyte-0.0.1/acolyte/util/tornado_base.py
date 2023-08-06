"""对tornado通用配置的一点微小的封装
"""
import tornado.wsgi
import tornado.ioloop
from tornado.web import Application


class TornadoApplicationLauncher:

    def __init__(self, identity, config, route,
                 core_bootstrap, app_settings=None):
        """
        :param identity: 服务身份，web_ui或者是rest_api
        :param config: 完成的配置数据
        :param routes: 路由
        :param core_bootstrap: 启动服务所需要的bootstrap对象
        :param app_settings: Tornado Application对象设置
        """

        if app_settings is None:
            app_settings = {}

        self._identity = identity
        self._config = config
        self._route = route
        self._core_bootstrap = core_bootstrap
        self._application = Application(self._route, **app_settings)
        self._wsgi_application = tornado.wsgi.WSGIAdapter(self._application)

    @property
    def tornado_application(self):
        return self._application

    @property
    def wsgi_application(self):
        return self._wsgi_application

    def start_core(self):
        """启动核心逻辑"""
        self._core_bootstrap.start(self._config)

    def start_application(self):
        """启动Tornado应用"""
        self._application.listen(self._config[self._identity]["port"])
        tornado.ioloop.IOLoop.current().start()
