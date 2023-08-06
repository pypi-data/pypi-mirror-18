import locale
import simplejson as json
from collections import ChainMap
from contextlib import contextmanager
from typing import Dict, Any
from acolyte.util import log
from acolyte.util.json import to_json
from acolyte.util.service_container import ServiceContainer
from acolyte.core.service import (
    AbstractService,
    Result,
)
from acolyte.core.flow import (
    FlowStatus,
    FlowInstanceGroupStatus
)
from acolyte.core.job import (
    JobStatus,
    ActionArg,
    ActionLockType,
    ActionRunTimes,
)
from acolyte.core.context import MySQLContext
from acolyte.core.storage.user import UserDAO
from acolyte.core.storage.flow_template import FlowTemplateDAO
from acolyte.core.storage.flow_instance import FlowInstanceDAO
from acolyte.core.storage.job_instance import JobInstanceDAO
from acolyte.core.storage.job_action_data import JobActionDataDAO
from acolyte.core.storage.flow_discard_reason import FlowDiscardReasonDAO
from acolyte.core.storage.flow_instance_group import (
    FlowInstanceGroupDAO,
    FlowInstanceGroupRelationDAO,
)
from acolyte.core.message import default_validate_messages
from acolyte.util.validate import (
    IntField,
    StrField,
    Field,
    check,
    BadReq,
    InvalidFieldException
)
from acolyte.exception import ObjectNotFoundException


class FlowExecutorService(AbstractService):

    def __init__(self, service_container: ServiceContainer):
        super().__init__(service_container)

    def _after_register(self):
        # 获取各种所依赖的服务
        self._db = self._("db")
        self._flow_tpl_dao = FlowTemplateDAO(self._db)
        self._flow_meta_mgr = self._("flow_meta_manager")
        self._job_mgr = self._("job_manager")
        self._flow_instance_dao = FlowInstanceDAO(self._db)
        self._user_dao = UserDAO(self._db)
        self._job_instance_dao = JobInstanceDAO(self._db)
        self._job_action_dao = JobActionDataDAO(self._db)
        self._flow_discard_dao = FlowDiscardReasonDAO(self._db)
        self._flow_instance_group_dao = FlowInstanceGroupDAO(self._db)
        self._flow_instance_group_rlt_dao = FlowInstanceGroupRelationDAO(
            self._db)

    @check(
        IntField("flow_template_id", required=True),
        IntField("initiator", required=True),
        StrField("description", required=True, max_len=1000),
        Field("start_flow_args", type_=dict, required=False,
              default=None, value_of=json.loads),
        IntField("group", required=False, default=0)
    )
    def start_flow(self, flow_template_id: int,
                   initiator: int, description: str,
                   start_flow_args: Dict[str, Any], group=0) -> Result:
        """开启一个flow进程，创建flow_instance并执行第一个Job

           S1. 根据flow_template_id获取flow_template，然后获取flow_meta，如果获取失败，返回错误
           S2. 检查并合并参数
           S3. 检查max_run_instance
           S4. 创建一条新的flow_instance记录
           S5. 创建context
           S6. 回调flow meta中on_start方法的逻辑

           :param flow_template_id: 使用的flow template
           :param initiator: 发起人
           :param description: 本次flow描述
           :param start_flow_args: 执行FlowMeta的on_start方法时所需要的参数
           :param group: flow instance所属的组，默认为0，不属于任何组
        """

        if start_flow_args is None:
            start_flow_args = {}

        # 检查flow_template_id是否合法
        flow_template = self._flow_tpl_dao.query_flow_template_by_id(
            flow_template_id)
        if flow_template is None:
            raise BadReq("invalid_flow_template",
                         flow_template_id=flow_template_id)
        flow_meta = self._flow_meta_mgr.get(flow_template.flow_meta)
        if flow_meta is None:
            raise BadReq("invalid_flow_meta", flow_meta=flow_meta)

        # 检查发起者
        initiator_user = self._user_dao.query_user_by_id(initiator)
        if initiator_user is None:
            raise BadReq("invalid_initiator", initiator=initiator)

        # 检查group
        if group:
            flow_instance_group = self._flow_instance_group_dao\
                .query_by_id(group)
            if flow_instance_group is None:
                raise BadReq("group_not_exist")

        # 检查并合并start_flow_args
        field_rules = getattr(flow_meta.on_start, "field_rules", [])
        rs = self._combine_and_check_args(
            "start", field_rules, start_flow_args, flow_meta.start_args)
        if rs.status_code == Result.STATUS_BADREQUEST:
            return rs
        start_flow_args = rs.data

        # 锁定检查instance数目并创建第一条记录
        flow_instance = None
        if flow_template.max_run_instance > 0:
            lock_key = "lock_instance_create_{tpl_id}".format(
                tpl_id=flow_template_id)
            with self._db.lock(lock_key):
                current_instance_num = self._flow_instance_dao.\
                    query_running_instance_num_by_tpl_id(flow_template_id)
                if current_instance_num >= flow_template.max_run_instance:
                    raise BadReq(
                        reason="too_many_instance",
                        allow_instance_num=flow_template.max_run_instance
                    )
                flow_instance = self._flow_instance_dao.insert(
                    flow_template_id, initiator, description)
        else:
            flow_instance = self._flow_instance_dao.insert(
                flow_template_id, initiator, description)

        # 创建Context
        ctx = MySQLContext(
            flow_executor=self,
            config=flow_template.config,
            db=self._db,
            flow_instance_id=flow_instance.id
        )

        # 回调on_start
        flow_meta.on_start(ctx, **start_flow_args)

        # 将状态更新到running
        self._flow_instance_dao.update_status(
            flow_instance.id, FlowStatus.STATUS_RUNNING)

        # 添加组
        if group:
            self._flow_instance_group_rlt_dao.insert(flow_instance.id, group)

        log.acolyte.info(
            "start flow instance {}".format(to_json(flow_instance)))

        return Result.ok(data=flow_instance)

    @check(
        IntField("flow_instance_id", required=True),
        StrField("target_step", required=True),
        StrField("target_action", required=True),
        IntField("actor", required=True),
        Field("action_args", type_=dict, required=False,
              default=None, value_of=json.loads)
    )
    def handle_job_action(self, flow_instance_id: int,
                          target_step: str, target_action: str,
                          actor: int, action_args: Dict[str, Any]) -> Result:
        """处理Job中的Action

           S1. 检查并获取flow实例
           S2. 检查job以及job_action的存在性
           S3. 检查执行人是否合法
           S4. 检查当前是否可以允许该step及target_action的执行
           S5. 合并以及检查相关参数
           S6. 回调相关Action逻辑
           S7. 返回回调函数的返回值

           :param flow_instance_id: flow的标识
           :param target_step: 要执行的Step
           :param target_action: 自定义的动作名称
           :param actor: 执行人
           :param action_args: 执行该自定义动作所需要的参数
        """

        if action_args is None:
            action_args = {}

        # 检查flow instance的id合法性
        flow_instance = self._flow_instance_dao.query_by_instance_id(
            flow_instance_id)
        if flow_instance is None:
            raise BadReq("invalid_flow_instance",
                         flow_instance_id=flow_instance_id)

        # 检查flow instance的状态
        if flow_instance.status != FlowStatus.STATUS_RUNNING:
            raise BadReq("invalid_status", status=flow_instance.status)

        # 获取对应的flow template和flow meta
        flow_template = self._flow_tpl_dao\
            .query_flow_template_by_id(flow_instance.flow_template_id)
        if flow_template is None:
            raise BadReq("unknown_flow_template",
                         flow_template_id=flow_instance.flow_template_id)
        try:
            flow_meta = self._flow_meta_mgr.get(flow_template.flow_meta)
        except ObjectNotFoundException:
            raise BadReq("unknown_flow_meta", flow_meta=flow_meta)

        actor_info = self._user_dao.query_user_by_id(actor)
        if actor_info is None:
            raise BadReq("invalid_actor", actor=actor)

        # 检查当前step以及当前step是否完成
        # 检查下一个状态是否是目标状态
        handler_mtd, job_def, job_ref = self._check_step(
            flow_meta, flow_instance, target_step, target_action)

        # 合并检查参数 request_args - template_bind_args - meta_bind_args
        rs = self._check_and_combine_action_args(
            job_def, target_action, action_args, job_ref, flow_template)
        if rs.status_code == Result.STATUS_BADREQUEST:
            return rs

        action_args = rs.data

        job_instance = self._job_instance_dao.query_by_instance_id_and_step(
            instance_id=flow_instance_id,
            step=target_step
        )

        action_constraint = job_def.action_constraints.get(target_action)

        with self._check_constraint(
                action_constraint, flow_instance_id,
                job_instance, target_action):

            # 如果是trigger事件，需要创建job_instance记录
            if target_action == "trigger":
                job_instance = self._job_instance_dao.insert(
                    flow_instance_id, target_step, job_def.name, actor)
                self._flow_instance_dao.update_current_step(
                    flow_instance_id, target_step)

            action = self._job_action_dao.insert(
                job_instance_id=job_instance.id,
                action=target_action,
                actor=actor,
                arguments=action_args,
                data_key="",
                data={}
            )

            ctx = MySQLContext(
                flow_executor=self,
                config=flow_template.config,
                db=self._db,
                flow_instance_id=flow_instance.id,
                job_instance_id=job_instance.id,
                job_action_id=action.id,
                job_action=target_action,
                flow_meta=flow_meta,
                current_step=target_step,
                actor=actor,
                action_queues=job_def.action_queues
            )

            try:
                exec_rs = handler_mtd(ctx, **action_args)
                if not isinstance(exec_rs, Result):
                    exec_rs = Result.ok(data=exec_rs)
            except Exception as e:
                self._job_action_dao.delete_by_id(action.id)
                log.error.exception(e)
                return Result.service_error("service_error", msg="服务器开小差了")
            else:
                if not exec_rs.is_success():
                    # 如果返回结果不成功，那么允许重来
                    self._job_action_dao.delete_by_id(action.id)
                else:
                    self._job_action_dao.sync_updated_on(action.id)

            log.acolyte.info((
                "Job action executed, "
                "action_data = {action_data}, "
                "action_result = {action_result}"
            ).format(
                action_data=to_json(action),
                action_result=to_json(rs)
            ))

            return exec_rs

    def _check_and_combine_action_args(
            self, job_def, target_action, request_args,
            job_ref, flow_template):

        job_arg_defines = job_def.job_args.get(target_action)

        # 无参数定义
        if not job_arg_defines:
            return Result.ok(data={})

        # 获取各级的参数绑定
        meta_bind_args = job_ref.bind_args.get(target_action, {})
        tpl_bind_args = flow_template.bind_args.get(
            job_ref.step_name, {}).get(target_action, {})

        args_chain = ChainMap(request_args, tpl_bind_args, meta_bind_args)

        # 最终生成使用的参数集合
        args = {}

        for job_arg_define in job_arg_defines:
            try:
                arg_name = job_arg_define.name

                # auto 类型，直接从chain中取值
                if job_arg_define.mark == ActionArg.MARK_AUTO:
                    value = args_chain[arg_name]
                # static类型，从template中取值
                elif job_arg_define.mark == ActionArg.MARK_STATIC:
                    value = tpl_bind_args.get(arg_name, None)

                    # 如果值是以$config.开头，那么从flow_template.config中替换值
                    if value and isinstance(value, str) and \
                            value.startswith('$config.'):
                        value = flow_template.config.get(
                            value[len('$config.'):])

                # const类型，从meta中取值
                elif job_arg_define.mark == ActionArg.MARK_CONST:
                    value = meta_bind_args.get(arg_name, None)

                args[arg_name] = job_arg_define.field_info(value)
            except InvalidFieldException as e:
                full_field_name = "{step}.{action}.{arg}".format(
                    step=job_ref.step_name,
                    action=target_action,
                    arg=arg_name
                )
                return self._gen_bad_req_result(e, full_field_name)

        return Result.ok(data=args)

    def _check_step(self, flow_meta, flow_instance,
                    target_step, target_action):
        current_step = flow_instance.current_step

        # 检查当前action的方法是否存在
        target_job_ref = flow_meta.get_job_ref_by_step_name(target_step)
        if target_job_ref is None:
            raise BadReq("unknown_target_step", target_step=target_step)
        try:
            job_def = self._job_mgr.get(target_job_ref.job_name)
        except ObjectNotFoundException:
            raise BadReq("unknown_job", job_name=target_job_ref.name)

        handler_mtd = getattr(job_def, "on_" + target_action, None)
        if handler_mtd is None:
            raise BadReq("unknown_action_handler", action=target_action)

        # 当前step即目标step
        if current_step == target_step:

            job_instance = self._job_instance_dao.\
                query_by_instance_id_and_step(
                    instance_id=flow_instance.id,
                    step=current_step
                )

            if job_instance.status == JobStatus.STATUS_FINISHED:
                raise BadReq("step_already_runned", step=target_step)

            # 检查当前action是否被执行过
            # action = self._job_action_dao.\
            #     query_by_job_instance_id_and_action(
            #         job_instance_id=job_instance.id,
            #         action=target_action
            #     )

            # if action:
            #     raise BadReq("action_already_runned", action=target_action)

            # 如果非trigger，则检查trigger是否执行过
            if target_action != "trigger":
                trigger_action = self._job_action_dao.\
                    query_by_job_instance_id_and_action(
                        job_instance_id=job_instance.id,
                        action="trigger"
                    )
                if trigger_action is None:
                    raise BadReq("no_trigger")

            return handler_mtd, job_def, target_job_ref

        if current_step != "start":
            # 当前step非目标step
            job_instance = self._job_instance_dao.\
                query_by_instance_id_and_step(
                    instance_id=flow_instance.id,
                    step=current_step
                )

            # 流程记录了未知的current_step
            if job_instance is None:
                raise BadReq("unknown_current_step", current_step=current_step)

            # 当前的step尚未完成
            if job_instance.status != JobStatus.STATUS_FINISHED:
                raise BadReq("current_step_unfinished",
                             current_step=current_step)

        # 获取下一个该运行的步骤
        next_step = flow_meta.get_next_step(current_step)
        if next_step.step_name != target_step:
            raise BadReq("invalid_target_step", next_step=next_step)
        if target_action != "trigger":
            raise BadReq("no_trigger")

        return handler_mtd, job_def, target_job_ref

    def _combine_and_check_args(
            self, action_name, field_rules, *args_dict):
        """合并 & 检查参数 先合并，后检查
           :param field_rules: 字段规则
           :param old_args
        """
        _combined_args = ChainMap(*args_dict).new_child()

        # 木有验证规则，直接返回数据
        if not field_rules:
            return Result.ok(data=_combined_args)

        try:
            for field_rule in field_rules:
                # 检查并替换掉相关参数
                val = field_rule(_combined_args[field_rule.name])
                _combined_args[field_rule.name] = val
        except InvalidFieldException as e:
            full_field_name = "{action_name}.{field_name}".format(
                action_name=action_name,
                field_name=e.field_name
            )
            return self._gen_bad_req_result(e, full_field_name)
        else:
            return Result.ok(data=_combined_args)

    def _gen_bad_req_result(self, e, full_field_name):
        loc, _ = locale.getlocale(locale.LC_CTYPE)
        full_reason = "{full_field_name}_{reason}".format(
            full_field_name=full_field_name,
            reason=e.reason
        )
        msg = default_validate_messages[loc][e.reason]
        if e.expect is None or e.expect == "":
            msg = msg.format(field_name=full_field_name)
        else:
            msg = msg.format(
                field_name=full_field_name, expect=e.expect)
        return Result.bad_request(reason=full_reason, msg=msg)

    @contextmanager
    def _check_constraint(self,
                          action_constraint, flow_instance_id,
                          job_instance, target_action):
        if action_constraint is None:
            yield
        else:
            if job_instance is not None:
                # 测试最大可运行数
                actions = self._job_action_dao.\
                    query_by_job_instance_id_and_action(
                        job_instance_id=job_instance.id,
                        action=target_action
                    )

                if (
                    len(actions) > 0 and
                    action_constraint.run_times == ActionRunTimes.ONCE
                ):
                    raise BadReq("action_already_runned", action=target_action)

            lock = action_constraint.lock
            # 处理独占锁
            if lock and lock.lock_type == ActionLockType.USER_EXCLUSIVE_LOCK:
                with self._db.lock(
                        lock.gen_lock_key(flow_instance_id), 0) as lock_rs:
                    if not lock_rs:
                        raise BadReq("someone_operating")
                    yield

    def _finish_step(self, ctx, waiting_for=None):
        """标记一个job instance完成，通常由action通过context进行回调
           S1. 将job_instance的状态更新为finish
           S2. 检查整个flow是否已经完成
           S3. 如果整个流程已经完成，那么标记flow_instance的status
           S4. 回调flow_meta中的on_finish事件
        """
        flow_instance_id, job_instance_id = (
            ctx.flow_instance_id,
            ctx.job_instance_id
        )

        if waiting_for:
            # 做个标记，偶已经执行完了

            _barrier_key = self._gen_barrier_key(
                job_instance_id, ctx.job_action)
            ctx[_barrier_key] = True

            # 加个大锁，避免mark finish状态mark重了
            with self._db.lock(
                    "action_barrier_lock_{}".format(job_instance_id)):

                job_instance = self._job_instance_dao.query_by_id(
                    job_instance_id)

                # job 已经被标记完成了，什么都不需要做了
                if job_instance.status == JobStatus.STATUS_FINISHED:
                    return

                # 检查依赖的action是否都执行完毕了，都执行完毕了就可以安全的标记完成状态
                if all(
                    ctx[self._gen_barrier_key(job_instance_id, action)]
                    for action in waiting_for
                ):
                    self._mark_finish_step(
                        ctx, flow_instance_id, job_instance_id)
        else:
            self._mark_finish_step(ctx, flow_instance_id, job_instance_id)

    def _gen_barrier_key(self, job_instance_id, job_action):
        return ("__action_barrier_"
                "{job_instance_id}_"
                "{job_action}"
                ).format(
                    job_instance_id=job_instance_id,
                    job_action=job_action)

    def _mark_finish_step(self, ctx, flow_instance_id, job_instance_id):
        self._job_instance_dao.update_status(
            job_instance_id=job_instance_id,
            status=JobStatus.STATUS_FINISHED
        )

        next_step = ctx.flow_meta.get_next_step(ctx.current_step)

        # 尚未完成，继续处理
        if next_step != "finish":
            next_step_job = self._job_mgr.get(next_step.job_name)
            # 下一个Step为自动触发类型
            if next_step_job.auto_trigger:
                self.handle_job_action(
                    flow_instance_id=ctx.flow_instance_id,
                    target_step=next_step.step_name,
                    target_action="trigger",
                    actor=ctx.actor,
                    action_args={}
                )
            return

        # 修改flow_instance的状态
        self._flow_instance_dao.update_status(
            flow_instance_id=flow_instance_id,
            status=FlowStatus.STATUS_FINISHED
        )

        # 回调on_finish事件
        on_finish_handler = getattr(ctx.flow_meta, "on_finish", None)
        if on_finish_handler is None:
            return
        on_finish_handler(ctx)

    def _failure_whole_flow(self, ctx):
        """终止整个flow的运行，通常由action通过context进行回调
           S1. 标记job_instance的status为stop
           S2. 标记flow_instance的status为stop
           S3. 回调flow_meta中的on_stop事件
        """
        self._job_instance_dao.update_status(
            job_instance_id=ctx.job_instance_id,
            status=JobStatus.STATUS_FAILURE
        )
        self._flow_instance_dao.update_status(
            flow_instance_id=ctx.flow_instance_id,
            status=FlowStatus.STATUS_FAILURE
        )

        # 回调on_stop事件
        on_failure_handler = getattr(ctx.flow_meta, "on_failure", None)
        if on_failure_handler is None:
            return
        on_failure_handler(ctx)

    def _handle_exception(self, job_instance_id, exc_type, exc_val, traceback):
        """标记Flow为Exception状态
        """
        pass

    @check(
        IntField("flow_instance_id", required=True),
        IntField("actor_id", required=True),
        StrField("discard_reason", required=False, max_len=1000, default="")
    )
    def discard_flow_instance(
            self, flow_instance_id, actor_id, discard_reason):
        """手工废弃整个flow instance
        """
        flow_instance = self._flow_instance_dao\
            .query_by_instance_id(flow_instance_id)

        # 检查flow_instance的存在性
        if flow_instance is None:
            raise BadReq("flow_instance_not_found")

        if flow_instance.status not in (
            FlowStatus.STATUS_RUNNING,
            FlowStatus.STATUS_INIT,
            FlowStatus.STATUS_WAITING
        ):
            raise BadReq("invalid_status", current_status=flow_instance.status)

        self._flow_instance_dao.update_status(
            flow_instance_id, FlowStatus.STATUS_DISCARD)

        # 插入废弃原因
        self._flow_discard_dao.insert(
            flow_instance_id, actor_id, discard_reason)

        return Result.ok()

    @check(
        StrField("name", required=True),
        StrField("description", required=False),
        Field("meta", required=False, type_=dict,
              value_of=json.loads, default=None)
    )
    def create_flow_instance_group(self, name, description, meta):
        """
        创建flow instance group
        S1. 检查name是否已经存在
        S2. 执行创建
        S3. 返回新创建的instance group对象
        :param name: group name
        :param description: 描述
        :param meta: group相关的meta信息
        """
        flow_instance_group = self._flow_instance_group_dao\
            .query_by_name(name)

        if flow_instance_group is not None:
            raise BadReq("group_existed", name=name)

        flow_instance_group = self._flow_instance_group_dao.insert(
            name=name,
            description=description,
            meta=meta,
            status=FlowInstanceGroupStatus.STATUS_RUNNING
        )
        return Result.ok(data=flow_instance_group)

    def _finish_instance_group(self, context):
        """标记instance group记录为完成状态，通常由上下文对象进行回调
        """
        flow_instance_id = context.flow_instance_id
        group_id = self._flow_instance_group_rlt_dao\
            .query_group_id_by_instance_id(flow_instance_id)

        if not group_id:
            # do nothing
            return

        self._flow_instance_group_dao\
            .update_status(
                group_id, FlowInstanceGroupStatus.STATUS_FINISHED)
