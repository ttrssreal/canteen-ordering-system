from flask import render_template, send_file, request, session, redirect
import sqlalchemy
from user.models import User
from order.models import Order, OrderProduct
from auth.routes import protected
from auth.csrf import check_csrf
from auth.auth_level import AuthLevel

from base.views import not_found
from base.views import server_error

def get_orders_by_user(userid):
    return [
        {
            "id": prod[1],
            "cd": "{}/{}/{} {}:{}".format(prod[2].day, prod[2].month, prod[2].year, prod[2].hour, prod[2].second),
            "td": "{}/{}/{} {}:{}".format(prod[3].day, prod[3].month, prod[3].year, prod[3].hour, prod[3].second)
        }
        for prod in Order.query.filter(
                        Order.user_id == userid,
                    ).add_columns(
                        Order.order_id,
                        Order.date_of_creation,
                        Order.target_date
                    ).all()
    ]

@protected(AuthLevel.Student, redirect="profile")
def profile_get():
    user = User.query.filter_by(student_id=int(session["studentid"])).first()
    orders = get_orders_by_user(user.s_id)
    return render_template("user/profile.html", session=session,
        studentid=user.student_id,
        first_name=user.first_name,
        last_name=user.last_name,
        orders=orders,
        owns=True
    )


@protected(AuthLevel.Admin, send_unauthorized=True)
def profile_by_user(userid):
    try:
        user = User.query.filter_by(s_id=userid).first()
        if not user:
            return not_found(404)
        orders = get_orders_by_user(user.s_id)
        return render_template("user/profile.html", session=session,
            studentid=user.student_id,
            first_name=user.first_name,
            last_name=user.last_name,
            orders=orders,
            owns=False
        )
    except:
        return not_found(404)
