from acolyte.testing.core.flow_executor_service import (
    AbstractFlowExecTestCase
)


class RunTimeConstraintTestCase(AbstractFlowExecTestCase):

    def setUp(self):
        super().setUp()

    def testRunTimeContraint(self):
        # 重复执行action
        rs = self._flow_exec.start_flow(
            flow_template_id=self._tpl_id,
            initiator=1,
            description="hehehe",
            start_flow_args={
                "x": 5, "y": 6
            },
            group=0
        )
        self.assertResultSuccess(rs)
        self.assertTrue(rs.data.id > 0)
        flow_instance_id = rs.data.id
        self._flow_instance_id_collector.append(rs.data.id)

        rs = self._flow_exec.handle_job_action(
            flow_instance_id=flow_instance_id,
            target_step="echo",
            target_action="trigger",
            actor=1,
            action_args={}
        )
        self.print_json(rs)
        self.assertResultSuccess(rs)
        self.assertEqual(rs.data, 7)

        for _ in range(5):
            rs = self._flow_exec.handle_job_action(
                flow_instance_id=flow_instance_id,
                target_step="echo",
                target_action="repeat",
                actor=1,
                action_args={}
            )
            self.print_json(rs)
            self.assertResultSuccess(rs)

    def tearDown(self):
        super().tearDown()
