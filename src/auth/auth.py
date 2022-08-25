from flask import Blueprint
from . import views
from auth.auth_level import AuthLevel

blueprint = Blueprint("auth", __name__, template_folder="templates")

blueprint.add_url_rule('/login', 'login_get', views.login_get, methods=["GET"])
blueprint.add_url_rule('/login', 'login_post', views.login_post, methods=["POST"])

blueprint.add_url_rule('/logout', 'logout', views.logout)

blueprint.add_url_rule('/signup', 'signup_get', views.signup_get, methods=["GET"])
blueprint.add_url_rule('/signup', 'signup_post', views.signup_post, methods=["POST"])