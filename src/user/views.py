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
    """Returns a json array of the orders from a user"""
    return [
        {
            "id": prod[1],
            # format the database entries
            "cd": "{}/{}/{} {}:{}".format(prod[2].day, prod[2].month, prod[2].year, prod[2].hour, prod[2].second),
            "td": "{}/{}/{} {}:{}".format(prod[3].day, prod[3].month, prod[3].year, prod[3].hour, prod[3].second)
        }
        for prod in Order.query.filter(
                        # belonging to the user_id supplied
                        Order.user_id == userid,
                    ).add_columns(
                        # get the infomation we need
                        Order.order_id,
                        Order.date_of_creation,
                        Order.target_date
                    ).all()
    ]

@protected(AuthLevel.Student, redirect="profile")
def profile_get():
    """Route renders the users current and past orders"""
    user = User.query.filter_by(student_id=int(session["studentid"])).first()
    orders = get_orders_by_user(user.s_id)
    # the (jinja2) template just loops through the orders list and displays each
    return render_template("user/profile.html", session=session,
        studentid=user.student_id,
        first_name=user.first_name,
        last_name=user.last_name,
        orders=orders,
        owns=True
    )

# due to the sensitive nature of the infomation, it is restricted
@protected(AuthLevel.Admin, send_unauthorized=True)
def profile_by_user(userid):
    """Route responds with another users data and orders"""
    try:
        user = User.query.filter_by(s_id=userid).first()
        if not user:
            # stop scanners scraping user_id's by giving a generic response
            return not_found(404)
        # get different users data
        orders = get_orders_by_user(user.s_id)
        # again render to the same template
        return render_template("user/profile.html", session=session,
            studentid=user.student_id,
            first_name=user.first_name,
            last_name=user.last_name,
            orders=orders,
            owns=False
        )
    except:
        # generic response
        return not_found(404)
