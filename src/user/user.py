from flask import Blueprint
from . import views

blueprint = Blueprint("user", __name__, template_folder="templates")

blueprint.add_url_rule('/profile', 'profile', views.profile_get, methods=["GET"])
blueprint.add_url_rule('/profile/<int:userid>', 'profile_by_user', views.profile_by_user, methods=["GET"])