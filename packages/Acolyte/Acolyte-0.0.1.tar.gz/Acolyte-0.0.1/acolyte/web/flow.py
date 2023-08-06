from collections import OrderedDict
import simplejson as json
from acolyte.web import (
    BaseWebHandler,
    check_token
)
from acolyte.core.service import Result
from acolyte.core.job import ActionArg


class FlowMetaHandler(BaseWebHandler):

    @check_token
    def get(self, flow_meta_name):
        """查询某个FlowMeta的详情
        """

        flow_service = self._("FlowService")

        rs = flow_service.get_flow_meta_info(flow_meta_name)

        if not rs.is_success():
            self.render("tip.html", msg=rs.msg)
            return

        flow_templates_rs = flow_service\
            .get_flow_templates_by_flow_meta_name(flow_meta_name)

        self.render(
            "flow_meta_details.html",
            flow_meta_name=flow_meta_name,
            flow_meta_details=rs.data,
            flow_templates=flow_templates_rs.data
        )


class ViewTemplateHandler(BaseWebHandler):

    @check_token
    def get(self, flow_template_id):
        """查询某个FlowTemplate的详情
        """

        flow_service = self._("FlowService")
        rs = flow_service.get_flow_template(flow_template_id)

        if not rs.is_success():
            self.render("tip.html", msg=rs.msg)
            return

        # 判断有无绑定参数
        bind_args = rs.data.bind_args
        action_num, empty_num = 0, 0
        for step_name in bind_args:
            for action in bind_args[step_name]:
                action_num += 1
                if not bind_args[step_name][action]:
                    empty_num += 1

        bind_args_json = json.dumps(
            bind_args, indent=4, ensure_ascii=False)
        config_json = json.dumps(
            rs.data.config, indent=4, ensure_ascii=False)

        return self.render(
            "flow_template_details.html",
            details=rs.data,
            bind_args_empty=action_num == empty_num,
            bind_args_json=bind_args_json,
            config_json=config_json
        )


class CreateTemplateHandler(BaseWebHandler):

    @check_token
    def get(self):
        """显示创建flow template页面
        """

        flow_meta_name = self.get_query_argument("meta")

        flow_service = self._("FlowService")

        rs = flow_service.get_flow_meta_info(flow_meta_name)

        if not rs.is_success():
            self.render("tip.html", msg=rs.msg)
            return

        flow_meta_details = rs.data

        return self.render(
            "create_flow_template.html",
            flow_meta_details=flow_meta_details,
            bind_args=self._render_bind_args_tpl(flow_meta_details)
        )

    def _render_bind_args_tpl(self, flow_meta_details):
        """渲染bind_args模板
        """

        job_mgr = self._("job_manager")

        bind_args = OrderedDict()

        for job_ref in flow_meta_details.jobs:
            job_name = job_ref.job_name
            job_define = job_mgr.get(job_name)
            bind_args[job_ref.step_name] = {
                action: self._render_act_args_tpl(job_define.job_args[action])
                for action in job_define.job_args}

        return bind_args

    def _render_act_args_tpl(self, action_args):
        return {
            a.name: {
                "type": a.field_info.type.__name__,
                "value": a.field_info.default,
                "mark": a.mark,
                "comment": a.comment
            } for a in action_args
            if a.mark != ActionArg.MARK_CONST
        }

    @check_token
    def post(self):
        """执行创建, 需要Ajax请求
        """

        (
            follow_meta_name,
            name,
            max_run_instance,
            config,
            bind_args

        ) = self._form(
            "flow_meta",
            "name",
            "max_run_instance",
            "config",
            "bind_args"
        )

        config = _parse_json(config)

        # config json解析失败
        if config is None:
            self._output_result(Result.bad_request(
                "invalid_config_fmt", msg="Config JSON格式有误"))
            return

        bind_args = _parse_json(bind_args)

        # bind_args json解析失败
        if bind_args is None:
            self._output_result(Result.bad_request(
                "invalid_bind_args_fmt", msg="Bind args JSON格式有误"))
            return

        rs = self._("FlowService").create_flow_template(
            flow_meta_name=follow_meta_name,
            name=name,
            bind_args=bind_args,
            max_run_instance=max_run_instance,
            config=config,
            creator=self.request.current_user.id
        )
        self._output_result(rs)


class ModifyTemplateHandler(BaseWebHandler):

    @check_token
    def post(self):
        """修改Flow template配置
        """

        (
            tpl_id,
            name,
            bind_args_json,
            max_run_instance,
            config_json
        ) = self._form(
            "tpl_id",
            "name",
            "bind_args",
            "max_run_instance",
            "config"
        )

        config = _parse_json(config_json)

        # config解析错误
        if config is None:
            self._output_result(Result.bad_request(
                "invalid_config_fmt", msg="Config JSON格式有误"))
            return

        bind_args = _parse_json(bind_args_json)

        # bind_args 解析错误
        if bind_args is None:
            self._output_result(Result.bad_request(
                "invalid_bind_args_fmt", msg="Bind args JSON格式有误"))
            return

        # 执行修改
        rs = self._("FlowService").modify_flow_template(
            flow_tpl_id=tpl_id,
            name=name,
            bind_args=bind_args,
            max_run_instance=max_run_instance,
            config=config
        )
        self._output_result(rs)


class ViewFlowInstanceHandler(BaseWebHandler):

    @check_token
    def get(self, flow_instance_id):
        """FlowInstance终端页
        """

        flow_service = self._("FlowService")
        job_mgr = self._("job_manager")

        rs = flow_service.get_flow_instance_details(flow_instance_id)
        if rs.is_success():
            flow_meta_info = flow_service.get_flow_meta_info(
                rs.data.flow_tpl.flow_meta_name).data
            jobs = {
                job_ref.job_name: job_mgr.get(job_ref.job_name)
                for job_ref in flow_meta_info.jobs
            }
            steps = {step.step_name: step for step in rs.data.steps}
            self.render(
                "flow_instance_details.html",
                details=rs.data,
                flow_meta_info=flow_meta_info,
                jobs=jobs,
                steps=steps
            )
        else:
            self.render("tip.html", msg=rs.msg)


def _parse_json(json_str):
    if not json_str:
        return {}
    else:
        try:
            return json.loads(json_str)
        except:
            return None


class DiscardFlowInstanceHandler(BaseWebHandler):

    @check_token
    def post(self):
        flow_exec_service = self._("FlowExecutorService")
        flow_instance_id, reason = self._form("flow_instance_id", "reason")
        actor_id = self.request.current_user.id
        rs = flow_exec_service.discard_flow_instance(
            int(flow_instance_id), actor_id, reason)
        self._output_result(rs)


class ViewFlowGroupDetailsHandler(BaseWebHandler):

    @check_token
    def get(self, group_id):
        flow_service = self._("FlowService")
        rs = flow_service\
            .get_flow_instance_group_details(group_id)
        self.render("flow_group_details.html", details=rs.data)
