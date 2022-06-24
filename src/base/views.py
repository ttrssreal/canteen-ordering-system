from flask import render_template, send_file, request, session

def index():
    return render_template("base/index.html", session=session)

def info():
    return render_template("base/info.html", session=session)

def favicon():
    return send_file("../static/favicon.ico", mimetype='image/gif')