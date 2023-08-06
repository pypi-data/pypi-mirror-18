from acolyte.testing import EasemobFlowTestCase
from acolyte.util.mail import send_mail


class SendMailTest(EasemobFlowTestCase):

    def testSend(self):
        send_mail("hongze.chi@gmail.com", "来自Acolyte的邮件", "Hello World")
