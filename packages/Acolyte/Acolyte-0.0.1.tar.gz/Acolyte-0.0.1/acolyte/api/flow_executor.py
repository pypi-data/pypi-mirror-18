from acolyte.api import BaseAPIHandler
from acolyte.core.service import Result
from acolyte.core.storage.flow_template import FlowTemplateDAO
from acolyte.core.storage.flow_instance import FlowInstanceDAO


handlers = [

    # start a flow instance
    {
        "url": r"/v1/flow/template/(\d+)/start",
        "http_method": "post",
        "service": "FlowExecutorService",
        "method": "start_flow",
        "path_variables": [
            "flow_template_id"
        ],
        "body_variables": {
            "description": "description",
            "start_flow_args": "start_flow_args",
            "group": "group"
        },
        "context_variables": {
            "current_user_id": "initiator"
        }
    },

    # run an action of the job
    {
        "url": r"/v1/flow/instance/(\d+)/([\w_]+)/([\w_]+)",
        "http_method": "post",
        "service": "FlowExecutorService",
        "method": "handle_job_action",
        "path_variables": [
            "flow_instance_id",
            "target_step",
            "target_action"
        ],
        "body_variables": {
            "action_args": "action_args"
        },
        "context_variables": {
            "current_user_id": "actor"
        }
    },

    # create a flow group
    {
        "url": r"/v1/flow/group/create",
        "http_method": "post",
        "service": "FlowExecutorService",
        "method": "create_flow_instance_group",
        "body_variables": {
            "name": "name",
            "description": "description",
            "meta": "meta"
        }
    }

]


class StartFlowByTplNameHandler(BaseAPIHandler):

    def post(self, tpl_name):

        check_token_rs = self._check_token()
        if not check_token_rs.is_success():
            self._output_result(check_token_rs)
            return

        flow_tpl_dao = FlowTemplateDAO(self._("db"))
        flow_template = flow_tpl_dao.query_flow_template_by_name(tpl_name)
        if flow_template is None:
            self._output_result(
                Result.bad_request(
                    "unknow_template",
                    msg="找不到名称为'{tpl_name}'的flow template".format(
                        tpl_name=tpl_name)))
            return

        body = self.json_body()
        initiator = body.get("initiator")
        # Body传递过来的initiator优先
        initiator = initiator or check_token_rs.data["id"]

        rs = self._("FlowExecutorService").start_flow(
            flow_template_id=flow_template.id,
            description=body.get("description", ""),
            start_flow_args=body.get("start_flow_args", ""),
            initiator=initiator
        )
        self._output_result(rs)


class RunActionByTplNameHandler(BaseAPIHandler):

    def post(self, tpl_name, target_step, target_action):

        check_token_rs = self._check_token()
        if not check_token_rs.is_success():
            self._output_result(check_token_rs)
            return

        flow_tpl_dao = FlowTemplateDAO(self._("db"))
        flow_instance_dao = FlowInstanceDAO(self._("db"))
        flow_template = flow_tpl_dao.query_flow_template_by_name(tpl_name)
        if flow_template is None:
            self._output_result(
                Result.bad_request(
                    "unknow_template",
                    msg="找不到名称为'{tpl_name}'的flow template".format(
                        tpl_name=tpl_name)))
            return

        running_instance_list = flow_instance_dao\
            .query_running_instance_list_by_tpl_id(flow_template.id)
        if not running_instance_list:
            self._output_result(Result.bad_request(
                "no_running_instance",
                msg="'{tpl_name}'下没有任何正在执行的实例".format(tpl_name=tpl_name)))
            return
        elif len(running_instance_list) > 1:
            self._output_result(Result.bad_request(
                "more_than_one",
                msg="'{tpl_name}'下有不止1个实例正在执行".format(tpl_name=tpl_name)
            ))
            return

        running_instance = running_instance_list.pop()
        body = self.json_body()

        rs = self._("FlowExecutorService").handle_job_action(
            flow_instance_id=running_instance.id,
            target_step=target_step,
            target_action=target_action,
            action_args=body.get("action_args", {}),
            actor=check_token_rs.data["id"]
        )
        self._output_result(rs)
