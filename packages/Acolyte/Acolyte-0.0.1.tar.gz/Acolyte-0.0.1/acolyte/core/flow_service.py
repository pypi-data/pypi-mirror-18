"""本模块包含跟flow相关的facade接口
"""

import simplejson as json
import datetime
import locale
from collections import Counter, defaultdict
from acolyte.util import log
from acolyte.util.json import to_json
from acolyte.util.validate import (
    Field,
    IntField,
    StrField,
    check,
    BadReq,
    InvalidFieldException
)
from acolyte.util.lang import get_from_nested_dict
from acolyte.core.service import (
    AbstractService,
    Result
)
from acolyte.core.flow import FlowTemplate, FlowStatus
from acolyte.core.mgr import ObjectNotFoundException
from acolyte.core.storage.flow_template import FlowTemplateDAO
from acolyte.core.storage.flow_instance import FlowInstanceDAO
from acolyte.core.storage.job_instance import JobInstanceDAO
from acolyte.core.storage.flow_discard_reason import FlowDiscardReasonDAO
from acolyte.core.storage.flow_instance_group import (
    FlowInstanceGroupDAO,
    FlowInstanceGroupRelationDAO
)
from acolyte.core.storage.user import UserDAO
from acolyte.core.view import (
    FlowMetaView,
    FlowTemplateView,
    FlowTemplateSimpleView,
    FlowSimpleInstanceView,
    FlowInstanceDetailsView,
    FlowInstanceGroupDetailsView,
    FlowInstanceGroupSimpleView
)
from acolyte.core.job import ActionArg
from acolyte.core.message import default_validate_messages


class FlowService(AbstractService):

    def __init__(self, service_container):
        super().__init__(service_container)

    def _after_register(self):
        # 注入两个manager
        self._flow_meta_mgr = self._("flow_meta_manager")
        self._job_mgr = self._("job_manager")
        db = self._("db")
        self._flow_tpl_dao = FlowTemplateDAO(db)
        self._user_dao = UserDAO(db)
        self._flow_instance_dao = FlowInstanceDAO(db)
        self._job_instance_dao = JobInstanceDAO(db)
        self._flow_discard_reason_dao = FlowDiscardReasonDAO(db)
        self._flow_instance_group_dao = FlowInstanceGroupDAO(db)
        self._flow_instance_group_rlt_dao = FlowInstanceGroupRelationDAO(db)

    def get_all_flow_meta(self) -> Result:
        """获得所有注册到容器的flow_meta信息
           :return [

                {

                    "name": "mooncake_flow",
                    "description": "just a test flow",
                    "jobs": [
                        {
                            "step_name": "programmer",
                            "job_name": "programmer",
                            "bind_args": {
                                "trigger": {
                                    "a": 1,
                                    "b": 2,
                                }
                            }
                        }
                    ]
                },
           ]
        """
        all_flow_meta = [
            FlowMetaView.from_flow_meta(meta, self._job_mgr)
            for meta in self._flow_meta_mgr.all()
        ]
        return Result.ok(data=all_flow_meta)

    @check(
        StrField("flow_meta_name", required=True),
    )
    def get_flow_meta_info(self, flow_meta_name) -> Result:
        """获取单个的flow_meta详情
        """

        try:
            flow_meta = self._flow_meta_mgr.get(flow_meta_name)
        except ObjectNotFoundException:
            raise BadReq("flow_meta_not_exist", flow_meta=flow_meta_name)

        return Result.ok(data=FlowMetaView.from_flow_meta(
            flow_meta, self._job_mgr))

    @check(
        StrField("flow_meta_name", required=True),
        StrField("name", required=True, min_len=3, max_len=50,
                 regex="^[a-zA-Z0-9_]+$"),
        Field("bind_args", type_=dict, required=True, value_of=json.loads),
        IntField("max_run_instance", required=True, min_=0),
        Field("config", type_=dict, required=True, value_of=json.loads),
        IntField("creator", required=True)
    )
    def create_flow_template(self, flow_meta_name, name, bind_args,
                             max_run_instance, config, creator) -> Result:
        """创建flow_template
        """

        # 获取flow_meta以及检查其存在性
        try:
            flow_meta = self._flow_meta_mgr.get(flow_meta_name)
        except ObjectNotFoundException:
            raise BadReq("flow_meta_not_exist", flow_meta=flow_meta_name)

        # 检查name是否已经存在
        if self._flow_tpl_dao.is_name_existed(name):
            raise BadReq("name_already_exist", name=name)

        # 检查creator是否存在
        creator_user = self._user_dao.query_user_by_id(creator)
        if not creator_user:
            raise BadReq("invalid_creator_id", creator=creator)

        # 校验参数
        rs = self._validate_tpl_bind_args(flow_meta, config, bind_args)
        if rs.status_code == Result.STATUS_BADREQUEST:
            return rs
        bind_args = rs.data

        created_on = datetime.datetime.now()

        # 插入吧!
        flow_template = self._flow_tpl_dao.insert_flow_template(
            flow_meta_name, name, bind_args, max_run_instance, config,
            creator, created_on)

        log.acolyte.info(
            "New flow template created, {}".format(to_json(flow_template)))

        # 返回刚创建的View
        return Result.ok(
            data=FlowTemplateView.from_flow_template(
                flow_template, creator_user))

    @check(
        IntField("flow_tpl_id", required=True),
        StrField("name", required=True, min_len=3, max_len=50,
                 regex="^[a-zA-Z0-9_]+$"),
        Field("bind_args", type_=dict, required=True, value_of=json.loads),
        IntField("max_run_instance", required=True, min_=0),
        Field("config", type_=dict, required=True, value_of=json.loads)
    )
    def modify_flow_template(self, flow_tpl_id, name, bind_args,
                             max_run_instance, config):
        """
        S1. 检查flow tpl是否存在
        S2. 检查名字是否改变，如果名字改变了，那么检查是否重复
        S3. 检查参数
        S4. 执行修改，返回结果
        """
        flow_tpl = self._flow_tpl_dao.query_flow_template_by_id(flow_tpl_id)
        if flow_tpl is None:
            raise BadReq("tpl_not_found", flow_tpl_id=flow_tpl_id)

        # 名字已经改变了，检查新名字是否已经存在
        if flow_tpl.name != name:
            if self._flow_tpl_dao.is_name_existed(name):
                raise BadReq("name_exist", name=name)

        # 检查参数
        flow_meta = self._flow_meta_mgr.get(flow_tpl.flow_meta)
        rs = self._validate_tpl_bind_args(flow_meta, config, bind_args)
        if rs.status_code == Result.STATUS_BADREQUEST:
            return rs
        bind_args = rs.data

        self._flow_tpl_dao.update_flow_template(
            flow_tpl_id, name, bind_args, max_run_instance, config)

        creator_info = self._user_dao.query_user_by_id(flow_tpl.creator)

        return Result.ok(data=FlowTemplateView.from_flow_template(
            FlowTemplate(
                id_=flow_tpl_id,
                flow_meta=flow_tpl.flow_meta,
                name=name,
                bind_args=bind_args,
                max_run_instance=max_run_instance,
                config=config,
                creator=flow_tpl.creator,
                created_on=flow_tpl.created_on
            ),
            creator_info
        ))

    # 校验template的绑定参数
    def _validate_tpl_bind_args(self, flow_meta, config, bind_args):
        new_bind_args = {}

        for job_ref in flow_meta.jobs:

            job = self._job_mgr.get(job_ref.job_name)
            new_bind_args[job.name] = {}

            for event, job_arg_declares in job.job_args.items():

                new_bind_args[job.name][event] = {}

                for job_arg_declare in job_arg_declares:

                    try:

                        bind_value = get_from_nested_dict(
                            bind_args, job.name, event, job_arg_declare.name)

                        # const 类型的参数不允许被绑定
                        if job_arg_declare.mark == ActionArg.MARK_CONST:
                            continue

                        # 如果为None并且是auto类型，那么可以在此不检查
                        if bind_value is None and \
                                job_arg_declare.mark == ActionArg.MARK_AUTO:
                            continue

                        if bind_value and isinstance(bind_value, str) \
                                and bind_value.startswith("$config."):
                            bind_value = config.get(
                                bind_value[len("$config."):])

                        # 执行校验并替换新值
                        new_value = job_arg_declare.field_info(bind_value)
                        new_bind_args[job.name][event][
                            job_arg_declare.name] = new_value

                    except InvalidFieldException as e:

                        field_name = "{job_name}_{event}_{arg_name}".format(
                            job_name=job.name,
                            event=event,
                            arg_name=job_arg_declare.name
                        )
                        full_reason = "{field_name}_{reason}".format(
                            field_name=field_name,
                            reason=e.reason
                        )

                        # 产生错误消息
                        loc, _ = locale.getlocale(locale.LC_CTYPE)
                        msg = default_validate_messages[loc][e.reason]
                        if e.expect is None:
                            msg = msg.format(field_name=field_name)
                        else:
                            msg = msg.format(
                                field_name=field_name, expect=e.expect)

                        return Result.bad_request(full_reason, msg=msg)

        return Result.ok(data=new_bind_args)

    def get_all_flow_templates(self):
        """获取所有的flow_templates列表
        """
        all_flow_templates = self._flow_tpl_dao.query_all_templates()
        if not all_flow_templates:
            return Result.ok(data=[])
        users = self._user_dao.query_users_by_id_list(
            [tpl.creator for tpl in all_flow_templates], to_dict=True)
        templates_view = [FlowTemplateView.from_flow_template(
            tpl, users[tpl.creator]) for tpl in all_flow_templates]
        return Result.ok(data=templates_view)

    @check(
        IntField("flow_template_id", required=True)
    )
    def get_flow_template(self, flow_template_id: int):
        """获取单个的flow_template详情
        """
        flow_template = self._flow_tpl_dao.query_flow_template_by_id(
            flow_template_id)
        if flow_template is None:
            raise BadReq("not_found", flow_template_id=flow_template_id)
        creator = self._user_dao.query_user_by_id(flow_template.creator)
        return Result.ok(
            FlowTemplateView.from_flow_template(flow_template, creator))

    @check(
        StrField("flow_meta_name", required=True)
    )
    def get_flow_templates_by_flow_meta_name(self, flow_meta_name: str):
        """根据flow meta来获取flow template列表
        """
        try:
            self._flow_meta_mgr.get(flow_meta_name)
        except ObjectNotFoundException:
            raise BadReq("unknown_flow_meta", flow_meta_name=flow_meta_name)

        flow_temlates = self._flow_tpl_dao.query_by_flow_meta_name(
            flow_meta_name)

        if not flow_temlates:
            return Result.ok(data=[])

        users = self._user_dao.query_users_by_id_list(
            [t.creator for t in flow_temlates], True)

        return Result.ok(data=[
            FlowTemplateView.from_flow_template(tpl, users[tpl.creator])
            for tpl in flow_temlates
        ])

    def get_all_running_instance(self):
        """获取所有运行中的实例
        """

        all_running_instance = self._flow_instance_dao\
            .get_flow_instance_by_status(FlowStatus.STATUS_RUNNING)

        return self._build_instance_list_view(all_running_instance)

    @check(
        Field("begin_date", type_=datetime.date),
        Field("end_date", type_=datetime.date)
    )
    def get_instance_by_time_scope(self, begin_date, end_date):
        """根据时间范围来查询运行实例
           :param begin_date: 起始时间
           :param end_date: 结束时间
        """

        if begin_date > end_date:
            raise BadReq("invalid_time_scope")

        instance_list = self._flow_instance_dao.\
            get_flow_instance_by_created_date(
                begin_date,
                end_date + datetime.timedelta(days=1))

        return self._build_instance_list_view(instance_list)

    def _build_instance_list_view(self, instance_list):
        """从instance model列表构建instance视图对象
        """

        if not instance_list:
            return Result.ok(data=[])

        tpl_id_list = []
        creator_id_list = []
        instance_id_list = []
        for instance in instance_list:
            tpl_id_list.append(instance.flow_template_id)
            creator_id_list.append(instance.initiator)
            instance_id_list.append(instance.id)

        templates = self._flow_tpl_dao.query_by_id_list(
            tpl_id_list, True)
        creators = self._user_dao.query_users_by_id_list(
            creator_id_list, True)

        instance_group_ids = self._flow_instance_group_rlt_dao\
            .query_group_ids_by_instance_ids(instance_id_list)

        groups = self._flow_instance_group_dao\
            .query_by_id_list(list(instance_group_ids.values()), to_dict=True)

        def get_group(instance_id):
            group_id = instance_group_ids.get(instance_id)
            if not group_id:
                return None
            return groups[group_id]

        return Result.ok([
            FlowSimpleInstanceView.from_flow_instance(
                flow_instance=instance,
                group=get_group(instance.id),
                flow_template=templates[instance.flow_template_id],
                flow_meta_mgr=self._flow_meta_mgr,
                creator=creators[instance.initiator]
            ) for instance in instance_list])

    @check(
        IntField("flow_instance_id", required=True)
    )
    def get_flow_instance_details(self, flow_instance_id):
        """获取flow instance详情
        """

        flow_instance = self._flow_instance_dao\
            .query_by_instance_id(flow_instance_id)

        if flow_instance is None:
            raise BadReq("not_found", flow_instance_id=flow_instance_id)

        # get flow template
        flow_tpl = self._flow_tpl_dao.query_flow_template_by_id(
            flow_instance.flow_template_id)
        flow_tpl_view = FlowTemplateSimpleView.from_flow_template(
            flow_tpl,
            self._flow_meta_mgr
        )

        # get initiator info
        initiator_info = self._user_dao.query_user_by_id(
            flow_instance.initiator)

        # job instance list
        job_instance_list = self._job_instance_dao\
            .query_by_flow_instance_id(flow_instance_id)

        flow_discard_reason = None
        if flow_instance.status == FlowStatus.STATUS_DISCARD:
            flow_discard_reason = self._flow_discard_reason_dao\
                .query_by_flow_instance_id(flow_instance.id)

        return Result.ok(FlowInstanceDetailsView.from_flow_instance(
            flow_instance=flow_instance,
            flow_tpl_view=flow_tpl_view,
            initiator_info=initiator_info,
            job_instance_list=job_instance_list,
            flow_discard_reason=flow_discard_reason
        ))

    @check(
        IntField("group_id", required=True)
    )
    def get_flow_instance_group_details(self, group_id):
        """获取flow instance group 详情
           :param group_id flow instance group id
        """
        flow_instance_group = self._flow_instance_group_dao\
            .query_by_id(group_id)
        if flow_instance_group is None:
            raise BadReq("group_not_exist", group_id=group_id)

        sub_flow_instance_ids = self._flow_instance_group_rlt_dao\
            .query_instance_id_lst_by_group_id(group_id)

        if not sub_flow_instance_ids:
            return Result.ok(
                FlowInstanceGroupDetailsView
                .from_flow_instance_group(
                    flow_instance_group,
                    []
                ))

        flow_instances = self._flow_instance_dao\
            .query_by_instance_id_list(sub_flow_instance_ids)

        initiators = self._user_dao.query_users_by_id_list(
            id_list=[fi.initiator for fi in flow_instances],
            to_dict=True
        )

        flow_templates = self._flow_tpl_dao.query_by_id_list(
            tpl_id_list=[fi.flow_template_id for fi in flow_instances],
            to_dict=True
        )

        flow_instance_views = [
            FlowSimpleInstanceView.from_flow_instance(
                flow_instance=fi,
                group=flow_instance_group,
                flow_template=flow_templates[fi.flow_template_id],
                flow_meta_mgr=self._flow_meta_mgr,
                creator=initiators[fi.initiator]
            ) for fi in flow_instances
        ]

        return Result.ok(
            FlowInstanceGroupDetailsView
            .from_flow_instance_group(
                flow_instance_group,
                flow_instance_views
            ))

    @check(
        Field("begin_date", type_=datetime.date, required=True),
        Field("end_date", type_=datetime.date, required=True)
    )
    def get_flow_instance_group_history(self, begin_date, end_date):
        """
        根据时间范围来查询flow instance group运行历史
        :param begin_date: 起始日期
        :param end_date: 结束日期
        """
        if begin_date > end_date:
            raise BadReq("invalid_datescope")

        end_date += datetime.timedelta(days=1)

        groups = self._flow_instance_group_dao.query_by_datescope(
            begin_date=begin_date,
            end_date=end_date
        )

        if not groups:
            return Result.ok(data=[])

        group_id_list = [g.id for g in groups]

        g_f_relations = self._flow_instance_group_rlt_dao\
            .query_by_group_id_list(
                group_id_list=group_id_list
            )

        all_instance_ids = []
        for v in g_f_relations.values():
            all_instance_ids += v

        flow_instances = self._flow_instance_dao\
            .query_by_instance_id_list(all_instance_ids, to_dict=True)

        all_status_counter = defaultdict(Counter)
        for group_id, instance_ids in g_f_relations.items():
            for instance_id in instance_ids:
                flow_instance = flow_instances[instance_id]
                all_status_counter[group_id][flow_instance.status] += 1

        return Result.ok(data=[
            FlowInstanceGroupSimpleView.from_flow_instance_group(
                flow_instance_group=g,
                sub_flow_num=len(g_f_relations[g.id]),
                sub_flow_status=all_status_counter[g.id]
            ) for g in groups])
