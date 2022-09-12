from flask import render_template, send_file, request, session, make_response, redirect
from order.models import Product
from db.database import canteendb
from auth.csrf import check_csrf
import json

actions = {
    "get_items": lambda: canteendb.get_items(Product) 
}

def order_get():
    if not session.get("authed"):
        return redirect("/login?next=order")
    return render_template("order/order.html", session=session)

@check_csrf
def order_post():
    if not session.get("authed"):
        return redirect("/login?next=order")
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
    result = [{"id": product.p_id, "name": product.name, "price": float(product.price)} for product in actions[action]()]
    response.set_data(json.dumps({"status": "success", "items": result}))
    return response