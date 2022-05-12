from flask import render_template, send_file, request

def order():
    return render_template("order/order.html")