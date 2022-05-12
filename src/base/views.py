from flask import render_template, send_file, request

def index():
    return render_template("base/index.html")

def info():
    return render_template("base/info.html")

def favicon():
    return send_file("../static/favicon.ico", mimetype='image/gif')