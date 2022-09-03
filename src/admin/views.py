from flask import render_template, send_file, request, session, make_response, redirect, send_file
import json, datetime, sqlalchemy

from db.database import canteendb

from auth.csrf import check_csrf
from auth.routes import protected
from auth.auth_level import AuthLevel

from user.models import User
from order.models import Order

@protected(AuthLevel.Admin, redirect="admin")
def admin_get():
    users = User.query.all()
    orders = [
        {
            "id": prod[1],
            "s_id": prod[4],
            "cd": "{}/{}/{} {}:{}".format(prod[2].day, prod[2].month, prod[2].year, prod[2].hour, prod[2].second),
            "td": "{}/{}/{} {}:{}".format(prod[3].day, prod[3].month, prod[3].year, prod[3].hour, prod[3].second)
        }
        for prod in Order.query.add_columns(
                        Order.order_id,
                        Order.date_of_creation,
                        Order.target_date,
                        Order.user_id
                    ).all()
    ]
    users = list(map(lambda user:
        {
            "id": user.s_id,
            "name": user.first_name + " " + user.last_name,
            "sid": user.student_id,
            "permisions": user.permissions
        }
    , users))
    return render_template("admin/admin.html", session=session, users=users, orders=orders)

@protected(AuthLevel.Admin, send_unauthorized=True)
def javascript():
    return send_file("admin/admin.js", mimetype='text/javascript')