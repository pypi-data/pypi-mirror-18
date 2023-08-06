import datetime
from functools import wraps
from acolyte.util.json import to_json
from tornado.web import RequestHandler


class BaseWebHandler(RequestHandler):

    def _(self, service_id):
        return BaseWebHandler.service_container.get_service(service_id)

    def _form(self, *field_names, strip=True):
        return [
            self.get_body_argument(field_name, "", strip=strip)
            for field_name in field_names
        ]

    def _query_args(self, *field_names, strip=True):
        return [
            self.get_query_argument(field_name, "", strip=strip)
            for field_name in field_names
        ]

    def _date_scope(self, prefix=""):
        (
            begin_year_str,
            begin_month_str,
            begin_day_str,
            end_year_str,
            end_month_str,
            end_day_str
        ) = self._query_args(
            "begin_year",
            "begin_month",
            "begin_day",
            "end_year",
            "end_month",
            "end_day"
        )
        return datetime.date(
            year=int(begin_year_str),
            month=int(begin_month_str),
            day=int(begin_day_str)
        ), datetime.date(
            year=int(end_year_str),
            month=int(end_month_str),
            day=int(end_day_str)
        )

    def _print_json(self, obj):
        """打印json，供调试使用
        """
        print(to_json(obj))

    def _output_result(self, rs):
        """将result对象按照json的格式输出
        """
        self.set_header('Content-Type', 'application/json')
        self.write(to_json(rs))
        self.finish()


class ReqUser:

    @classmethod
    def from_session_data(cls, session_data):
        return cls(
            id_=session_data["id"],
            email=session_data["session_data"]["email"],
            name=session_data["session_data"]["name"]
        )

    def __init__(self, id_, email, name):
        self._id = id_
        self._email = email
        self._name = name

    @property
    def id(self):
        return self._id

    @property
    def email(self):
        return self._email

    @property
    def name(self):
        return self._name


def check_token(func):

    @wraps(func)
    def _f(self, *args, **kwds):
        token = self.get_secure_cookie("_t")

        if token is None:
            self.redirect("/login?redirect={}".format(self.request.uri))
            return

        token = token.decode("utf-8")
        rs = self._("UserService").check_token(token)

        if rs.is_success():
            self.request._token = token
            self.request.current_user = ReqUser.from_session_data(rs.data)
            return func(self, *args, **kwds)
        else:
            self.redirect("/login?redirect={}".format(self.request.uri))
            return

    return _f
