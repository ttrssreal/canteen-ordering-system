# PROBABLY VULN TO CSRF, dosent validate csrf token

from flask import render_template, send_file, redirect, request, url_for, make_response, session
import sqlalchemy, json, time, re
from auth.auth_level import AuthLevel

from user.models import User
from db.database import canteendb, UserError

name_test_regex = r"^[a-zA-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð ,.'-]+$"
student_id_regex = r"^\d{5}$"
password_regex = r"^((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*]).{7,30})$"

def login():
    if request.method == "GET":
        return render_template("auth/login.html")
    if request.method == "POST":
        response = make_response()
        response.content_type = "application/json; charset=UTF-8"
        creds = request.form
        if "studentid" not in creds or "pass" not in creds:
            response.set_data(json.dumps({"status": "error"}))
        print(creds)
        # authenticate
        # User.query.filter_b12452y(email = email).first()
        if User.query.filter_by(student_id=int(creds["studentid"])).first().password == creds["pass"]:
            session["authed"] = True
            return redirect("/")
        return render_template("auth/login.html")


def logout():
    session["authed"] = False
    return redirect("/")

def signup():
    if request.method == "GET":
        return render_template("auth/signup.html")
    if request.method == "POST":
        response = make_response()
        response.content_type = "application/json; charset=UTF-8"
        creds = request.json
        required_fields = ["fname", "lname", "studentid", "pass"]
        if not set(required_fields).issubset(set(creds)): # check we have all required fields
            response.set_data(json.dumps({"status": "error"}))
            return response
        # stop the haxors
        if not re.match(name_test_regex, creds["fname"]) or not re.match(name_test_regex, creds["lname"]):
            response.set_data(json.dumps({"status": "error"}))
            return response
        if not re.match(student_id_regex, creds["studentid"]):
            response.set_data(json.dumps({"status": "error"}))
            return response
        if not re.match(password_regex, creds["pass"]):
            response.set_data(json.dumps({"status": "error"}))
            return response
        
        u = User(
            first_name=creds["fname"],
            last_name=creds["lname"],
            student_id=creds["studentid"],
            password=creds["pass"]
        )

        if canteendb.add_rows([u]) == UserError.ALREADY_EXISTS:
            response.set_data(json.dumps({"status": "error", "generic": "User already exists"}))
            return response
        creds.pop("pass")
        session["details"] = creds
        session["authed"] = True
        response.set_data(json.dumps({"status": "success"}))
        return response