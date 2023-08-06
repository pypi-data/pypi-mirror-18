import types
import smtplib
from email import encoders
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Attachment:

    """Attachment对象用来描述一个邮件附件
    """

    def __init__(self, filepath, mime_type, attachment_filename):
        """
        :param filepath: 附件所引用的具体文件路径
        :param mime_type: 附件的mime类型
        :param attachment_filename: 展示为附件时的文件名称
        """
        self.filepath = filepath
        self.mime_type = mime_type
        self.attachment_filename = attachment_filename

    def build_mime_object(self):
        """构建Mime对象"""
        mime_type = self._mime_type.split("/")
        mime = MIMEBase(mime_type[0], mime_type[1])
        mime.set_payload(self._gen_payload())
        encoders.encode_base64(mime)
        mime.add_header(
            'Content-Disposition',
            'attachment; filename="{}"'.format(self._attachment_filename))
        return mime

    def _gen_payload(self):
        # 文件类型的情况
        if isinstance(self._attachment_file, types.FileType):
            try:
                return self._attachment_file.read()
            finally:
                self._attachment_file.close()
        # 字符串路径的情况
        elif isinstance(self._attachment_file, types.StringTypes):
            with open(self._attachment_file, "r") as f:
                return f.read()
        # StringIO or cStringIO
        else:
            self._attachment_file.seek(0)
            return self._attachment_file.read()


def send_mail(receiver, subject, content,
              encoding="utf-8", attachments=None):
    """调用该函数可以发送邮件
       :param receiver: 收件人
       :param sender: 发件人
       :param subject: 主题
       :param content: 邮件正文
       :param encoding: 编码
       :param attachments: 附件列表
    """

    global _smtp_config

    smtp_server = smtplib.SMTP(
        host=_smtp_config.host,
        port=_smtp_config.port
    )
    smtp_server.login(_smtp_config.account, _smtp_config.password)

    try:
        msg = MIMEMultipart()
        msg['From'] = _smtp_config.sender
        msg['To'] = receiver
        msg['Subject'] = Header(subject, encoding)
        msg.attach(MIMEText(content, "html", encoding))
        if attachments:
            for attachment in attachments:
                msg.attach(attachment.build_mime_object())
        smtp_server.sendmail(
            _smtp_config.sender,
            [email_address.strip() for email_address in receiver.split(",")],
            msg.as_string()
        )
    finally:
        smtp_server.quit()


class SMTPConfig:

    """SMTP服务配置
    """

    def __init__(self, host, port, account, password, sender, ssl=False):
        self._host = host
        self._port = port
        self._account = account
        self._password = password
        self._sender = sender
        self._ssl = ssl

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port

    @property
    def account(self):
        return self._account

    @property
    def password(self):
        return self._password

    @property
    def sender(self):
        return self._sender


def load_smtp_config(config):
    """加载smtp的相关配置
    """
    global _smtp_config
    _smtp_config = SMTPConfig(**config["smtp"])
