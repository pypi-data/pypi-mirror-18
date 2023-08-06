import inspect
import pkg_resources
from abc import ABCMeta, abstractmethod
from acolyte.exception import (
    UnsupportOperationException,
    ObjectAlreadyExistedException,
    ObjectNotFoundException,
    InvalidArgumentException
)
from acolyte.core.job import (
    ActionConstraint,
    ActionLock,
    ActionLockType,
    ActionRunTimes,
)


class AbstractManager(metaclass=ABCMeta):

    def __init__(self):
        ...

    @abstractmethod
    def load(self):
        """加载所有对象到容器
        """
        ...

    @abstractmethod
    def register(self, name, obj):
        """注册对象到容器
        """
        ...

    @abstractmethod
    def get(self, name):
        """从容器中获取元素
        """
        ...

    @abstractmethod
    def all(self):
        """获取容器中的所有元素信息
        """
        ...


class ManagerChain(AbstractManager):

    def __init__(self, *mgr_list):
        self._mgr_list = mgr_list

    def load(self):
        map(lambda mgr: mgr.load(), self._mgr_list)

    def register(self, name: str, obj: object):
        raise UnsupportOperationException.build(ManagerChain, "register")

    def get(self, name: str) -> object:
        for mgr in self._mgr_list:
            try:
                return mgr.get(name)
            except ObjectNotFoundException:
                continue
            else:
                raise ObjectNotFoundException(name)

    def all(self):
        result = []
        for mgr in self._mgr_list:
            result += mgr.all()
        return result


class DictBasedManager(AbstractManager):

    def __init__(self):
        super().__init__()
        self._container = {}

    def load(self):
        raise UnsupportOperationException.build(DictBasedManager, "load")

    def register(self, name, obj):
        if name in self._container:
            raise ObjectAlreadyExistedException(name)
        self._container[name] = self._handle_obj(obj)

    def get(self, name):
        try:
            return self._container[name]
        except KeyError:
            raise ObjectNotFoundException(name)

    def all(self):
        return self._container.values()

    def _handle_obj(self, obj):
        """子类可以实现该方法对加载的对象做更多的处理
        """
        return obj


class EntryPointManager(DictBasedManager):

    def __init__(self, entry_point: str):
        super().__init__()
        self._entry_point = entry_point
        self._container = {}

    def load(self):
        for ep in pkg_resources.iter_entry_points(self._entry_point):
            obj = ep.load()()
            self._container[obj.name] = self._handle_obj(obj)


class JobManager(EntryPointManager):

    def __init__(self, entry_point: str):
        super().__init__(entry_point)

    def _handle_obj(self, obj):
        for mtd_name, mtd in inspect.getmembers(obj, inspect.ismethod):
            if mtd_name.startswith("on_"):
                action_name = mtd_name[len("on_"):]

                # 处理action_args
                action_args = getattr(mtd, "_action_args", tuple())
                obj.job_args[action_name] = action_args

                # 添加默认执行约束 包括:
                # 1. 用户互斥锁
                # 2. 运行次数为1
                # 3. 需要检查data_key
                action_constraint = getattr(mtd, "_action_constraint", None)
                if action_constraint is None:

                    # 默认为用户级的互斥锁
                    lock_key = "{job_name}_{action_name}".format(
                        job_name=obj.name, action_name=action_name)
                    action_lock = ActionLock(
                        lock_key=lock_key,
                        lock_type=ActionLockType.USER_EXCLUSIVE_LOCK
                    )

                    obj.action_constraints[action_name] = \
                        ActionConstraint(lock=action_lock,
                                         run_times=ActionRunTimes.ONCE)
                else:
                    if (
                        action_name == "trigger" and
                        action_constraint.run_times != ActionRunTimes.ONCE
                    ):
                        # 如果action是trigger，那么run_times只能为once
                        raise InvalidArgumentException((
                            "The trigger action of job '{job_name}' "
                            "only allow run_times = ActionRunTimes.ONCE"
                        ).format(job_name=obj.name))
        return obj


# managers for job, flow_meta, notify
job_manager = JobManager("acolyte.job")
flow_meta_manager = EntryPointManager("acolyte.flow_meta")
notify_template_manager = EntryPointManager("acolyte.notify_template")
