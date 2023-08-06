from acolyte.core.job import JobStatus
from acolyte.testing.core.flow_executor_service import (
    AbstractFlowExecTestCase
)


class ActionBarrierTestCase(AbstractFlowExecTestCase):

    def setUp(self):
        super(ActionBarrierTestCase, self).setUp()

    def testActionBarrier(self):
        """测试action barrier的执行
        """

        # 开启一个新的flow instance
        rs = self._flow_exec.start_flow(
            flow_template_id=self._tpl_id,
            initiator=1,
            description="测试flow instance",
            start_flow_args={"x": 5, "y": 6}
        )

        flow_instance = rs.data
        self._flow_instance_id_collector.append(flow_instance.id)

        # 执行 trigger
        rs = self._flow_exec.handle_job_action(
            flow_instance_id=flow_instance.id,
            target_step="echo",
            target_action="trigger",
            actor=1,
            action_args={
            }
        )
        self.print_json(rs)

        # 执行a action
        rs = self._flow_exec.handle_job_action(
            flow_instance_id=flow_instance.id,
            target_step="echo",
            target_action="a",
            actor=1,
            action_args={
            }
        )
        self.print_json(rs)
        self.assertJobInstanceStatus(
            flow_instance.id, "echo", JobStatus.STATUS_RUNNING)

        # 执行b action
        rs = self._flow_exec.handle_job_action(
            flow_instance_id=flow_instance.id,
            target_step="echo",
            target_action="b",
            actor=1,
            action_args={
            }
        )
        self.print_json(rs)
        self.assertJobInstanceStatus(
            flow_instance.id, "echo", JobStatus.STATUS_RUNNING)

        # 执行c action
        rs = self._flow_exec.handle_job_action(
            flow_instance_id=flow_instance.id,
            target_step="echo",
            target_action="c",
            actor=1,
            action_args={
            }
        )
        self.print_json(rs)
        self.assertJobInstanceStatus(
            flow_instance.id, "echo", JobStatus.STATUS_FINISHED)

    def assertJobInstanceStatus(self, flow_instance_id, step_name, status):
        job_instance = self._job_instance_dao.\
            query_by_instance_id_and_step(flow_instance_id, step_name)
        self.assertEqual(job_instance.status, status)

    def tearDown(self):
        super(ActionBarrierTestCase, self).tearDown()
