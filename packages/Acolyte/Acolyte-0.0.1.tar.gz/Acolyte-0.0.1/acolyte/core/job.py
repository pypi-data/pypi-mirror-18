import datetime
from typing import (
    Dict,
    Any
)
from abc import (
    ABCMeta,
    abstractmethod
)
from functools import wraps
from acolyte.util.validate import Field


class AbstractJob(metaclass=ABCMeta):

    """描述一个Job
       实现的其它Job均需要继承该类
    """

    def __init__(self, name: str, description: str, *,
                 ui=None, decisions=None, auto_trigger=False,
                 action_queues=None):
        """
        :param name: Job名称
        :param description: Job描述
        :param job_args: Job参数声明
        :param ui: 自定义终端页UI的相关信息
        :param decisions: 相关的决策页面
        :param auto_trigger: 是否为自动触发
        :param action_queues: action队列
        """
        self._name = name
        self._description = description
        self._job_args = {}
        self._action_constraints = {}
        self._ui = ui
        if decisions is None:
            decisions = []
        self._decisions = decisions
        self._decisions_dict = {
            decision.name: decision for decision in decisions}
        self._auto_trigger = auto_trigger
        if action_queues is None:
            self._action_queues = []
        else:
            self._action_queues = action_queues

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description

    @property
    def job_args(self):
        return self._job_args

    @property
    def action_constraints(self):
        return self._action_constraints

    @property
    def ui(self):
        return self._ui

    @property
    def decisions(self):
        return self._decisions

    @property
    def auto_trigger(self):
        return self._auto_trigger

    @property
    def action_queues(self):
        return self._action_queues

    def get_decision(self, decision_name):
        """根据名称获取指定的Decision对象
        """
        return self._decisions_dict.get(decision_name, None)

    @abstractmethod
    def on_trigger(self, context, arguments):
        """当工作单元被触发时执行此动作
        """
        ...


class DetailsPageUI(metaclass=ABCMeta):

    """用于描述Job的自定义UI组件
    """

    def __init__(self):
        ...

    @abstractmethod
    def render_instance_details_page(self, **data):
        """渲染JobInstance详情页
        :param data: 渲染数据
        """
        ...


class Jinja2DetailsPageUI(DetailsPageUI):

    """基于Jinja2的UI自定义渲染组件
    """

    def __init__(self, env, tpl):
        """
        :param env: Jinja2 Environment对象
        :param tpl: 引用的模板名称
        """
        self._env = env
        self._tpl = tpl

    def render_instance_details_page(self, **data):
        tpl = self._env.get_template(self._tpl)
        return tpl.render(**data)


class Decision:

    """一个Decision表示一个决策页面，用户通过在DecisionUI进行表决来
       触发对应的action
    """

    def __init__(self, name, title, prompt, *options):
        """
        :param name: Decision名称，用来在各处引用
        :param title: 该Decision的简要文字说明，比如“反馈沙箱部署结果”
        :param prompt: 展示在页面的提示说明
        :param options: Decision的具体选项
        """
        self._name = name
        self._title = title
        self._prompt = prompt
        self._options = options

    @property
    def name(self):
        return self._name

    @property
    def title(self):
        return self._title

    @property
    def prompt(self):
        return self._prompt

    @property
    def options(self):
        return self._options


class DecisionOption:

    """Decision中所包含的决策选项
    """

    def __init__(self, action, label):
        """
        :param action: 该Option执行会触发的Action
        :param label: 该Option在页面的简要说明
        """
        self._action = action
        self._label = label

    @property
    def action(self):
        return self._action

    @property
    def label(self):
        return self._label


class JobStatus:

    """Job实例的各种运行状态
    """

    STATUS_WAITING = "waiting"

    STATUS_RUNNING = "running"

    STATUS_FINISHED = "finished"

    STATUS_FAILURE = "failure"

    STATUS_EXCEPTION = "exception"


class JobInstance:

    """描述一个Job的运行状态
    """

    def __init__(self, id_: int, flow_instance_id: int, step_name: str,
                 job_name: str, status: str, trigger_actor: int,
                 created_on, updated_on):
        """
        :param id_: 每个Job的运行实例有一个编号
        :param flow_instance_id: 隶属的flow_instance
        :param step_name: step名称
        :param job_name: job名称
        :param status: 运行状态
        :param trigger_actor: 触发者
        :param created_on: 运行实例起始时间
        :param updated_on: 最近更新状态时间
        """
        self.id = id_
        self.flow_instance_id = flow_instance_id
        self.step_name = step_name
        self.job_name = job_name
        self.status = status
        self.trigger_actor = trigger_actor
        self.created_on = created_on
        self.updated_on = updated_on


class JobActionData:

    """记录Job每一个Action执行的数据
    """

    def __init__(self,
                 id_: int, job_instance_id: int,
                 action: str, actor: int,
                 arguments: Dict[str, Any],
                 data_key: str,
                 data: Dict[str, Any],
                 created_on: datetime.datetime,
                 updated_on: datetime.datetime):
        """
        :param id_: Action实例编号
        :param job_instance_id: 隶属的job instance
        :param action: 动作名称
        :param actor: 执行者
        :param arguments: 执行该Action时所使用的参数
        :param data_key: 用于标记本次action的执行
        :param data: 该Action执行后回填的数据
        :param created_on: 执行时间
        :param finished_on: 执行结束时间
        """

        self.id = id_
        self.job_instance_id = job_instance_id
        self.action = action
        self.actor = actor
        self.arguments = arguments
        self.data_key = data_key
        self.data = data
        self.created_on = created_on
        self.updated_on = updated_on


class JobRef:

    """还对象用于在FlowMeta等声明中引用一个Job
    """

    def __init__(
            self, step_name: str, job_name: str = None, **bind_args):
        """
        :param step_name: 不能叫'start'或者'finish'，这俩是保留字
        """
        self._step_name = step_name
        self._job_name = job_name if job_name is not None else step_name
        self._bind_args = bind_args if bind_args is not None else {}

    @property
    def step_name(self):
        return self._step_name

    @property
    def job_name(self):
        return self._job_name

    @property
    def bind_args(self):
        return self._bind_args


class ActionArg:

    """参数声明
    """

    # 参数类型

    MARK_AUTO = "auto"  # 自动变量，绑定参数值可以被运行时参数值所覆盖

    MARK_CONST = "const"  # const类型的参数的值自FlowMeta指定后就不在变了

    MARK_STATIC = "static"  # static类型的参数值自FlowInstance指定后就不再变了

    def __init__(self, field_info: Field, mark: str, comment: str):
        """
        :param step_name: 当前步骤名称
        :param job_name: 引用的job名称
        :param field_info: 字段类型以及验证属性
        :param mark: 字段标记 auto、const、static
        :param comment: 说明
        """
        self._name = field_info.name
        self._field_info = field_info
        self._mark = mark
        self._comment = comment

    @property
    def name(self):
        return self._name

    @property
    def field_info(self):
        return self._field_info

    @property
    def mark(self):
        return self._mark

    @property
    def comment(self):
        return self._comment


def action_args(*action_args):

    def _job_args(f):

        f._action_args = action_args

        @wraps(f)
        def _f(*args, **kwds):
            return f(*args, **kwds)

        return _f

    return _job_args


class ActionLockType:

    # 用户独占锁，同一时刻只允许一个用户执行
    USER_EXCLUSIVE_LOCK = "user_exclusive_lock"


class ActionLock:

    """用于描述Action上加锁的信息
    """

    def __init__(self, lock_key, lock_type, wait_time=0):
        """
        :param lock_key: 用于标识该锁的字符串
        :param lock_type: 锁类型
        :param wait_time: 等待获取锁的时间，单位是秒，0为立即返回，
                          -1永不超时
        """
        self._lock_key = lock_key
        self._lock_type = lock_type
        self._wait_time = wait_time

    @property
    def lock_key(self):
        return self._lock_key

    @property
    def lock_type(self):
        return self._lock_type

    @property
    def wait_time(self):
        return self._wait_time

    def gen_lock_key(self, value):
        return "{lock_key}_{value}".format(
            lock_key=self.lock_key, value=value)


class ActionRunTimes:

    ONCE = 1  # 只能运行一次

    NO_LIMIT = 0  # 无限制


class ActionConstraint:

    """描述Action执行的约束
    """

    def __init__(self, *, lock=None, run_times=ActionRunTimes.ONCE):
        """
        :param lock: Action执行所需要的锁
        :param run_times: 运行次数
        """
        self._lock = lock
        self._run_times = run_times

    @property
    def lock(self):
        return self._lock

    @property
    def run_times(self):
        return self._run_times


def action_constraint(*, lock, run_times):
    """使用该注解为action添加约束
       :param lock: Action执行的锁定类型
       :param run_times: Action可运行的次数
    """

    def _action_constraint(f):

        f._action_constraint = ActionConstraint(
            lock=lock,
            run_times=run_times
        )

        @wraps(f)
        def _f(*args, **kwds):
            return f(*args, **kwds)

        return _f

    return _action_constraint
