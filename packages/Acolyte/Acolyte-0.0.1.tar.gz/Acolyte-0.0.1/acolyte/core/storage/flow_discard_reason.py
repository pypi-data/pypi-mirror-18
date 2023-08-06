import datetime
from acolyte.core.storage import AbstractDAO
from acolyte.core.flow import FlowDiscardReason


def _mapper(row):
    return FlowDiscardReason(**row)


class FlowDiscardReasonDAO(AbstractDAO):

    def __init__(self, db):
        super().__init__(db)

    def insert(self, flow_instance_id, actor, reason):
        return self._db.execute((
            "insert ignore into flow_discard_reason ("
            "flow_instance_id, actor, reason, discard_time) "
            "values (%s, %s, %s, %s)"
        ), (flow_instance_id, actor, reason, datetime.datetime.now()))

    def query_by_flow_instance_id(self, flow_instance_id):
        return self._db.query_one((
            "select * from flow_discard_reason where "
            "flow_instance_id = %s limit 1"
        ), (flow_instance_id, ), _mapper)

    def delete_by_flow_instance_id(self, flow_instance_id):
        return self._db.execute((
            "delete from flow_discard_reason where "
            "flow_instance_id = %s limit 1"
        ), (flow_instance_id, ))
