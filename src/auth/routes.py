from flask import session, make_response, request, render_template
from flask import redirect as flask_redirect
from auth.auth_level import AuthLevel, check_auth_level
from user.models import User
from functools import wraps

def protected(auth_level: AuthLevel, redirect:str=None, send_unauthorized=False):
    """
    The decorator protected requires route access to be authenticated.
    The auth_level parameter defines a minimum required access level.
    By default it will redirect to login. 
    The user will be sent to the redirect parameter after login. 
    If send_unauthorized is True then an unauthorized page is shown.

    eg.
    @protected(AuthLevel.Student, redirect="view")
    def view():
        ...
    """
    def check_login(view):
        @wraps(view)
        def func(*args, **kwargs):
            # Use the settings
            if redirect and not send_unauthorized:
                unauth_resp = flask_redirect("/login?next=" + redirect)
            elif not send_unauthorized:
                unauth_resp = flask_redirect("/login")
            else:
                unauth_resp = make_response(render_template("auth/unauthorized.html"))
            if not session.get("authed"):
                return unauth_resp
            s_id = session.get("studentid")
            if not s_id:
                return unauth_resp
            # in case we change permissions, we don't save in the session
            user = User.query.filter_by(student_id=int(s_id)).first()
            if not user:
                return unauth_resp
            # just a fancy int comparison
            if not check_auth_level(auth_level, user.permissions):
                return unauth_resp
            return view(*args, **kwargs)
        return func
    return check_login