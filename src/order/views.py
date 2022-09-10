from flask import render_template, send_file, request, session, make_response, redirect
import json, datetime, sqlalchemy

from db.database import canteendb

from auth.csrf import check_csrf
from auth.routes import protected
from auth.auth_level import AuthLevel

from .actions import *
# define a mapping of server function strings to python functions from actions.py
actions = {
    "get_items": action_get_items,
    "new_order": action_new_order,
    "get_order": action_get_order
}

@protected(AuthLevel.Student, redirect="order")
def order_get():
    return render_template("order/order.html", session=session)

@check_csrf
@protected(AuthLevel.Student, redirect="order")
def order_post():
    """Takes a post to order, parses it and calls the appropriate server function with any input specified"""
    response = make_response()
    response.content_type = "application/json; charset=UTF-8"
    req_json = request.get_json()
    if "action" not in req_json:
        response.set_data(json.dumps({"status": "error", "msg":"No action."}))
        return response
    if req_json["action"] not in actions:
        response.set_data(json.dumps({"status": "error", "msg":"Action non-existant."}))
        return response
    action = req_json["action"]
    # lookup and invoke the function matching the string supplying the request as a parameter
    successful, result = actions[action](req_json)
    # parse the output to the HTTP response
    returned = {"status": "success" if successful else "failed"}
    if result:
        returned["result"] = result
    response.set_data(json.dumps(returned))
    return response