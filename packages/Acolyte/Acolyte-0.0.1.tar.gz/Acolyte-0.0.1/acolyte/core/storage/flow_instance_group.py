import datetime
from collections import defaultdict
from acolyte.util.json import to_json
from acolyte.core.storage import AbstractDAO
from acolyte.core.flow import FlowInstanceGroup


def _mapper(row):
    row["id_"] = row.pop("id")
    return FlowInstanceGroup(**row)


class FlowInstanceGroupDAO(AbstractDAO):

    def __init__(self, db):
        super().__init__(db)

    def insert(self, name, description, meta, status):
        now = datetime.datetime.now()
        with self._db.connection() as conn:
            with conn.cursor() as csr:
                csr.execute((
                    "insert into flow_instance_group "
                    "(name, `description`, `meta`, status, "
                    "created_on, updated_on) values ("
                    "%s, %s, %s, %s, %s, %s)"
                ), (name, description, to_json(meta), status, now, now))
                conn.commit()
                return FlowInstanceGroup(
                    id_=csr.lastrowid,
                    name=name,
                    description=description,
                    meta=meta,
                    status=status,
                    created_on=now,
                    updated_on=now
                )

    def query_by_id(self, id_):
        return self._db.query_one((
            "select * from flow_instance_group where "
            "id = %s limit 1"
        ), (id_, ), _mapper)

    def query_by_id_list(self, id_list, to_dict=False):
        if not id_list:
            return {} if to_dict else []
        holders = ",".join(("%s", ) * len(id_list))
        rs = self._db.query_all((
            "select * from flow_instance_group where "
            "id in ({holders})"
        ).format(holders=holders), id_list, _mapper)
        if to_dict:
            return {g.id: g for g in rs}
        return rs

    def query_by_name(self, name):
        return self._db.query_one((
            "select * from flow_instance_group where "
            "name = %s limit 1"
        ), (name, ), _mapper)

    def query_by_datescope(self, begin_date, end_date):
        return self._db.query_all((
            "select * from flow_instance_group where "
            "created_on between %s and %s"
        ), (begin_date, end_date), _mapper)

    def update_status(self, id_, status):
        now = datetime.datetime.now()
        return self._db.execute((
            "update flow_instance_group set status = %s, "
            "updated_on = %s "
            "where id = %s limit 1"
        ), (status, now, id_))

    def delete(self, id_):
        return self._db.execute((
            "delete from flow_instance_group "
            "where id = %s limit 1"
        ), (id_, ))

    def query_all(self):
        return self._db.query_all((
            "select * from flow_instance_group"
        ), tuple(), _mapper)


class FlowInstanceGroupRelationDAO(AbstractDAO):

    def __init__(self, db):
        super().__init__(db)

    def insert(self, flow_instance_id, group_id):
        now = datetime.datetime.now()
        with self._db.connection() as conn:
            with conn.cursor() as csr:
                csr.execute((
                    "insert ignore into flow_instance_group_relation "
                    "(flow_instance_id, group_id, created_on) "
                    "values (%s, %s, %s)"
                ), (flow_instance_id, group_id, now))
                conn.commit()

    def is_in_group(self, flow_instance_id, group_id):
        return self._db.query_one_field((
            "select id from flow_instance_group_relation where "
            "flow_instance_id = %s and group_id = %s"
        ), (flow_instance_id, group_id))

    def query_group_id_by_instance_id(self, flow_instance_id):
        return self._db.query_one_field((
            "select group_id from flow_instance_group_relation "
            "where flow_instance_id = %s"
        ), (flow_instance_id, ))

    def query_instance_id_lst_by_group_id(self, group_id):
        rs = self._db.query_all((
            "select flow_instance_id from "
            "flow_instance_group_relation where "
            "group_id = %s"
        ), (group_id,))
        if not rs:
            return []
        return [row["flow_instance_id"] for row in rs]

    def query_by_group_id_list(self, group_id_list):
        if not group_id_list:
            return {}

        holders = ",".join(("%s", ) * len(group_id_list))

        rs = self._db.query_all((
            "select flow_instance_id, group_id from "
            "flow_instance_group_relation where "
            "group_id in ({holders})"
        ).format(holders=holders), group_id_list)

        if not rs:
            return {}

        groupby_rs = defaultdict(list)

        for row in rs:
            groupby_rs[row["group_id"]].append(row["flow_instance_id"])

        return groupby_rs

    def query_group_ids_by_instance_ids(self, instance_ids):
        if not instance_ids:
            return {}
        holders = ",".join(("%s", ) * len(instance_ids))
        rs = self._db.query_all((
            "select group_id, flow_instance_id from "
            "flow_instance_group_relation where "
            "flow_instance_id in ({holders})"
        ).format(holders=holders), instance_ids)
        return {r["flow_instance_id"]: r["group_id"] for r in rs}

    def delete_by_group_id(self, group_id):
        return self._db.execute((
            "delete from flow_instance_group_relation "
            "where group_id = %s"
        ), (group_id, ))
