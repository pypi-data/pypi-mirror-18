import typing
import inspect
import datetime
from abc import ABCMeta
from acolyte.core.job import ActionArg
from acolyte.core.flow import FlowMeta
from acolyte.core.notify import ReadStatus
from acolyte.core.mgr import AbstractManager
from acolyte.util.validate import (
    Field,
    IntField,
    StrField
)
from acolyte.util.lang import get_source_code


class ViewObject(metaclass=ABCMeta):

    """ViewObject用做最终输出的视图对象，可以直接序列化为json
    """
    ...


class UserSimpleView(ViewObject):

    """用户信息的简单视图
    """

    @classmethod
    def from_user(cls, user):
        return cls(user.id, user.email, user.name)

    def __init__(self, id_, email, name):
        self.id = id_
        self.email = email
        self.name = name


class FlowMetaView(ViewObject):

    """FlowMeta渲染视图
    """

    @classmethod
    def from_flow_meta(cls, flow_meta: FlowMeta, job_mgr: AbstractManager):
        """从FlowMeta对象来构建
           :param flow_meta: flow meta对象
           :param job_mgr: 用于获取Job对象
        """
        jobs = [JobRefView.from_job_ref(job_ref) for job_ref in flow_meta.jobs]
        return cls(
            flow_meta.name, flow_meta.description, jobs,
            get_source_code(flow_meta.__class__))

    def __init__(self, name: str, description: str,
                 jobs: list, source_code: str):
        """
        :param name: flow meta名称
        :param description: 描述
        :param jobs: job列表
        :param source_code: 源码
        """
        self.name = name
        self.description = description
        self.jobs = jobs
        self.source_code = source_code


class JobRefView(ViewObject):

    @classmethod
    def from_job_ref(cls, job_ref) -> ViewObject:
        return cls(job_ref.step_name, job_ref.job_name, job_ref.bind_args)

    def __init__(self, step_name: str, job_name: str,
                 bind_args: dict):
        """
        :param step_name: 步骤名称
        :param job_name: Job名称
        :param bind_args: 绑定参数
        """
        self.step_name = step_name
        self.job_name = job_name
        self.bind_args = bind_args


class FieldInfoView(ViewObject):

    """字段的类型和验证视图
    """

    @classmethod
    def from_field_obj(cls, field: Field):
        """从Field对象进行构建
        """
        if isinstance(field, StrField):
            return _StrFieldView(field.required, field.default,
                                 field.min_len, field.max_len, field.regex)
        elif isinstance(field, IntField):
            return _IntFieldView(
                field.required, field.default, field.min, field.max)
        else:
            return cls(field.type.__name__, field.required, field.default)

    def __init__(self, type_: str, required: bool, default: typing.Any):
        self.type = type_
        self.required = required
        self.default = default


class _IntFieldView(FieldInfoView):

    def __init__(self, required: bool, default: int,
                 min_: int or None, max_: int or None):
        super().__init__('int', required, default)
        self.min = min_
        self.max = max_


class _StrFieldView(FieldInfoView):

    def __init__(self, required: bool, default: str,
                 min_len: int or None, max_len: int or None,
                 regex: str or None):
        super().__init__('str', required, default)
        self.min_len = min_len
        self.max_len = max_len
        self.regex = regex


class JobArgView(ViewObject):

    @classmethod
    def from_job_arg(cls, job_arg: ActionArg) -> ViewObject:
        return cls(
            job_arg.name,
            FieldInfoView.from_field_obj(job_arg.field_info),
            job_arg.mark,
            job_arg.comment,
        )

    def __init__(self, name: str, field_info: FieldInfoView,
                 mark: str, comment: str):
        self.name = name
        self.field_info = field_info
        self.mark = mark
        self.comment = comment


class FlowTemplateView(ViewObject):

    @classmethod
    def from_flow_template(cls, flow_template, user):
        return FlowTemplateView(
            id_=flow_template.id,
            flow_meta=flow_template.flow_meta,
            name=flow_template.name,
            bind_args=flow_template.bind_args,
            max_run_instance=flow_template.max_run_instance,
            creator_info=UserSimpleView.from_user(user),
            config=flow_template.config
        )

    def __init__(self, id_: int, flow_meta: str, name: str,
                 bind_args: dict, max_run_instance: int,
                 creator_info: UserSimpleView, config: dict):
        self.id = id_
        self.flow_meta = flow_meta
        self.name = name
        self.bind_args = bind_args
        self.max_run_instance = max_run_instance
        self.creator_info = creator_info
        self.config = config


class FlowTemplateSimpleView(ViewObject):

    """简化版的FlowTemplate视图
       主要用于FlowInstance视图
    """

    @classmethod
    def from_flow_template(cls, flow_template, flow_meta_mgr):
        flow_meta = flow_meta_mgr.get(flow_template.flow_meta)
        return cls(flow_template.id, flow_meta.name, flow_template.name)

    def __init__(self, id_, flow_meta_name, name):
        """
        :param id_: 编号
        :param flow_meta_name: flow meta名称
        :param name: flow template名称
        """
        self.id = id_
        self.flow_meta_name = flow_meta_name
        self.name = name


class FlowSimpleInstanceView(ViewObject):

    """描述一个FlowInstance的简单实例
    """

    @classmethod
    def from_flow_instance(
            cls, flow_instance, group, flow_template, flow_meta_mgr, creator):

        return cls(
            id_=flow_instance.id,
            status=flow_instance.status,
            description=flow_instance.description,
            current_step=flow_instance.current_step,
            group=group,
            created_on=flow_instance.created_on,
            updated_on=flow_instance.updated_on,
            flow_template_info=FlowTemplateSimpleView.from_flow_template(
                flow_template, flow_meta_mgr),
            creator_info=UserSimpleView.from_user(creator)
        )

    def __init__(self, id_, status, description, current_step,
                 group, created_on, updated_on, flow_template_info,
                 creator_info):
        """
        :param id_: 编号
        :param status: 状态
        :param description: 描述
        :param current_step: 当前运行到的步骤
        :param group: 所属分组
        :param created_on: 创建时间
        :param updated_on: 最近更新时间
        :param flow_template_info: flow_template视图
        :param creator_info: creator视图
        """
        self.id = id_
        self.status = status
        self.description = description
        self.current_step = current_step
        self.group = group
        self.created_on = created_on
        self.updated_on = updated_on
        self.flow_template_info = flow_template_info
        self.creator_info = creator_info


class ActionDetailsView(ViewObject):

    @classmethod
    def from_action_mtd(cls, act_mtd, job_args):
        action_name = act_mtd.__name__[len("on_"):]
        return cls(
            action_name,
            doc=act_mtd.__doc__,
            args=[JobArgView.from_job_arg(a) for a in job_args[action_name]]
        )

    def __init__(self, name: str, doc: str, args: typing.List[JobArgView]):
        self.name = name
        self.doc = doc
        self.args = args


class JobDetailsView(ViewObject):

    @classmethod
    def from_job(cls, job):
        action_methods = [
            ActionDetailsView.from_action_mtd(mtd, job.job_args)
            for mtd_name, mtd in inspect.getmembers(job, inspect.ismethod)
            if mtd_name.startswith("on_")
        ]
        return cls(job.name, job.description, action_methods,
                   get_source_code(job.__class__))

    def __init__(self, name: str, description: str,
                 actions: typing.List[ActionDetailsView], source_code: str):
        self.name = name
        self.description = description
        self.actions = actions
        self.source_code = source_code


class JobInstanceSimpleView(ViewObject):

    @classmethod
    def from_job_instance(cls, job_instance):
        return cls(
            id_=job_instance.id,
            step_name=job_instance.step_name,
            job_name=job_instance.job_name,
            status=job_instance.status,
            created_on=job_instance.created_on,
            updated_on=job_instance.updated_on
        )

    def __init__(self, id_, step_name, job_name, status,
                 created_on, updated_on):
        self.id = id_
        self.step_name = step_name
        self.job_name = job_name
        self.status = status
        self.created_on = created_on
        self.updated_on = updated_on


class FlowInstanceDetailsView(ViewObject):

    @classmethod
    def from_flow_instance(cls, flow_instance, flow_tpl_view,
                           initiator_info, job_instance_list,
                           flow_discard_reason=None):
        return cls(
            id_=flow_instance.id,
            flow_tpl_view=flow_tpl_view,
            status=flow_instance.status,
            initiator_info=initiator_info,
            updated_on=flow_instance.updated_on,
            created_on=flow_instance.created_on,
            steps=[
                JobInstanceSimpleView.from_job_instance(instance)
                for instance in job_instance_list
            ],
            flow_discard_reason=flow_discard_reason
        )

    def __init__(self, id_: int, flow_tpl_view: FlowTemplateSimpleView,
                 status: str, initiator_info: UserSimpleView,
                 updated_on: datetime.datetime, created_on: datetime.datetime,
                 steps: typing.List[JobInstanceSimpleView],
                 flow_discard_reason=None):
        """FlowInstance详情
           :param id: 编号
           :param flow_tpl_view: simple flow template view
           :param status: 状态
           :param initiator_info: 触发者信息
           :param updated_on: 最近更新时间
           :param created_on: 创建时间
           :param steps: 执行步骤列表
           :param flow_discard_reason: 废弃原因
        """
        self.id = id_
        self.flow_tpl = flow_tpl_view
        self.status = status
        self.initiator_info = initiator_info
        self.updated_on = updated_on
        self.created_on = created_on
        self.steps = steps
        self.flow_discard_reason = flow_discard_reason


class JobActionDataDetailsView(ViewObject):

    @classmethod
    def from_job_action_data(cls, job_action_data, actor: UserSimpleView=None):
        return JobActionDataDetailsView(
            id_=job_action_data.id,
            action_name=job_action_data.action,
            arguments=job_action_data.arguments,
            data=job_action_data.data,
            created_on=job_action_data.created_on,
            updated_on=job_action_data.updated_on,
            actor=actor
        )

    def __init__(self, id_: int, action_name: str, arguments: typing.Dict,
                 data: typing.Dict, created_on: datetime.datetime,
                 updated_on: datetime.datetime, actor: UserSimpleView=None):
        self.id = id_
        self.action_name = action_name
        self.arguments = arguments
        self.data = data
        self.created_on = created_on
        self.updated_on = updated_on
        self.actor = actor


class JobInstanceDetailsView(ViewObject):

    @classmethod
    def from_job_instance(
            cls, job_instance, action_data_list, action_actors=None):

        if action_actors is None:
            action_actors = {}

        return JobInstanceDetailsView(
            id_=job_instance.id,
            step_name=job_instance.step_name,
            job_name=job_instance.job_name,
            status=job_instance.status,
            updated_on=job_instance.updated_on,
            created_on=job_instance.created_on,
            actions=[
                JobActionDataDetailsView.from_job_action_data(
                    act_data,
                    actor=UserSimpleView.from_user(
                        action_actors[act_data.actor])
                )
                for act_data in action_data_list
            ]
        )

    def __init__(self, id_: int, step_name: str, job_name: str,
                 status: str, created_on: datetime.datetime,
                 updated_on: datetime.datetime,
                 actions: typing.List[JobActionDataDetailsView]):
        self.id = id_
        self.step_name = step_name
        self.job_name = job_name
        self.status = status
        self.updated_on = updated_on
        self.created_on = created_on
        self.actions = actions


class DecisionView(ViewObject):

    @classmethod
    def from_decision_define(cls, decision, job_define):
        return cls(
            job_name=job_define.name,
            decision_name=decision.name,
            title=decision.title,
            prompt=decision.prompt,
            options=[
                DecisionOptionView.from_decision_option_define(
                    option,
                    job_define
                ) for option in decision.options
            ]
        )

    def __init__(self, job_name, decision_name, title, prompt, options):
        self.job_name = job_name
        self.decision_name = decision_name
        self.title = title
        self.prompt = prompt
        self.options = options


class DecisionOptionView(ViewObject):

    @classmethod
    def from_decision_option_define(cls, decision_option, job_define):
        return cls(
            action=decision_option.action,
            label=decision_option.label,
            action_args=[
                JobArgView.from_job_arg(action_arg)
                for action_arg in job_define.job_args.get(
                    decision_option.action, [])]
        )

    def __init__(self, action: str, label: str,
                 action_args: typing.List[JobArgView]):
        self.action = action
        self.label = label
        self.action_args = action_args


class FlowInstanceGroupDetailsView(ViewObject):

    @classmethod
    def from_flow_instance_group(
            cls, flow_instance_group, flow_simple_instance_view_lst):
        return cls(
            id_=flow_instance_group.id,
            name=flow_instance_group.name,
            description=flow_instance_group.description,
            status=flow_instance_group.status,
            created_on=flow_instance_group.created_on,
            updated_on=flow_instance_group.updated_on,
            flow_simple_instance_view_lst=flow_simple_instance_view_lst
        )

    def __init__(self, id_: int, name: str, description: str, status: str,
                 created_on: datetime.datetime, updated_on: datetime.datetime,
                 flow_simple_instance_view_lst):
        self.id = id_
        self.name = name
        self.description = description
        self.status = status
        self.created_on = created_on
        self.updated_on = updated_on
        self.flow_simple_instance_view_lst = flow_simple_instance_view_lst


class FlowInstanceGroupSimpleView(ViewObject):

    @classmethod
    def from_flow_instance_group(
            cls, flow_instance_group, sub_flow_num, sub_flow_status):
        return cls(
            id_=flow_instance_group.id,
            name=flow_instance_group.name,
            description=flow_instance_group.description,
            status=flow_instance_group.status,
            created_on=flow_instance_group.created_on,
            updated_on=flow_instance_group.updated_on,
            sub_flow_num=sub_flow_num,
            sub_flow_status=sub_flow_status
        )

    def __init__(self, id_: int, name: str, description: str,
                 status: str, created_on: datetime.datetime,
                 updated_on: datetime.datetime, sub_flow_num: int,
                 sub_flow_status: typing.Dict[str, int]):
        self.id = id_
        self.name = name
        self.description = description
        self.status = status
        self.created_on = created_on
        self.updated_on = updated_on
        self.sub_flow_num = sub_flow_num
        self.sub_flow_status = sub_flow_status


class NotifySimpleView(ViewObject):

    @classmethod
    def from_notify_index(cls, notify_index, notify_tpl_manager):
        notify_tpl = notify_tpl_manager.get(notify_index.notify_template)
        return cls(
            id_=notify_index.id,
            subject=notify_tpl.render_subject(
                **notify_tpl.subject_template_args),
            digest=notify_tpl.render_digest(
                **notify_tpl.content_template_args),
            read_status=notify_index.read_status,
            created_on=notify_index.created_on
        )

    def __init__(
            self, id_: int, subject: str,
            digest: str, read_status: ReadStatus,
            created_on: datetime.datetime):
        self.id = id_
        self.subject = subject
        self.digest = digest
        self.read_status = read_status
        self.created_on = created_on


class NotifyDetailsView(ViewObject):

    @classmethod
    def from_notify_index(cls, notify_index, notify_tpl_manager):
        notify_tpl = notify_tpl_manager.get(notify_index.notify_template)
        return cls(
            id_=notify_index.id,
            subject=notify_tpl.render_subject(
                **notify_tpl.subject_template_args),
            digest=notify_tpl.render_digest(
                **notify_tpl.digest_template_args),
            content=notify_tpl.render_content(
                **notify_tpl.content_template_args),
            read_status=notify_index.read_status,
            created_on=notify_index.created_on
        )

    def __init__(self, id_: int, subject: str, digest: str, content: str,
                 read_status: ReadStatus, created_on: datetime.datetime):
        self.id = id_
        self.subject = subject
        self.digest = digest
        self.content = content
        self.read_status = read_status
        self.created_on = created_on
