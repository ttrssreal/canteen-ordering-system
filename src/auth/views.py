from flask import render_template, send_file, redirect, request, url_for, make_response, session
import sqlalchemy, json, time, re, bcrypt
from auth.auth_level import AuthLevel

from auth.csrf import check_csrf, gen_csrf

from user.models import User
from db.database import canteendb, UserError

# These regex's are for verifying the server input.
# This is done on the client as well only for speed,
# as we can trust the client.

# One or more ascii or unicode characters to support more diverse names.
name_test_regex = r"^[a-zA-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð ,.'-]+$"
# A string with 5 digits
student_id_regex = r"^\d{5}$"
# Must contain at least one digit, lowercase, uppercase and special
# character anywhere in the string, providing the string is between 7 and 30 characters.
# This closely adheres to the governments suggested password requirements
password_regex = r"^((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*]).{7,30})$"

def login_get():
    return render_template("auth/login.html", session=session)

# Authenticates the user asynchronously on the frontend
def login_post():
    """
    This route will return a json HTTP response with a status value
    either success or error
    """
    response = make_response()
    # set mime type
    response.content_type = "application/json; charset=UTF-8"
    if session.get("authed"):
        # instruct the client to set the "msg" elements value.
        response.set_data(json.dumps({"status": "error", "msg": 
            "Already Authenticated."
        }))
        return response

    creds = request.get_json()
    if "studentid" not in creds or "pass" not in creds:
        response.set_data(json.dumps({"status": "error"}))
        return response
    if not creds["studentid"].isdigit():
        response.set_data(json.dumps({"status": "error"}))
        return response

    # Get the users details from the database
    user = User.query.filter_by(student_id=int(creds["studentid"])).first()
    if user:
        if bcrypt.checkpw(creds["pass"].encode("utf-8"), user.password):
            session["s_id"] = user.s_id
            session["perms"] = user.permissions
            session["studentid"] = creds["studentid"]
            session["authed"] = True
            # set a new server side anti-csrf token
            session["csrf_token"] = gen_csrf()
            response.set_data(json.dumps({"status": "success"}))
            return response 
    response.set_data(json.dumps({"status": "error"}))
    return response 

def signup_get():
    return render_template("auth/signup.html", session=session)
    
def signup_post():
    """Verifys and inserts new users into the database."""
    response = make_response()
    response.content_type = "application/json; charset=UTF-8"
    creds = request.json
    required_fields = ["fname", "lname", "studentid", "pass"]
    if not set(required_fields).issubset(set(creds)): # check we have all required fields
        response.set_data(json.dumps({"status": "error"}))
        return response
    # stop the haxors
    # match appropriate regex's described above against corrosponding user supplied values.
    if not re.match(name_test_regex, creds["fname"]) or not re.match(name_test_regex, creds["lname"]):
        response.set_data(json.dumps({"status": "error"}))
        return response
    if not re.match(student_id_regex, creds["studentid"]):
        response.set_data(json.dumps({"status": "error"}))
        return response
    if not re.match(password_regex, creds["pass"]):
        response.set_data(json.dumps({"status": "error"}))
        return response
    
    encoded_password = creds["pass"].encode("utf-8")
    hashed_password = bcrypt.hashpw(encoded_password, bcrypt.gensalt())

    # aaa!2Daaa!2D
    # prepare the user item
    u = User(
        first_name=creds["fname"],
        last_name=creds["lname"],
        student_id=creds["studentid"],
        password=hashed_password,
        permissions=1
    )

    # use the static database util class to insert the single item
    if canteendb.add_rows([u]) == UserError.ALREADY_EXISTS:
        response.set_data(json.dumps({"status": "error", "generic": "User already exists"}))
        return response
    creds.pop("pass")
    session["details"] = creds
    response.set_data(json.dumps({"status": "success"}))
    return response

# Check csrf is good to have so users can't be logged out by third parties
@check_csrf
def logout_post():
    """Clears the users session data and logs them out"""
    resp = make_response()
    session.clear()
    resp.status = 200
    return resp