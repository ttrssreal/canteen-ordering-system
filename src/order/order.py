from flask import Blueprint
from . import views

blueprint = Blueprint("order", __name__, template_folder="templates")

blueprint.add_url_rule('/order', 'order', views.order, methods=["GET", "POST"])