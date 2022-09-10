from flask import render_template, send_file, request, session

def index():
    return render_template("base/index.html", session=session)

def info():
    print(session)
    return render_template("base/info.html", session=session)

def favicon():
    return send_file("../static/favicon.ico", mimetype='image/gif')

def not_found(e):
    return render_template("base/error/404.html", session=session)

def server_error(e):
    return render_template("base/error/500.html", session=session)