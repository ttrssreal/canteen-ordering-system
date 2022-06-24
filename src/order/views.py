from flask import render_template, send_file, request, session, make_response, redirect
from order.models import Product

def order():
    if not session.get("authed"):
        return redirect("/")
    if request.method == "GET":
        return render_template("order/order.html", session=session)