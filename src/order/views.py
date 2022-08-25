from flask import render_template, send_file, request, session, make_response, redirect

def order():
    if not session.get("authed"):
        return redirect("/")
    return render_template("order/order.html")