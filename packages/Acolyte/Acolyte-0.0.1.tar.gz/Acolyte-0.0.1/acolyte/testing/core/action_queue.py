from acolyte.testing.core.flow_executor_service import (
    AbstractFlowExecTestCase
)


class MySQLActionQueueTestCase(AbstractFlowExecTestCase):

    def setUp(self):
        super(MySQLActionQueueTestCase, self).setUp()

    def testActionQueue(self):

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

        # 执行 queue init action
        rs = self._flow_exec.handle_job_action(
            flow_instance_id=flow_instance.id,
            target_step="echo",
            target_action="queue_init",
            actor=1,
            action_args={}
        )
        self.assertResultSuccess(rs)

        for task_id in range(1, 6):
            self._flow_exec.handle_job_action(
                flow_instance_id=flow_instance.id,
                target_step="echo",
                target_action="ack",
                actor=1,
                action_args={
                    "task_id": task_id
                }
            )

    def tearDown(self):
        super(MySQLActionQueueTestCase, self).tearDown()
        self._db.execute("truncate `job_action_queue`", args=tuple())
