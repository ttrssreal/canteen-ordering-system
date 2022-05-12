from flask import Blueprint
from . import views

blueprint = Blueprint("base", __name__, template_folder="templates")

blueprint.add_url_rule('/', 'index', views.index)
blueprint.add_url_rule('/info', 'info', views.info)
blueprint.add_url_rule('/favicon.ico', 'favicon', views.favicon) 