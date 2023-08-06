"""本模块包含跟Job相关的Facade接口
"""
from acolyte.util.validate import (
    check,
    StrField,
    IntField,
    BadReq,
)
from acolyte.core.service import (
    Result,
    AbstractService
)
from acolyte.core.storage.job_instance import JobInstanceDAO
from acolyte.core.storage.job_action_data import JobActionDataDAO
from acolyte.core.storage.user import UserDAO
from acolyte.core.view import (
    JobDetailsView,
    JobInstanceDetailsView,
    DecisionView,
)
from acolyte.exception import ObjectNotFoundException


class JobService(AbstractService):

    def __init__(self, service_container):
        super().__init__(service_container)
        self._job_mgr = self._("job_manager")
        self._db = self._("db")
        self._job_instance_dao = JobInstanceDAO(self._db)
        self._job_action_data_dao = JobActionDataDAO(self._db)
        self._user_dao = UserDAO(self._db)

    @check(
        StrField("job_name", required=True)
    )
    def get_job_details_by_name(self, job_name):
        """根据job名称来获取job定义详情
        """
        try:
            job_define = self._job_mgr.get(job_name)
        except ObjectNotFoundException:
            raise BadReq("job_not_found", job_name=job_name)
        return Result.ok(data=JobDetailsView.from_job(job_define))

    def get_all_job_definations(self):
        """获取所有的Job定义
        """
        ...

    def get_job_instance_list_by_flow_instance(self, flow_instance_id):
        """根据flow_instance_id获取job_instance列表
        """
        ...

    @check(
        IntField("job_instance_id", required=True),
    )
    def get_job_instance_details(self, job_instance_id):
        """获取某个job_instance的详情数据，包括每个其中每个event的数据
        """

        job_instance = self._job_instance_dao.query_by_id(
            job_instance_id)

        if job_instance is None:
            raise BadReq(
                "instance_not_found", job_instance_id=job_instance.id)

        action_data_list = self._job_action_data_dao\
            .query_by_instance_id(job_instance.id)

        actor_id_list = [action_data.actor for action_data in action_data_list]
        actors = self._user_dao.query_users_by_id_list(actor_id_list, True)

        return Result.ok(data=JobInstanceDetailsView.from_job_instance(
            job_instance, action_data_list, actors))

    @check(
        IntField("job_instance_id", required=True),
        StrField("decision_name", required=True)
    )
    def get_decision_info(self, job_instance_id, decision_name):
        """获取Job的某个Decison摘要
        """

        job_instance = self._job_instance_dao.query_by_id(job_instance_id)
        if job_instance is None:
            raise BadReq("job_instance_not_found",
                         job_instance_id=job_instance_id)

        job_define = self._job_mgr.get(job_instance.job_name)
        decision_define = job_define.get_decision(decision_name)
        if decision_define is None:
            raise BadReq("decision_not_found", decision_name=decision_name)

        return Result.ok(DecisionView.from_decision_define(
            decision_define, job_define))
