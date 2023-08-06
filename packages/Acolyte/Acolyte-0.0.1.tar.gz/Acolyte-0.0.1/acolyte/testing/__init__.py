import os
import atexit
import fixtures
from concurrent.futures import ThreadPoolExecutor
from acolyte.util.service_container import ServiceContainer
from acolyte.core.bootstrap import AbstractBootstrap
from acolyte.testing.core.mgr_define import (
    flow_meta_mgr,
    job_mgr,
    notify_tpl_mgr
)
from acolyte.util import db
from acolyte.util import log
from acolyte.util.json import to_json
from acolyte.core.service import Result
from acolyte.core.flow_service import FlowService
from acolyte.core.user_service import UserService
from acolyte.core.job_service import JobService
from acolyte.core.flow_executor_service import FlowExecutorService
from acolyte.core.notify_logic import NotifyLogic
from acolyte.core.storage.flow_template import FlowTemplateDAO
from acolyte.core.storage.flow_instance import FlowInstanceDAO
from acolyte.core.storage.job_instance import JobInstanceDAO
from acolyte.core.storage.job_action_data import JobActionDataDAO
from acolyte.core.context import AbstractFlowContext
from acolyte.util.conf import load_from_py_module
from acolyte.util.mail import load_smtp_config


class UnitTestBootstrap(AbstractBootstrap):

    def __init__(self):
        super().__init__()

    def start(self, config):
        log.load_logger_config(config)
        self.service_container = ServiceContainer()
        atexit.register(self.service_container.finalize)
        load_smtp_config(config)
        self._binding(config, self.service_container)

    def _binding(self, config, service_container):

        db_pool = db.load_db_config(config)
        service_container.register(
            service_id="db",
            service_obj=db_pool,
            finalize=lambda: db_pool.close_all()
        )

        service_container.register(
            service_id="job_manager",
            service_obj=job_mgr
        )

        service_container.register(
            service_id="flow_meta_manager",
            service_obj=flow_meta_mgr
        )

        service_container.register(
            service_id="notify_tpl_manager",
            service_obj=notify_tpl_mgr
        )

        notify_executor = ThreadPoolExecutor(10)
        service_container.register(
            service_id="notify_executor",
            service_obj=notify_executor,
            finalize=lambda: notify_executor.shutdown()
        )

        service_container.register_service(FlowService)
        service_container.register_service(UserService)
        service_container.register_service(JobService)
        service_container.register_service(FlowExecutorService)
        service_container.register_service(NotifyLogic)

        service_container.after_register()


def load_config():
    return load_from_py_module(
        os.environ.get(
            "ACOLYTE_TEST_CONFIG", "config/acolyte_test_config.py"))


_test_bootstrap = UnitTestBootstrap()
_test_bootstrap.start(load_config())
test_container = _test_bootstrap.service_container


class EasemobFlowTestCase(fixtures.TestWithFixtures):

    def _(self, service_id):
        """从容器中获取服务
        """
        global test_container
        self._test_container = test_container
        return test_container.get_service(service_id)

    def print_json(self, obj):
        print(to_json(obj, indent=4 * ' '))

    def assertResultSuccess(self, result):
        self.assertEqual(result.status_code, Result.STATUS_SUCCESS)

    def assertResultBadRequest(self, result, reason):
        self.assertEqual(result.status_code, Result.STATUS_BADREQUEST)
        self.assertEqual(result.reason, reason)


class FlowTemplateFixture(fixtures.Fixture):

    """该fixture可以用来创建和销毁FlowTemplate对象
    """

    def __init__(self, flow_meta_name, tpl_name, bind_args, max_run_instance,
                 config, creator, service_container):
        self._flow_meta_name = flow_meta_name
        self._tpl_name = tpl_name
        self._bind_args = bind_args
        self._max_run_instance = max_run_instance
        self._config = config
        self._creator = creator
        self._flow_service = service_container.get("FlowService")
        self._flow_tpl_dao = FlowTemplateDAO(service_container.get("db"))

    @property
    def flow_template(self):
        return self._flow_template

    def setUp(self):
        self._flow_template = self._flow_service.create_flow_template(
            flow_meta_name=self._flow_meta_name,
            name=self._tpl_name,
            bind_args=self._bind_args,
            max_run_instance=self._max_run_instance,
            config=self._config,
            creator=self._creator
        ).data

    def cleanUp(self):
        self._flow_tpl_dao.delete_by_id(self._flow_template.id)


class FlowInstanceFixture(fixtures.Fixture):

    """该fixture可以用来创建和销毁FlowInstance
    """

    def __init__(self, tpl_id, initiator, description,
                 start_flow_args, service_container):
        self._tpl_id = tpl_id
        self._initiator = initiator
        self._description = description
        self._start_flow_args = start_flow_args
        self._flow_executor_service = service_container.get(
            "FlowExecutorService")

        _db = service_container.get("db")
        self._flow_instance_dao = FlowInstanceDAO(_db)
        self._job_instance_dao = JobInstanceDAO(_db)
        self._job_action_data_dao = JobActionDataDAO(_db)

    @property
    def flow_instance(self):
        return self._flow_instance

    def setUp(self):
        self._flow_instance = self._flow_executor_service.start_flow(
            flow_template_id=self._tpl_id,
            initiator=self._initiator,
            description=self._description,
            start_flow_args=self._start_flow_args
        ).data

    def cleanUp(self):
        # 清理创建的flow_instance
        self._flow_instance_dao.delete_by_instance_id(
            self._flow_instance.id)

        job_instance_lst = self._job_instance_dao.\
            query_by_flow_instance_id(self._flow_instance.id)

        # 删除整个flow instance下的job instance
        self._job_instance_dao.delete_by_flow_instance_id(
            self._flow_instance.id)

        # 删除各个job action dat
        for job_instance in job_instance_lst:
            self._job_action_data_dao.delete_by_job_instance_id(
                job_instance.id)


class MockContext(AbstractFlowContext):

    def __init__(self, executor, config, flow_instance_id, job_instance_id,
                 job_action_id, current_step):
        super().__init__(executor, config)

        self._flow_instance_id = flow_instance_id
        self._job_instance_id = job_instance_id
        self._job_action_id = job_action_id
        self._current_step = current_step

        self._saved_data = {
            flow_instance_id: {
                job_instance_id: {

                }
            }
        }

        self._context_data = {}

    @property
    def context_data(self):
        return self._context_data

    @property
    def saved_data(self):
        return self._saved_data

    def failure(self):
        ...

    def finish(self):
        ...

    def __getitem__(self, key):
        return self._context_data[key]

    def __setitem__(self, key, value):
        self._context_data[key] = value

    def __delitem__(self, key):
        del self._context_data[key]

    def __len__(self):
        return len(self._context_data)

    def __iter__(self):
        return self._context_data.keys()

    def get(self, key, default):
        return self._context_data.get(key, default)

    def items(self):
        return self._context_data.items()

    def keys(self):
        return self._context_data.keys()

    def values(self):
        return self._context_data.values()

    def save(self, data):
        self._saved_data[self._flow_instance_id][
            self._job_instance_id][self._job_action_id] = data
