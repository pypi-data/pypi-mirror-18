from acolyte.web import (
    BaseWebHandler,
    check_token
)
from acolyte.core.service import Result
from acolyte.core.storage.job_instance import JobInstanceDAO


class ViewJobDetailsHandler(BaseWebHandler):

    @check_token
    def get(self, job_name):

        job_service = self._("JobService")
        rs = job_service.get_job_details_by_name(job_name)

        if not rs.is_success():
            self.render("tip.html", msg=rs.msg)
            return

        return self.render(
            "job_details.html",
            details=rs.data
        )


class ViewJobInstanceDetailsHandler(BaseWebHandler):

    @check_token
    def get(self, job_instance_id, original=None):

        rs = self._("JobService")\
            .get_job_instance_details(job_instance_id)

        if not rs.is_success():
            self.render("tip.html", msg=rs.msg)
            return

        job_instance_details = rs.data
        job_mgr = self._("job_manager")
        job_define = job_mgr.get(job_instance_details.job_name)

        if job_define.ui is None or original == "original":
            self.render(
                "job_instance_details.html",
                details=job_instance_details,
                job_define=job_define
            )
        else:
            content = job_define.ui.render_instance_details_page(
                details=job_instance_details,
                job_define=job_define,
                request=self.request
            )
            self.render(
                "customize_job_instance_details.html",
                content=content
            )


class JobDecisionHandler(BaseWebHandler):

    @check_token
    def get(self, job_instance_id, decision_name):
        """渲染展示Decision页面
        """
        rs = self._("JobService").get_decision_info(
            job_instance_id, decision_name)

        if not rs.is_success():
            self.render("tip.html", msg=rs.msg)
            return

        self.render(
            "job_decision.html",
            details=rs.data,
            instance_id=job_instance_id
        )

    @check_token
    def post(self, job_instance_id, action):
        """执行选择的Action
        """

        job_instance_dao = JobInstanceDAO(self._("db"))
        job_instance = job_instance_dao.query_by_id(job_instance_id)

        if job_instance is None:
            self._output_result(
                Result.bad_request(
                    "job_instance_not_found",
                    msg="找不到指定的Job instance: {}".format(job_instance.id))
            )
            return

        action_args = {
            name: value_list[0].decode("utf-8")
            for name, value_list in self.request.arguments.items()}

        self._print_json(action_args)

        flow_executor_service = self._("FlowExecutorService")
        rs = flow_executor_service.handle_job_action(
            flow_instance_id=job_instance.flow_instance_id,
            target_step=job_instance.step_name,
            target_action=action,
            actor=self.request.current_user.id,
            action_args=action_args
        )

        self._print_json(rs)

        self._output_result(rs)
