from flask import Blueprint
from . import views
from auth.auth_level import AuthLevel

blueprint = Blueprint("auth", __name__, template_folder="templates")

blueprint.add_url_rule('/login', 'login', views.login, methods=["GET", "POST"])
blueprint.add_url_rule('/logout', 'logout', views.logout)
blueprint.add_url_rule('/signup', 'signup', views.signup, methods=["GET", "POST"])