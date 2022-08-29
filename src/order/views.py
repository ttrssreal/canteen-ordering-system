from flask import render_template, send_file, request, session, make_response, redirect
from order.models import Product
from db.database import canteendb
from auth.csrf import check_csrf
from auth.routes import protected
from auth.auth_level import AuthLevel
import json

actions = {
    "get_items": lambda: [{
            "id": product.p_id,
            "name": product.name,
            "price": float(product.price)
        } for product in canteendb.get_items(Product)
    ]
}

@protected(AuthLevel.Student, redirect="order")
def order_get():
    return render_template("order/order.html", session=session)

@check_csrf
@protected(AuthLevel.Student, redirect="order")
def order_post():
    response = make_response()
    response.content_type = "application/json; charset=UTF-8"
    if not session.get("authed"):
        response.set_data(json.dumps({"status": "error", "msg":"Not authorized."}))
        return response
    creds = request.get_json()
    if "action" not in creds:
        response.set_data(json.dumps({"status": "error", "msg":"No action."}))
        return response
    if creds["action"] not in actions:
        response.set_data(json.dumps({"status": "error", "msg":"Action non-existant."}))
        return response
    action = creds["action"]
    response.set_data(json.dumps({"status": "success", "result": actions[action]()}))
    return response