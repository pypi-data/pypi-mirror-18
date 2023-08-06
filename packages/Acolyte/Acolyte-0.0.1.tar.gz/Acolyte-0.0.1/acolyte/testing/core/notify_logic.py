from acolyte.testing import EasemobFlowTestCase
from acolyte.core.notify import (
    NotifyWay,
    NotifyReceiver
)
from acolyte.core.storage.user import UserDAO


class NotifyLogicTestCase(EasemobFlowTestCase):

    def setUp(self):
        self._notify_logic = self._("NotifyLogic")
        self._user_dao = UserDAO(self._("db"))
        self._user = self._user_dao.query_user_by_id(1)

    def testNotify(self):
        test_subject_args = {"name": "Sam"}
        test_content_args = {"name": "Sam"}
        test_digest_args = {"name": "Sam"}
        self._notify_logic.notify(
            "test", [NotifyWay.WEB_INBOX, NotifyWay.EMAIL],
            NotifyReceiver(
                self._user,
                test_subject_args, test_content_args, test_digest_args))
