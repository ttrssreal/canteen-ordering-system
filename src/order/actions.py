from flask import request, session

from datetime import datetime
import sqlalchemy

from db.database import canteendb
from order.models import Product
from order.models import Order
from order.models import OrderProduct

# The core of the order API, providing the actual functionality
# Functions prefixed with "action" are marked for export, at least semantically

# The "action" functions should return a tuple representing a success value + results
# ie. (success: bool, results: primitive or builtin type (something that can be json encoded))

def action_get_items(req):
    """Responds with all of the products in the database"""
    try:
        items = [
            {
                "id": product.p_id,
                "name": product.name,
                "price": float(product.price)
                            # Another use of method from that database util class
            } for product in canteendb.get_items(Product)
        ]
    except:
        return False, None
    return True, items

def action_get_order(req):
    try:
        # Sanity checks?
        if not session:
            return False, None
        if "orderid" not in req:
            return False, None
        if not type(req["orderid"]) == int:
            return False, None
        
        # get the matching order, then the associated user_id
        user_id_order = Order.query.filter(Order.order_id == int(req["orderid"])).first().user_id
        # Permit access to either the owner of the data or an admin
        if session["s_id"] != user_id_order and session.get("perms") != 3:
            return False, None
        
        # SQL INNER JOIN query on Order and OrderProduct.
        order = OrderProduct.query.join(
            Order,
            OrderProduct.order_id == Order.order_id,
        ).join(
            Product,
            OrderProduct.p_id == Product.p_id,
        ).add_columns(
            # The infomation we want
            Product.name,
            OrderProduct.amount
        ).filter(
            # Match the user_id
            Order.user_id == int(session.get("s_id")),
        ).filter(
            # Match the order_id
            Order.order_id == int(req["orderid"]),
        ).all()
        # Return success status and the data organised into k-v pairs.
        return True, {prod[1]: prod[2] for prod in order}
    except:
        return False, None


def action_new_order(req):
    try:
        # Again sanity check
        if "items" not in req:
            return False, None
        if type(req["items"]) != list:
            return False, None
        if len(req["items"]) == 0:
            return False, None
        if "date" not in req:
            return False, None
        items = req["items"]
        # Make the order itme
        order = Order(
            date_of_creation=datetime.now(),
            # using the datetime module to parse the string into a datetime object
            target_date=datetime.strptime(req["date"], "%Y-%m-%d"),
            user_id=session.get("s_id")
        )
        # add the item
        canteendb.add_rows([order])
        
        # Immediately get the order_id by getting the most recent addition
        order_id = canteendb.db.session.query(Order).filter_by(
            user_id=session.get("s_id")
        ).order_by(
            # descending order so the highest first
            sqlalchemy.desc(Order.order_id)
        ).first().order_id

        # now with the order_id we can assign the item to the order
        # first generate all the OrderProduct items
        order_items = list(map(lambda item_details:
            OrderProduct(
                order_id=order_id,
                p_id=item_details["p_id"],
                amount=item_details["amount"]
            )
        , items))
        # then just insert all at once.
        canteendb.add_rows(order_items)
    except:
        return False, None
    # return success with no results
    return True, None