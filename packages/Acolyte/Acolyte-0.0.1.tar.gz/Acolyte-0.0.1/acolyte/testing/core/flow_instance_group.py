import datetime
import acolyte.testing.core.flow_executor_service as fes
from acolyte.core.storage.flow_instance_group import (
    FlowInstanceGroupDAO,
    FlowInstanceGroupRelationDAO
)


class FlowInstanceGroupTestCase(fes.AbstractFlowExecTestCase):

    def setUp(self):
        super(FlowInstanceGroupTestCase, self).setUp()
        self._group_id_collector = []
        self._flow_instance_group_dao = FlowInstanceGroupDAO(self._db)
        self._flow_instance_group_rlt_dao = FlowInstanceGroupRelationDAO(
            self._db)
        # 创建一个flow template供测试使用
        bind_args = {
            "echo": {
                "trigger": {
                    "b": "$config.b"
                },
                "multiply": {
                    "c": 3
                },
                "minus": {
                    "d": 11,
                    "e": 12
                }
            }
        }
        rs = self._flow_service.create_flow_template(
            flow_meta_name="test_flow",
            name="sam_test_x",
            bind_args=bind_args,
            max_run_instance=0,
            config={"dev_email": "chihongze@gmail.com", "b": 2},
            creator=1
        )
        self._tpl_id = rs.data.id
        self._flow_tpl_id_collector.append(self._tpl_id)

    def testGroupOperation(self):
        """测试flow instance group的相关操作
        """

        begin_date = datetime.date.today()

        # 创建 flow instance group
        rs = self._flow_exec.create_flow_instance_group(
            name="rest_v1.4.2",
            description="rest v1.4.2 更新",
            meta={}
        )
        self.assertResultSuccess(rs)
        self._group_id_collector.append(rs.data.id)
        group_id = rs.data.id

        # 创建同名的 flow instance group
        rs = self._flow_exec.create_flow_instance_group(
            name="rest_v1.4.2",
            description="rest v1.4.2 更新",
            meta={}
        )
        self.assertResultBadRequest(rs, "group_existed")

        # 创建隶属该组的flow instance
        instance_id_lst = []
        for _ in range(5):
            rs = self._flow_exec.start_flow(
                flow_template_id=self._tpl_id,
                initiator=1,
                description="hehehe",
                start_flow_args={
                    "x": 5, "y": 6
                },
                group=group_id
            )
            self.assertResultSuccess(rs)
            flow_instance_id = rs.data.id
            instance_id_lst.append(flow_instance_id)
            self._flow_instance_id_collector.append(flow_instance_id)
            self.assertTrue(self._flow_instance_group_rlt_dao
                            .is_in_group(flow_instance_id, group_id))

        # 丢弃一个instance
        self._flow_exec.discard_flow_instance(
            flow_instance_id=instance_id_lst[0],
            actor_id=1,
            discard_reason="呵呵"
        )

        # 测试视图查看

        # 查看某group详情
        rs = self._flow_service.get_flow_instance_group_details(group_id)
        self.print_json(rs)
        self.assertResultSuccess(rs)

        # 查看group历史
        end_date = begin_date
        rs = self._flow_service.get_flow_instance_group_history(
            begin_date, end_date)

        self.print_json(rs)
        self.assertResultSuccess(rs)
        group_status = rs.data[0].sub_flow_status
        self.assertEqual(group_status["running"], 4)
        self.assertEqual(group_status["discard"], 1)

    def tearDown(self):
        super(FlowInstanceGroupTestCase, self).tearDown()
        for group_id in self._group_id_collector:
            self._flow_instance_group_dao.delete(group_id)
            self._flow_instance_group_rlt_dao.delete_by_group_id(group_id)
