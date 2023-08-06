from acolyte.core.job import (
    AbstractJob,
    ActionArg,
    action_args,
    action_constraint,
    ActionLockType,
    ActionLock,
    ActionRunTimes,
)
from acolyte.core.service import Result
from acolyte.util.validate import IntField, StrField
from acolyte.core.action_queue import (
    MySQLActionQueue,
    Task
)


class EchoJob(AbstractJob):

    """该Job用于测试，打印事件和参数，并返回接收到的参数
    """

    def __init__(self):
        super().__init__(
            "echo",
            "test job echo",
            action_queues=[
                MySQLActionQueue(
                    "test", "queue_init", "consume", "ack"),
            ]
        )
        self._test_barrier = ("a", "b", "c")

    @action_args(
        ActionArg(IntField("a", required=True), ActionArg.MARK_CONST, "a的值"),
        ActionArg(IntField("b", required=True), ActionArg.MARK_STATIC, "b的值"),
    )
    def on_trigger(self, context, a, b):
        print("I received args: a={a}, b={b}".format(
            a=a,
            b=b
        ))
        r = a + b
        context["add_result"] = r
        return Result.ok(data=r)

    @action_args(
        ActionArg(IntField("c", required=True), ActionArg.MARK_AUTO, "c的值")
    )
    def on_multiply(self, context, c):
        print("I received args: c={c}".format(c=c))
        r = int(context["add_result"]) * c
        context["multiply_result"] = r
        return Result.ok(data=r)

    @action_args(
        ActionArg(IntField("d", required=True), ActionArg.MARK_AUTO, "d的值"),
        ActionArg(IntField("e", required=True), ActionArg.MARK_AUTO, "e的值")
    )
    def on_minus(self, context, d, e):
        print("I received args: d={d}, e={e}".format(d=d, e=e))
        r = int(context["multiply_result"]) - d - e
        context.finish()
        return Result.ok(data=r)

    @action_args(
        ActionArg(IntField("sleep_time", required=True),
                  ActionArg.MARK_AUTO, "sleep time"),
    )
    def on_pass(self, context):
        ...

    def on_a(self, context):
        context.finish(waiting_for=self._test_barrier)

    def on_b(self, context):
        context.finish(waiting_for=self._test_barrier)

    def on_c(self, context):
        context.finish(waiting_for=self._test_barrier)

    @action_constraint(
        lock=ActionLock("repeat_action", ActionLockType.USER_EXCLUSIVE_LOCK),
        run_times=ActionRunTimes.NO_LIMIT
    )
    def on_repeat(self, context):
        context.save({"a": 1})

    def on_queue_init(self, context):
        tasks = [Task.from_args({"count": i}) for i in range(5)]
        context.queue.test.init(*tasks, trigger_consume_action=True)

    @action_constraint(
        lock=None,
        run_times=ActionRunTimes.NO_LIMIT
    )
    def on_consume(self, context):
        task = context.queue.test.take()
        if task:
            print(task.args)

    @action_args(
        ActionArg(
            IntField("task_id", required=True),
            mark=ActionArg.MARK_AUTO,
            comment="任务ID"
        ),
    )
    @action_constraint(
        lock=None,
        run_times=ActionRunTimes.NO_LIMIT
    )
    def on_ack(self, context, task_id):
        context.queue.test.ack(task_id, trigger_consume_action=True,
                               auto_finish=True)


class OldManJob(AbstractJob):

    """Mock Job 长者Job
    """

    def __init__(self):
        super().__init__("old_man", "old man job")

    def on_trigger(self, context):
        print("old man job on trigger")
        return Result.ok(data="跑的比谁都快")

    @action_args(
        ActionArg(
            StrField("question", required=True), ActionArg.MARK_AUTO, "向长者提问")
    )
    def on_question(self, context, question):
        if question == "董先森连任好不好啊":
            context.finish()
            return Result.ok(data="吼啊")
        else:
            return Result.bad_request("old_man_angry", msg="无可奉告")

    def on_angry(self, context):
        print("I'm angry! 你们这样子是不行的！我要终止整个flow！")
        context.failure()
        return Result.bad_request("old_man_angry", msg="I'm angry!")


def letter_job_meta(letter):

    class LetterJobMeta(type):

        def __new__(cls, name, bases, attrs):

            def _make_method(action):
                @action_args(
                    ActionArg(
                        IntField("x", required=True),
                        ActionArg.MARK_AUTO, "arg x"),
                    ActionArg(
                        IntField("y", required=True),
                        ActionArg.MARK_AUTO, "arg y")
                )
                def method(self, context, x, y):
                    context.finish()
                    return Result.ok(data=(x + y))
                return method

            attrs["on_trigger"] = _make_method("trigger")
            attrs["__init__"] = lambda self: AbstractJob.__init__(
                self, "job_" + letter, "job " + letter)

            bases += (AbstractJob,)

            return type(name, bases, attrs)

    return LetterJobMeta


class AJob(metaclass=letter_job_meta("A")):
    ...


class BJob(metaclass=letter_job_meta("B")):
    ...


class CJob(metaclass=letter_job_meta("C")):
    ...


class DJob(metaclass=letter_job_meta("D")):
    ...
