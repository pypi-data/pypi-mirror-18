from acolyte.web import BaseWebHandler, check_token
from acolyte.core.storage.flow_template import FlowTemplateDAO


class IndexHandler(BaseWebHandler):

    @check_token
    def get(self):
        flow_service = self._("FlowService")
        flow_tpl_dao = FlowTemplateDAO(self._("db"))

        # get all flow meta
        all_flow_meta = flow_service.get_all_flow_meta().data

        # get all running instance
        running_instance_list = flow_service.get_all_running_instance()

        # get all templates
        all_templates = flow_tpl_dao.query_all_templates()

        self.render(
            "index.html",
            all_flow_meta=all_flow_meta,
            running_instance_list=running_instance_list.data,
            all_templates=all_templates
        )


class QueryFlowInstanceHandler(BaseWebHandler):

    @check_token
    def get(self):
        begin_date, end_date = self._date_scope()
        flow_service = self._("FlowService")
        self.render(
            "_ajax_pages/_flow_instance_list.html",
            rs=flow_service.get_instance_by_time_scope(
                begin_date, end_date)
        )
