from flask import render_template, send_file, redirect, request

def login():
    if request.method == "GET":
        return render_template("auth/login.html")
    if request.method == "POST":
        creds = request.form
        if "user" not in creds or "pwd" not in creds:
            return "Insufficient Credentials"
        # authenticate
        return render_template("auth/login.html")


def logout():
    return redirect("/")

def signup():
    if request.method == "GET":
        return render_template("auth/signup.html")
    if request.method == "POST":
        creds = request.form
        if "user" not in creds or "pwd" not in creds:
            return "Insufficient Credentials"
        # add user
        return render_template("auth/signup.html")