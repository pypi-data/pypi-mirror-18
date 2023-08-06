import datetime
from typing import Dict, List, Any
from enum import Enum


class NotifyWay(Enum):

    """通知方式"""

    WEB_INBOX = 1  # 站内通知

    EMAIL = 2  # 邮件通知

    SMS = 3  # 短信通知

    WEIXIN = 4  # 微信通知


class NotifyTemplate:

    """通知模板
    """

    def __init__(self, name, subject_template, content_template,
                 digest_template):
        """通知模板
        """

        self._name = name
        self._subject_template = subject_template
        self._content_template = content_template
        self._digest_template = digest_template

    @property
    def name(self):
        return self._name

    @property
    def subject_template(self):
        return self._subject_template

    @property
    def content_template(self):
        return self._content_template

    @property
    def digest_template(self):
        return self._digest_template

    def render_subject(self, **subject_args):
        return self._subject_template.format(**subject_args)

    def render_digest(self, **digest_args):
        return self._digest_template.format(**digest_args)

    def render_content(self, **content_args):
        return self._content_template.format(**content_args)


class Jinja2NotifyTemplate(NotifyTemplate):

    """基于jinja2的通知模板
    """

    def __init__(self,
                 name, subject_template, content_template,
                 digest_template, jinja2_env):
        super().__init__(
            name=name,
            subject_template=subject_template,
            content_template=content_template,
            digest_template=digest_template
        )
        self._jinja2_env = jinja2_env

    def render_subject(self, **subject_args):
        return self._render(self._subject_template, **subject_args)

    def render_digest(self, **digest_args):
        return self._render(self._digest_template, **digest_args)

    def render_content(self, **content_args):
        return self._render(self._content_template, **content_args)

    def _render(self, tpl, **args):
        if tpl.startswith("tpl:"):
            return self._render_with_jinja2(tpl[len("tpl:"):], **args)
        else:
            return self._render_with_format(tpl, **args)

    def _render_with_format(self, tpl, **args):
        return tpl.format(**args)

    def _render_with_jinja2(self, tpl, **args):
        tpl = self._jinja2_env.get_template(tpl)
        return tpl.render(**args)


class ReadStatus(Enum):

    """通知阅读状态"""

    UNREAD = 0  # 未读状态
    READED = 1  # 已读状态


class NotifyReceiver:

    """用于通知发送接口，表示收件人
    """

    def __init__(self, receiver_user, subject_template_args,
                 content_template_args, digest_template_args):
        self._receiver_user = receiver_user
        self._subject_template_args = subject_template_args
        self._content_template_args = content_template_args
        self._digest_template_args = digest_template_args

    @property
    def receiver_user(self):
        return self._receiver_user

    @property
    def subject_template_args(self):
        return self._subject_template_args

    @property
    def content_template_args(self):
        return self._content_template_args

    @property
    def digest_template_args(self):
        return self._digest_template_args


class NotifyIndex:

    """通知分发索引
    """

    @classmethod
    def from_notify_receiver(
            cls, id_, notify_template, notify_receiver, notify_ways):
        return cls(
            id_=id_,
            notify_template=notify_template,
            receiver=notify_receiver._receiver_user.id,
            subject_template_args=notify_receiver.subject_template_args,
            content_template_args=notify_receiver.content_template_args,
            digest_template_args=notify_receiver.digest_template_args,
            notify_ways=notify_ways
        )

    def __init__(self, id_: int, notify_template: str, receiver: int,
                 subject_template_args: Dict[str, Any],
                 content_template_args: Dict[str, Any],
                 digest_template_args: Dict[str, Any],
                 notify_ways: List[NotifyWay]=None,
                 read_status: ReadStatus=ReadStatus.UNREAD,
                 created_on=None, updated_on=None):
        """
        :param notify_template: 所引用的模板名称
        :param receiver: 收件人
        :param subject_template_args: 渲染标题所需要的参数
        :param content_template_args: 渲染正文所需要的参数
        :param digest_template_args: 渲染摘要所需要的参数
        :param notify_ways: 通知方式
        :param read_status: 阅读状态
        :param created_on: 创建时间
        :param updated_on: 更新时间
        """

        self._id = id_
        self._notify_template = notify_template
        self._receiver = receiver
        self._subject_template_args = subject_template_args
        self._content_template_args = content_template_args
        self._digest_template_args = digest_template_args
        self._notify_ways = notify_ways if notify_ways else []
        self._read_status = read_status
        now = datetime.datetime.now()
        self._created_on = created_on if created_on else now
        self._updated_on = updated_on if updated_on else now

    @property
    def id(self):
        return self._id

    @property
    def notify_template(self):
        return self._notify_template

    @property
    def receiver(self):
        return self._receiver

    @property
    def subject_template_args(self):
        return self._subject_template_args

    @property
    def content_template_args(self):
        return self._content_template_args

    @property
    def digest_template_args(self):
        return self._digest_template_args

    @property
    def notify_ways(self):
        return self._notify_ways

    @property
    def read_status(self):
        return self._read_status

    @property
    def created_on(self):
        return self._created_on

    @property
    def updated_on(self):
        return self._updated_on
