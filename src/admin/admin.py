from flask import Blueprint
from . import views

blueprint = Blueprint("admin", __name__, template_folder="templates")

blueprint.add_url_rule('/admin', 'admin_get', views.admin_get, methods=["GET"])

# like a protected static file (more info on the route)
blueprint.add_url_rule('/admin/admin.js', 'admin_js', views.javascript, methods=["GET"])