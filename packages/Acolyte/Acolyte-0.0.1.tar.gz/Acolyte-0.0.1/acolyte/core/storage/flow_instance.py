import datetime
from acolyte.core.storage import AbstractDAO
from acolyte.core.flow import FlowInstance, FlowStatus


def _mapper(result):
    result["id_"] = result.pop("id")
    return FlowInstance(**result)


class FlowInstanceDAO(AbstractDAO):

    def __init__(self, db):
        super().__init__(db)

    def query_by_instance_id(self, instance_id):
        return self._db.query_one((
            "select * from flow_instance where id = %s limit 1"
        ), (instance_id,), _mapper)

    def query_by_instance_id_list(self, id_list, to_dict=False):
        if not id_list:
            return []

        holders = ",".join(("%s", ) * len(id_list))
        rs = self._db.query_all((
            "select * from flow_instance where "
            "id in ({holders}) order by id"
        ).format(holders=holders), id_list, _mapper)
        if to_dict:
            return {instance.id: instance for instance in rs}
        return rs

    def query_running_instance_num_by_tpl_id(self, tpl_id):
        return int(self._db.query_one_field((
            "select count(*) as c from flow_instance "
            "where flow_template_id = %s and "
            "status in ('running', 'init')"
        ), (tpl_id,)))

    def query_running_instance_list_by_tpl_id(self, tpl_id):
        return self._db.query_all((
            "select * from flow_instance "
            "where flow_template_id = %s and "
            "status = 'running'"
        ), (tpl_id,), _mapper)

    def insert(self, flow_template_id, initiator, description):
        now = datetime.datetime.now()
        with self._db.connection() as conn:
            with conn.cursor() as csr:
                csr.execute((
                    "insert into flow_instance ("
                    "flow_template_id, initiator, current_step, status, "
                    "description, created_on, updated_on) values ("
                    "%s, %s, %s, %s, %s, %s, %s)"
                ), (flow_template_id, initiator, "start",
                    FlowStatus.STATUS_INIT, description, now, now))
                conn.commit()
                return FlowInstance(
                    id_=csr.lastrowid,
                    flow_template_id=flow_template_id,
                    initiator=initiator,
                    current_step="start",
                    status=FlowStatus.STATUS_INIT,
                    description=description,
                    created_on=now,
                    updated_on=now
                )

    def update_status(self, flow_instance_id, status):
        now = datetime.datetime.now()
        return self._db.execute((
            "update flow_instance set status = %s, "
            "updated_on = %s where id = %s limit 1"
        ), (status, now, flow_instance_id))

    def update_current_step(self, flow_instance_id, current_step):
        now = datetime.datetime.now()
        return self._db.execute((
            "update flow_instance set current_step = %s, "
            "updated_on = %s where id = %s limit 1"
        ), (current_step, now, flow_instance_id))

    def delete_by_instance_id(self, instance_id):
        if isinstance(instance_id, list):
            holders = ",".join(("%s", ) * len(instance_id))
            return self._db.execute(
                "delete from flow_instance where id in ({holders})".format(
                    holders=holders), instance_id)
        else:
            return self._db.execute("delete from flow_instance where id = %s",
                                    (instance_id, ))

    def get_flow_instance_by_status(self, flow_status):
        return self._db.query_all((
            "select * from flow_instance where status = %s"
        ), (flow_status, ), _mapper)

    def get_flow_instance_by_created_date(self, begin_date, end_date):
        return self._db.query_all((
            "select * from flow_instance where "
            "created_on between %s and %s order by created_on desc"
        ), (begin_date, end_date), _mapper)
