from flask import render_template, send_file, request, session, make_response, redirect
from order.models import Product
from db.database import canteendb
import json

actions = {
    "get_items": lambda: canteendb.get_items(Product) 
}

def order():
    if not session.get("authed"):
        return redirect("/login?next=order")
    if request.method == "GET":
        return render_template("order/order.html", session=session)
    if request.method == "POST":
        response = make_response()
        response.content_type = "application/json; charset=UTF-8"
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