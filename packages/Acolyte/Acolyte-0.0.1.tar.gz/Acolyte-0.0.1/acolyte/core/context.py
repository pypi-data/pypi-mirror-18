import collections
from abc import ABCMeta
from acolyte.core.storage.job_action_data import JobActionDataDAO


class AbstractFlowContext(collections.Mapping, metaclass=ABCMeta):

    """上下文对象用于在Flow运行中的Job之间传递数据
    """

    def __init__(self, flow_executor, config):
        super().__init__()
        self._flow_executor = flow_executor
        self._config = config

    @property
    def config(self):
        """用于获取一个template的配置对象
        """
        return self._config

    def init(self):
        ...

    def destroy(self):
        ...

    def failure(self):
        """Job可以在action中随时回调此方法终结flow的执行
        """
        self._flow_executor._failure_whole_flow(self)

    def finish(self, waiting_for=None):
        """Job可以在action中调用此方法来表示自己已经执行完毕
        """
        self._flow_executor._finish_step(self, waiting_for)

    def save(self, data):
        """Job可以通过该方法保存持久化的数据
        """
        ...

    def finish_instance_group(self):
        self._flow_executor._finish_instance_group(self)


class MySQLContext(AbstractFlowContext):

    """基于MySQL的上下文实现
    """

    class _ActionQueueDelegate:

        def __init__(self, context, queue):
            self._context = context
            self._queue = queue

        def init(self, *tasks, trigger_consume_action=False):
            self._queue.init(
                self._context, *tasks,
                trigger_consume_action=trigger_consume_action)

        def take(self):
            return self._queue.take(self._context)

        def ack(self,
                task_id, *, trigger_consume_action=False, auto_finish=False):
            self._queue.ack(self._context, task_id,
                            trigger_consume_action=trigger_consume_action,
                            auto_finish=auto_finish)

        def clear(self):
            self._queue.clear(self._context)

        @property
        def untake_num(self):
            return self._queue.untake_num(self._context)

        @property
        def taken_num(self):
            return self._queue.taken_num(self._context)

        @property
        def acked_num(self):
            return self._queue.acked_num(self._context)

        @property
        def dropped_num(self):
            return self._queue.dropped_num(self._context)

    class _ActionQueueContainer(dict):

        def __init__(self, context, action_queues):
            if action_queues is None:
                action_queues = []
            super().__init__({
                aq.name: MySQLContext._ActionQueueDelegate(context, aq)
                for aq in action_queues})

        def __setattr__(self, name, value):
            self[name] = value

        def __getattr__(self, name):
            return self[name]

    def __init__(self, flow_executor, config, db, flow_instance_id,
                 job_instance_id=None, job_action_id=None, job_action=None,
                 flow_meta=None, current_step=None, actor=0,
                 action_queues=None):
        """
        :param flow_executor: 当前执行flow的executor对象
        :param db: 数据源
        :param flow_instance_id: flow实例ID
        :param job_instance_id: job实例ID
        :param job_action_id: job action ID
        :param job_action: job action名称
        :param flow_meta: flow元信息
        :param current_step: 当前运行到的job step
        """
        super().__init__(flow_executor, config)
        self._db = db
        self._flow_instance_id = flow_instance_id
        self._job_instance_id = job_instance_id
        self._job_action = job_action
        self._job_action_id = job_action_id
        self._flow_meta = flow_meta
        self._current_step = current_step
        self._actor = actor
        self._queue = MySQLContext._ActionQueueContainer(self, action_queues)

    @property
    def flow_instance_id(self):
        return self._flow_instance_id

    @property
    def job_instance_id(self):
        return self._job_instance_id

    @property
    def job_action(self):
        return self._job_action

    @property
    def job_action_id(self):
        return self._job_action_id

    @property
    def flow_meta(self):
        return self._flow_meta

    @property
    def current_step(self):
        return self._current_step

    @property
    def actor(self):
        return self._actor

    @property
    def queue(self):
        return self._queue

    def __getitem__(self, key):
        return self._db.query_one_field((
            "select v from flow_context where "
            "flow_instance_id = %s and k = %s"
        ), (self._flow_instance_id, key))

    def __setitem__(self, key, value):
        self._db.execute((
            "insert into flow_context ("
            "flow_instance_id, k, v) values ("
            "%s, %s, %s) on duplicate key update "
            "v = %s"
        ), (self._flow_instance_id, key, value, value))

    def __delitem__(self, key):
        return self._db.execute((
            "delete from flow_context where "
            "flow_instance_id = %s and k = %s limit 1"
        ), (self._flow_instance_id, key))

    def __len__(self):
        return self._db.query_one_field((
            "select count(*) as c from flow_context where "
            "flow_instance_id = %s"
        ), (self._flow_instance_id,))

    def __iter__(self):
        return self.keys()

    def get(self, key, value=None):
        v = self[key]
        if v is None:
            return value
        return v

    def items(self):
        rs = self._db.query_all((
            "select k, v from flow_context where "
            "flow_instance_id = %s"
        ), (self._flow_instance_id,))
        return [(row["k"], row["v"]) for row in rs]

    def keys(self):
        rs = self._db.query_all((
            "select k from flow_context where "
            "flow_instance_id = %s"
        ), (self._flow_instance_id,))
        return [row['k'] for row in rs]

    def values(self):
        rs = self._db.query_all((
            "select v from flow_context where "
            "flow_instance_id = %s"
        ), (self._flow_instance_id,))
        return [row['v'] for row in rs]

    def destroy(self):
        self._db.execute((
            "delete from flow_context where "
            "flow_instance_id = %s"
        ), (self._flow_instance_id,))

    def save(self, data):
        action_dao = JobActionDataDAO(self._db)
        action_dao.update_data(self._job_action_id, data)

    def save_with_key(self, data_key, data):
        action_dao = JobActionDataDAO(self._db)
        action_dao.update_data_with_key(self._job_action_id, data_key, data)
