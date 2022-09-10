from flask import Blueprint
from . import views

blueprint = Blueprint("base", __name__, template_folder="templates")

blueprint.add_url_rule('/', 'index', views.index)
blueprint.add_url_rule('/info', 'info', views.info)
blueprint.add_url_rule('/favicon.ico', 'favicon', views.favicon)

# seems weird but just using a decorator in a
# different way to set HTTP error handlers
blueprint.app_errorhandler(404)(views.not_found)
blueprint.app_errorhandler(500)(views.server_error)