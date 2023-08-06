import functools
from typing import Iterable
from acolyte.util.mail import send_mail
from acolyte.util.validate import check, BadReq
from acolyte.core.notify import (
    NotifyReceiver,
    NotifyWay,
    NotifyTemplate,
    ReadStatus
)
from acolyte.core.view import NotifyDetailsView, NotifySimpleView
from acolyte.core.service import AbstractService, Result
from acolyte.core.storage.notify_index import NotifyIndexDAO


class NotifyLogic(AbstractService):

    def __init__(self, service_container):
        super().__init__(service_container)

        def _send_email(tpl, receiver):
            send_mail(
                receiver=receiver.receiver_user.email,
                subject=tpl.render_subject(**receiver.subject_template_args),
                content=tpl.render_content(**receiver.content_template_args)
            )

        self._send_methods = {
            NotifyWay.WEB_INBOX: None,
            NotifyWay.EMAIL: _send_email,
            NotifyWay.SMS: None,
            NotifyWay.WEIXIN: None
        }

    def _after_register(self):
        db = self._("db")
        self._notify_index_dao = NotifyIndexDAO(db)
        self._notify_executor = self._("notify_executor")
        self._notify_tpl_manager = self._("notify_tpl_manager")

    def notify(
            self, notify_template_name: str,
            notify_ways: Iterable[NotifyWay],
            *receivers: NotifyReceiver):

        tpl = self._notify_tpl_manager.get(notify_template_name)
        notify_function = functools.partial(
            self._notify, tpl_name=notify_template_name,
            tpl=tpl, notify_ways=notify_ways)

        def _batch_notify():
            for receiver in receivers:
                notify_function(receiver=receiver)

        self._notify_executor.submit(_batch_notify)

        return Result.ok()

    def _notify(self, tpl_name: str, tpl: NotifyTemplate,
                notify_ways: Iterable[NotifyWay], receiver: NotifyReceiver):
        """通知个体"""

        # 不管用什么方式，先插一条站内信
        self._notify_index_dao.insert(
            notify_template=tpl_name,
            notify_receiver=receiver,
            notify_ways=notify_ways
        )

        for notify_way in notify_ways:
            send_method = self._send_methods[notify_way]
            if send_method is None:
                continue
            send_method(tpl, receiver)

    @check()
    def view_notify_details(self, notify_index_id):
        notify_index = self._notify_index_dao.query_by_id(notify_index_id)
        if notify_index is None:
            raise BadReq("notify_index_not_found")

        # 如果未读则标记已读
        if notify_index.read_status == ReadStatus.unread:
            self._notify_index_dao.update_read_status(
                notify_index_id, ReadStatus.READED.value)

        return Result.ok(
            NotifyDetailsView.from_notify_index(
                notify_index, self._notify_tpl_manager))

    def mark_all_readed(self, receiver_id):
        """全部标记已读
        """
        self._notify_index_dao.update_read_status_by_receiver_id(
            receiver_id, ReadStatus.READED.value)
        return Result.ok()

    def get_unread_count(self, receiver_id):
        """获得未读消息数目
        """
        return self._notify_index_dao.query_unread_num(receiver_id)

    def get_all_unread(self, receiver_id):
        """获取所有的未读列表
        """
        unread_notify_index_lst = self._notify_index_dao\
            .query_unread(receiver_id)

        if not unread_notify_index_lst:
            return []

        return Result.ok(data=[
            NotifySimpleView.from_notify_index(
                notify_index, self._notify_tpl_manager
            ) for notify_index in unread_notify_index_lst])

    def view_history(self, receiver_id, offset_id, limit):
        """查看历史
        """
        notify_index_lst = self._notify_index_dao\
            .query_by_receiver_id(receiver_id, offset_id, limit)

        if not notify_index_lst:
            return Result.ok(data=[])

        return Result.ok(data=[
            NotifySimpleView.from_notify_index(
                notify_index, self._notify_tpl_manager
            ) for notify_index in notify_index_lst])
