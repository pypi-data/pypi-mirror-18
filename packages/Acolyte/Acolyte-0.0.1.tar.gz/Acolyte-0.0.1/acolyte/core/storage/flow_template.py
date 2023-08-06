import simplejson as json
from acolyte.core.flow import FlowTemplate
from acolyte.core.storage import AbstractDAO


def _mapper(result):
    return FlowTemplate(
        id_=result["id"],
        flow_meta=result["flow_meta"],
        name=result["name"],
        bind_args=json.loads(result["bind_args"]),
        max_run_instance=result["max_run_instance"],
        config=json.loads(result["config"]),
        creator=result["creator"],
        created_on=result["created_on"]
    )


class FlowTemplateDAO(AbstractDAO):

    """针对flow_template表的操作
    """

    def __init__(self, db):
        super().__init__(db)

    def query_flow_template_by_id(self, template_id):
        global _mapper
        return self._db.query_one((
            "select * from flow_template where id = %s"
        ), (template_id,), _mapper)

    def query_flow_template_by_name(self, tpl_name):
        global _mapper
        return self._db.query_one((
            "select * from flow_template where name = %s"
        ), (tpl_name,), _mapper)

    def insert_flow_template(self, flow_meta, name, bind_args,
                             max_run_instance, config, creator, created_on):
        with self._db.connection() as conn:
            with conn.cursor() as csr:
                csr.execute((
                    "insert into `flow_template` "
                    "(flow_meta, name, bind_args, max_run_instance, "
                    "config, creator, created_on) values ("
                    "%s, %s, %s, %s, %s, %s, %s)"
                ), (flow_meta, name, json.dumps(bind_args), max_run_instance,
                    json.dumps(config), creator, created_on))
                conn.commit()
                return FlowTemplate(
                    id_=csr.lastrowid,
                    flow_meta=flow_meta,
                    name=name,
                    bind_args=bind_args,
                    max_run_instance=max_run_instance,
                    config=config,
                    creator=creator,
                    created_on=created_on
                )

    def update_flow_template(self, flow_tpl_id, name,
                             bind_args, max_run_instance, config):
        return self._db.execute((
            "update flow_template set name = %s, bind_args = %s, "
            "max_run_instance = %s, config = %s where id = %s limit 1"
        ), (name, json.dumps(bind_args), max_run_instance, json.dumps(config),
            flow_tpl_id))

    def is_name_existed(self, name):
        return self._db.execute((
            "select id from flow_template where name = %s limit 1"
        ), (name,))

    def delete_by_id(self, tpl_id):
        if isinstance(tpl_id, list):
            holders = ",".join(("%s", ) * len(tpl_id))
            return self._db.execute((
                "delete from flow_template where id in ({holders})"
            ).format(holders=holders), tpl_id)
        else:
            return self._db.execute((
                "delete from flow_template where id = %s"
            ), (tpl_id,))

    def query_all_templates(self):
        return self._db.query_all((
            "select * from flow_template"
        ), tuple(), _mapper)

    def query_by_flow_meta_name(self, flow_meta_name):
        return self._db.query_all((
            "select * from flow_template where "
            "flow_meta = %s"
        ), (flow_meta_name, ), _mapper)

    def query_by_id_list(self, tpl_id_list, to_dict=False):
        if not tpl_id_list:
            return [] if not to_dict else {}
        holders = ",".join(("%s", ) * len(tpl_id_list))
        rs = self._db.query_all((
            "select * from flow_template where id in ({holders})"
        ).format(holders=holders), tpl_id_list, _mapper)
        if to_dict:
            return {t.id: t for t in rs}
        return rs
