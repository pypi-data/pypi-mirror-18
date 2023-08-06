import datetime
import simplejson as json
from acolyte.core.storage import AbstractDAO
from acolyte.core.notify import (
    NotifyIndex,
    ReadStatus,
    NotifyWay
)


_notify_ways = list(NotifyWay)
_read_status_list = list(ReadStatus)


def _mapper(row):
    return NotifyIndex(
        id_=row["id"],
        notify_template=row["notify_template"],
        receiver=row["receiver"],
        subject_template_args=json.loads(row["subject_template_args"]),
        content_template_args=json.loads(row["content_template_args"]),
        digest_template_args=json.loads(row["digest_template_args"]),
        notify_ways=json.loads(row["notify_ways"]),
        read_status=_read_status_list[row["read_status"]],
        updated_on=row["updated_on"],
        created_on=row["created_on"]
    )


class NotifyIndexDAO(AbstractDAO):

    def __init__(self, db):
        super().__init__(db)

    def insert(self, notify_template, notify_receiver, notify_ways):

        now = datetime.datetime.now()

        with self._db.connection() as conn:
            with conn.cursor() as csr:
                csr.execute((
                    "insert into notify_index(notify_template, receiver, "
                    "subject_template_args, content_template_args, "
                    "digest_template_args, notify_ways, read_status, "
                    "updated_on, created_on) values ("
                    "%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                ), (
                    notify_template,
                    notify_receiver.receiver_user.id,
                    json.dumps(notify_receiver.subject_template_args),
                    json.dumps(notify_receiver.content_template_args),
                    json.dumps(notify_receiver.digest_template_args),
                    json.dumps([way.value for way in notify_ways]),
                    ReadStatus.UNREAD.value,
                    now, now
                ))
                conn.commit()
                return NotifyIndex.from_notify_receiver(
                    id_=csr.lastrowid,
                    notify_template=notify_template,
                    notify_receiver=notify_receiver,
                    notify_ways=notify_ways
                )

    def query_by_id(self, id_):
        return self._db.query_one((
            "select * from notify_index where "
            "id = %s limit 1"
        ), (id_, ), _mapper)

    def query_unread(self, receiver_id):
        return self._db.query_all((
            "select * from notify_index where "
            "receiver = %s and read_status = %s "
            "order by created_on desc"
        ), (receiver_id, ReadStatus.UNREAD.value), _mapper)

    def query_unread_num(self, receiver_id):
        return self._db.query_one_field((
            "select count(*) from notify_index "
            "where receiver = %s and read_status = %s"
        ), (receiver_id, ReadStatus.UNREAD.value))

    def query_by_receiver_id(self, receiver_id, offset_id, limit):
        return self._db.query_all((
            "select * from notify_index where "
            "receiver = %s where id < %s order by id desc "
            "limit %s"
        ), (receiver_id, offset_id, limit), _mapper)

    def update_read_status(self, id_, read_status):
        now = datetime.datetime.now()
        return self._db.execute((
            "update notify_index set read_status = %s, "
            "updated_on = %s "
            "where id = %s limit 1"
        ), (read_status, now, id_))

    def update_read_status_by_receiver_id(self, receiver_id, read_status):
        now = datetime.datetime.now()
        return self._db.execute((
            "update notify_index set read_status = %s, "
            "updated_on = %s "
            "where receiver = %s"
        ), (read_status, now, receiver_id))
