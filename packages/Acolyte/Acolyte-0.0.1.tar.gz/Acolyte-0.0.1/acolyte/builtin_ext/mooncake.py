"""抢月饼，你懂的
"""

from acolyte.core.job import (
    AbstractJob,
    ActionArg,
    JobRef,
    action_args,
    Jinja2DetailsPageUI,
    Decision,
    DecisionOption
)
from jinja2 import Environment, PackageLoader
from acolyte.core.flow import FlowMeta
from acolyte.core.service import Result
from acolyte.util.validate import IntField, StrField


jinja2_env = Environment(
    loader=PackageLoader('acolyte.builtin_ext', 'mooncake_ui'))


class ProgrammerJob(AbstractJob):

    def __init__(self):
        super().__init__(
            name="programmer",
            description=(
                "我是一个程序员，"
                "我的爱好是抢月饼！"
            ),
            ui=Jinja2DetailsPageUI(jinja2_env, "programmer.html")
        )

    def on_trigger(self, context):
        """程序员出场
        """
        return Result.ok(data="好吧，我要开始加班还房贷了")

    @action_args(
        ActionArg(
            IntField("cake_num", required=False, default=1, min_=1),
            mark=ActionArg.MARK_AUTO, comment="抢到的月饼数目"
        )
    )
    def on_midautumn(self, context, cake_num):
        context.finish()
        return Result.ok(data="我抢了{cake_num}个月饼".format(cake_num=cake_num))


class HRJob(AbstractJob):

    def __init__(self):
        super().__init__(
            name="hr",
            description=(
                "我是一个HR，"
                "我专门跟抢月饼的程序员过不去。"
            ),
            auto_trigger=True
        )

    def on_trigger(self, context):
        return Result.ok(data="刚才好像有人抢了月饼")

    @action_args(
        ActionArg(
            StrField("who", required=True, regex=r'^\w+$'),
            mark=ActionArg.MARK_AUTO,
            comment="抢月饼的人"
        )
    )
    def on_found(self, context, who):
        context.finish()
        return Result.ok(data="是{who}在抢月饼，我要去报告老板!".format(who=who))


class BossJob(AbstractJob):

    def __init__(self):
        super().__init__(
            name="boss",
            description=(
                "我是老板，"
                "我的心情即公司价值观"
            ),
            decisions=[
                Decision(
                    "handle_employee", "如何处理员工？",
                    DecisionOption("fire_him", "开除他！"),
                    DecisionOption("nice_mood", "没多大事，留下他吧。")
                ),
            ],
            auto_trigger=True
        )

    def on_trigger(self, context):
        return Result.ok(data="这个世界不是因为你能做什么，而是你该做什么。")

    @action_args(
        ActionArg(
            StrField("mood", required=True),
            mark=ActionArg.MARK_AUTO,
            comment="老板心情",
        )
    )
    def on_hr_report(self, context, mood):
        if mood == "好":
            context.finish()
            return Result.ok(data="Geek文化嘛，多大点儿事")
        else:
            context.failure()
            return Result.ok(data="不诚信，违反价值观，严肃处理")

    @action_args(
        ActionArg(
            StrField("reason", required=True),
            mark=ActionArg.MARK_AUTO,
            comment="开除原因"
        )
    )
    def on_fire_him(self, context, reason):
        context.failure()
        return Result.ok(data="开除此员工，因为：{}".format(reason))

    def on_nice_mood(self, context):
        context.finish()
        context.save({"boos_think": "Geek文化嘛，多大点儿事"})
        return Result.ok(data="Geek文化嘛，多大点儿事")


class MooncakeFlowMeta(FlowMeta):

    def __init__(self):
        super().__init__(
            name="mooncake_flow",
            description="抢月饼flow",
            jobs=(
                JobRef(
                    step_name="programmer",
                    job_name="programmer"
                ),
                JobRef(
                    step_name="hr",
                    job_name="hr"
                ),
                JobRef(
                    step_name="boss",
                    job_name="boss"
                )
            )
        )

    def on_start(self, context):
        ...

    def on_failure(self, context):
        ...

    def on_finish(self, context):
        ...
