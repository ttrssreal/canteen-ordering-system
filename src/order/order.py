from flask import Blueprint
from . import views

blueprint = Blueprint("order", __name__, template_folder="templates")

blueprint.add_url_rule('/order', 'order_get', views.order_get, methods=["GET"])
blueprint.add_url_rule('/order', 'order_post', views.order_post, methods=["POST"])