from acolyte.web import BaseWebHandler, check_token


class UserLoginHandler(BaseWebHandler):

    def get(self):
        self._if_logined_then_go_home()
        redirect, = self._query_args("redirect")
        self.render("login.html", redirect=redirect)

    def post(self):
        self._if_logined_then_go_home()
        account, password, redirect = self._form(
            "account", "password", "redirect")
        rs = self._("UserService").login(account, password)
        if rs.is_success():
            self.set_secure_cookie("_t", rs.data["token"])
            if redirect:
                self.redirect(redirect)
            else:
                self.redirect("/")
        else:
            self.render("login.html", msg=rs.msg, account=account)

    def _if_logined_then_go_home(self):
        """如果已经登录了，那么跳转到首页
        """
        token = self.get_secure_cookie("_t")
        if not token:
            return

        token = token.decode("utf-8")
        rs = self._("UserService").check_token(token)

        if rs.is_success():
            self.redirect("/index")
            return


class LogoutHandler(BaseWebHandler):

    @check_token
    def get(self):
        self._("UserService").logout(self.request._token)
        self.redirect("/login")


class SettingsHandler(BaseWebHandler):

    @check_token
    def get(self):
        self.render("user_settings.html")


class ModifyPasswordHandler(BaseWebHandler):

    @check_token
    def post(self):
        old_password, new_password = self._form("old_password", "new_password")
        rs = self._("UserService").modify_password(
            self.request.current_user.id,
            old_password,
            new_password
        )
        self._output_result(rs)


class ProfileHandler(BaseWebHandler):

    @check_token
    def get(self):
        return self.render("profile.html")
