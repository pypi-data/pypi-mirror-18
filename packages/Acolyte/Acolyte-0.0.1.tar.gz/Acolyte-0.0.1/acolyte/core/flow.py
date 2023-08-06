import datetime
from typing import List, Dict, Any
from abc import ABCMeta
from acolyte.core.job import JobRef


class FlowMeta(metaclass=ABCMeta):

    """flow meta
       每个流程都可以抽象成flow meta，比如工程更新、SQL审核、机器审核等等
    """

    def __init__(self, name: str, jobs: List[JobRef],
                 start_args: Dict[str, Any]=None,
                 failure_args: Dict[str, Any]=None,
                 description: str=""):
        """
        :param name: flow meta名称
        :param jobs: 包含的JobRef对象列表
        :param bind_args: 绑定的静态参数，格式 {start: {args}, stop: {args}}
        """
        self._name = name
        self._jobs = jobs
        self._start_args = start_args
        self._failure_args = failure_args
        self._description = description
        self._job_ref_map = {job_ref.step_name: job_ref for job_ref in jobs}

    @property
    def name(self):
        return self._name

    @property
    def jobs(self):
        return self._jobs

    @property
    def start_args(self):
        if self._start_args is None:
            return {}
        return self._start_args

    @property
    def failure_args(self):
        if self._failure_args is None:
            return {}
        return self._failure_args

    @property
    def description(self):
        return self._description

    def on_start(self, context, arguments):
        """当Flow启动时，执行此逻辑
           :param context: flow执行上下文
           :param arguments: 生成的运行时参数
        """
        ...

    def on_failure(self, context, arguments):
        """当Flow被终止时，执行此逻辑
           :param context: flow执行上下文
           :param arguments: 生成的运行时参数
        """
        ...

    def on_finish(self, context):
        """当flow结束是，执行此逻辑
           :param context: flow执行上下文
        """
        ...

    def on_discard(self, context):
        """当flow instance被废弃的时候，回调此逻辑
        """
        ...

    def get_next_step(self, current_step):
        """根据当前步骤获取下一个执行步骤
        """

        # 当前step为start的情况
        if current_step == "start":
            if self._jobs:
                return self._jobs[0]
            else:
                return "finish"

        for idx, job_ref in enumerate(self._jobs):
            if job_ref.step_name == current_step:
                if idx < len(self._jobs) - 1:
                    return self._jobs[idx + 1]
                else:
                    return "finish"

    def get_job_ref_by_step_name(self, step_name):
        return self._job_ref_map.get(step_name, None)


class FlowTemplate:

    def __init__(self, id_: int, flow_meta: str, name: str,
                 bind_args: Dict[str, Any], max_run_instance: int,
                 config: Dict[str, Any], creator: int,
                 created_on: datetime.datetime):
        """根据FlowMeta来生成的Flow模板
           :param flow_meta: 使用的flow_meta
           :param name: 模板名称
           :param bind_args: 绑定的参数
           :param max_run_instance: 最大可运行实例数目
           :param config: 配置数据，该数据可以在上下文当中被引用
           :param creator: 创建者
           :param created_on: 创建时间
        """
        self.id = id_
        self.flow_meta = flow_meta
        self.name = name
        self.bind_args = bind_args
        self.max_run_instance = max_run_instance
        self.config = config
        self.creator = creator
        self.created_on = created_on


class FlowStatus:

    """flow的当前运行状态
    """

    STATUS_WAITING = "waiting"  # 等待执行

    STATUS_INIT = "init"  # 初始化，正在运行on_start

    STATUS_RUNNING = "running"  # 正在执行

    STATUS_FINISHED = "finished"  # 已经完成

    STATUS_FAILURE = "failure"  # 已经失败

    STATUS_EXCEPTION = "exception"  # 由于异常而终止

    STATUS_DISCARD = "discard"  # 废弃


class FlowInstance:

    """描述flow template的运行实例
    """

    def __init__(self, id_: int, flow_template_id: int, initiator: int,
                 current_step: str, status, description, created_on,
                 updated_on):
        """
        :param id_: 每个flow运行实例都会有一个唯一ID
        :param flow_template_id: 所属的flow_template
        :param initiator: 发起人
        :param current_step: 当前执行到的步骤
        :param status: 执行状态
        :param created_on: 创建时间
        :param updated_on: 最新更新步骤时间
        """

        self.id = id_
        self.flow_template_id = flow_template_id
        self.initiator = initiator
        self.current_step = current_step
        self.status = status
        self.description = description
        self.created_on = created_on
        self.updated_on = updated_on


class FlowDiscardReason:

    """Flow instance的废弃原因
    """

    def __init__(self, flow_instance_id, actor, reason, discard_time):
        """
        :param flow_instance_id: flow instance id
        :param actor: 执行人
        :param reason: 废弃原因
        :param discard_time: 废弃时间
        """

        self.flow_instance_id = flow_instance_id
        self._actor = actor
        self.reason = reason
        self.discard_time = discard_time


class FlowInstanceGroupStatus:

    STATUS_RUNNING = "running"

    STATUS_FINISHED = "finished"


class FlowInstanceGroup:

    """用于标记一组逻辑上有关联的FlowInstance
    """

    def __init__(self,
                 id_, name, description, meta,
                 status, created_on, updated_on):
        """
        :param id_: 编号
        :param name: 名称
        :param description: 描述
        :param meta: 元数据
        :param status: 状态
        :param created_on: 创建时间
        :param updated_on: 状态更新时间
        """
        self.id = id_
        self.name = name
        self.description = description
        self.meta = meta
        self.status = status
        self.created_on = created_on
        self.updated_on = updated_on
