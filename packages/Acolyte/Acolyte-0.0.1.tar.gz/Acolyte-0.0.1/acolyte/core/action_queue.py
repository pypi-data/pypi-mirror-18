import datetime
import simplejson as json
from abc import ABCMeta, abstractmethod
from acolyte.util import db
from acolyte.util.json import to_json


class TaskStatus:

    UNTAKE = "untake"

    TAKEN = "taken"

    ACKED = "acked"

    DROPPED = "dropped"


class Task:

    @classmethod
    def from_args(cls, args):
        return cls(0, TaskStatus.UNTAKE, args)

    def __init__(self, id_, status, args):
        self._id = id_
        self._status = status
        self._args = args

    @property
    def id(self):
        return self._id

    @property
    def status(self):
        return self._status

    @property
    def args(self):
        return self._args


class ActionQueue(metaclass=ABCMeta):

    """Action队列
    """

    def __init__(self, name, init_action, consume_action, ack_action):
        self._name = name
        self._init_action = init_action
        self._consume_action = consume_action
        self._ack_action = ack_action

    @property
    def name(self):
        return self._name

    def init(self, context, *tasks, trigger_consume_action=False):
        """初始化队列
           :param trigger_consume_action: 如果为True，会在初始化之后自动触发
                  consume_action
        """
        self._save_tasks_into_queue(context, *tasks)
        if trigger_consume_action:
            self._execute_action(
                context, self._consume_action, {})

    @abstractmethod
    def _save_tasks_into_queue(self, context, *tasks):
        """批量保存任务到队列
        """
        ...

    def take(self, context):
        """从队列中取出任务
        """
        return self._take_from_queue(context)

    @abstractmethod
    def _take_from_queue(self, context):
        ...

    def ack(self, context, task_id, *,
            trigger_consume_action=False, auto_finish=False):
        """确认任务完毕
           :param trigger_consume_action: 如果为True，并且队列没有全部消费完，
                  会自动触发consume_action
           :param 如果队列全部消费完，是否调用finish方法
        """
        self._mark_task_acked(task_id)

        # 所有消息都被ack
        if self._is_all_acked(context):
            if auto_finish:
                context.finish()
        else:
            if trigger_consume_action:
                self._execute_action(context, self._consume_action, {})

    @abstractmethod
    def _mark_task_acked(self, task_id):
        ...

    @abstractmethod
    def _is_all_acked(self, context):
        ...

    def give_back(self, context, task, *, trigger_consume_action=False):
        """将消息归还给队列
           :param trigger_consume_action: 归还后是否触发consume_action
        """
        self._mark_task_untake(task)
        if trigger_consume_action:
            self._execute_action(context, self._consume_action, {})

    @abstractmethod
    def _mark_task_untake(self, context, task):
        ...

    def drop_task(self, context, task, *, trigger_consume_action=False):
        """将消息丢弃
           :param trigger_consume_action: 丢弃后是否触发consume_action
        """
        self._mark_task_dropped(context, task)
        if trigger_consume_action:
            self._execute_action(context, self._consume_action, {})

    @abstractmethod
    def _mark_task_dropped(self, context, task):
        ...

    @abstractmethod
    def clear(self, context):
        """将整个队列中的任务标记为Dropped状态
        """
        ...

    def _execute_action(self, context, action, args=None):
        if args is None:
            args = {}
        context._flow_executor.handle_job_action(
            flow_instance_id=context.flow_instance_id,
            target_step=context.current_step,
            target_action=action,
            actor=context.actor,
            action_args=args
        )

    # 各种状态数目

    def untake_num(self, context):
        return self._get_num_by_status(context, TaskStatus.UNTAKE)

    def taken_num(self, context):
        return self._get_num_by_status(context, TaskStatus.TAKEN)

    def acked_num(self, context):
        return self._get_num_by_status(context, TaskStatus.ACKED)

    def dropped_num(self, context):
        return self._get_num_by_status(context, TaskStatus.DROPPED)

    @abstractmethod
    def _get_num_by_status(self, context, status):
        ...


class _TaskModel:

    @classmethod
    def from_task_and_ctx(cls, task, queue_name, context):
        return cls(
            id_=task.id,
            flow_instance_id=context.flow_instance_id,
            job_instance_id=context.job_instance_id,
            queue_name=queue_name,
            status=task.status,
            args=task.args
        )

    def __init__(self, id_, flow_instance_id, job_instance_id,
                 queue_name, status, args):
        self.id = id_
        self.flow_instance_id = flow_instance_id
        self.job_instance_id = job_instance_id
        self.queue_name = queue_name
        self.status = status
        self.args = args
        now = datetime.datetime.now()
        self.updated_on = now
        self.created_on = now


def _task_mapper(row):
    return Task(
        id_=row.pop("id"),
        status=row["status"],
        args=json.loads(row["args"])
    )


class MySQLActionQueue(ActionQueue):

    def __init__(self, name, init_action, consume_action, ack_action):
        super().__init__(
            name=name,
            init_action=init_action,
            consume_action=consume_action,
            ack_action=ack_action
        )

    def _save_tasks_into_queue(self, context, *tasks):
        if not tasks:
            return
        tasks = [_TaskModel.from_task_and_ctx(
            t, self.name, context) for t in tasks]
        db.default.executemany(
            "insert into job_action_queue ("
            "flow_instance_id, job_instance_id, queue_name, "
            "status, args, updated_on, created_on) values ("
            "%s, %s, %s, %s, %s, %s, %s);",
            [(
                t.flow_instance_id,
                t.job_instance_id,
                t.queue_name,
                t.status,
                to_json(t.args),
                t.updated_on,
                t.created_on
            ) for t in tasks])

    def _take_from_queue(self, context):
        task = db.default.query_one(
            sql="select id, status, args from "
            "job_action_queue where flow_instance_id = %s "
            "and job_instance_id = %s and queue_name = %s and status = %s "
            "limit 1",
            args=(
                context.flow_instance_id,
                context.job_instance_id,
                self.name,
                TaskStatus.UNTAKE
            ),
            mapper=_task_mapper
        )

        if not task:
            return None

        self._update_task_status(task.id, TaskStatus.TAKEN)
        return task

    def _mark_task_acked(self, task_id):
        self._update_task_status(task_id, TaskStatus.ACKED)

    def _mark_task_untake(self, task):
        self._update_task_status(task.id, TaskStatus.UNTAKE)

    def _mark_task_dropped(self, task):
        self._update_task_status(task.id, TaskStatus.DROPPED)

    def _update_task_status(self, id_, status):
        now = datetime.datetime.now()
        db.default.execute((
            "update job_action_queue set status = %s, "
            "updated_on = %s where id = %s"
        ), (status, now, id_))

    def _is_all_acked(self, context):
        unack_count = db.default.query_one_field(
            sql="select count(*) from job_action_queue "
            "where flow_instance_id = %s and job_instance_id = %s "
            "and queue_name = %s and status != %s limit 1",
            args=(
                context.flow_instance_id,
                context.job_instance_id,
                self.name,
                TaskStatus.ACKED
            )
        )
        return unack_count == 0

    def _get_num_by_status(self, context, status):
        return db.default.query_one_field(
            "select count(*) from job_action_queue "
            "where flow_instance_id = %s and job_instance_id = %s "
            "and queue_name = %s and status = %s",
            args=(
                context.flow_instance_id,
                context.job_instance_id,
                self._name,
                status
            )
        )

    def clear(self, context):
        return db.default.execute((
            "update job_action_queue set status = %s "
            "where flow_instance_id = %s and job_instance_id = %s "
            "and queue_name = %s"
        ), (
            TaskStatus.DROPPED,
            context.flow_instance_id,
            context.job_instance_id,
            self._name
        ))
