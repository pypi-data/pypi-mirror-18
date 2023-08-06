from abc import (
    ABCMeta,
    abstractmethod
)
from typing import Dict, Any
from acolyte.util import db
from acolyte.util import log
from acolyte.util.service_container import ServiceContainer
from acolyte.core.mgr import (
    job_manager,
    flow_meta_manager
)
from acolyte.util.mail import load_smtp_config
from acolyte.core.flow_service import FlowService
from acolyte.core.user_service import UserService
from acolyte.core.job_service import JobService
from acolyte.core.flow_executor_service import FlowExecutorService


class AbstractBootstrap(metaclass=ABCMeta):

    """Bootstrap类用于统一初始化启动应用所需要的组件和服务
    """

    def __init__(self):
        ...

    @abstractmethod
    def start(config):
        ...


class EasemobFlowBootstrap(AbstractBootstrap):

    """正式启动应用所需的Bootstrap
    """

    def __init__(self):
        super().__init__()
        self._service_container = ServiceContainer()

    def start(self, config: Dict[str, Dict[str, Any]]):
        """在这里对各种组件进行初始化
           :param config: 配置数据，字典套字典什么的
        """

        # 初始化日志
        log.load_logger_config(config)
        log.acolyte.info("Starting acolyte ...")

        # 初始化数据库连接池
        self._pool = db.load_db_config(config)

        self._service_binding(self._service_container)

        # 初始化邮箱配置
        load_smtp_config(config)

        log.acolyte.info("Acolyte started .")

    @property
    def service_container(self):
        return self._service_container

    def _service_binding(self, service_container: ServiceContainer):
        """将服务绑定到注册容器
        """

        service_container.register(
            service_id="db",
            service_obj=self._pool
        )

        service_container.register(
            service_id="job_manager",
            service_obj=job_manager,
            init_callback=lambda service_obj: service_obj.load()
        )

        service_container.register(
            service_id="flow_meta_manager",
            service_obj=flow_meta_manager,
            init_callback=lambda service_obj: service_obj.load()
        )

        # 注册各种Service
        service_container.register_service(FlowService)
        service_container.register_service(UserService)
        service_container.register_service(JobService)
        service_container.register_service(FlowExecutorService)

        service_container.after_register()
