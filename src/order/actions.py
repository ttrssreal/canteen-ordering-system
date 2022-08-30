from flask import request, session

from datetime import datetime
import sqlalchemy

from db.database import canteendb
from order.models import Product
from order.models import Order
from order.models import OrderProduct

def action_get_items(req):
    try:
        items = [
            {
                "id": product.p_id,
                "name": product.name,
                "price": float(product.price)
            } for product in canteendb.get_items(Product)
        ]
    except:
        return False, None
    return True, items

def action_new_order(req):
    if "items" not in req:
        return False, None
    if type(req["items"]) != list:
        return False, None
    if len(req["items"]) == 0:
        return False, None
    if "date" not in req:
        return False, None
    try:
        items = req["items"]
        print("Request:", req)
        print("items:", req["items"])
        order = Order(
            date_of_creation=datetime.now(),
            target_date=datetime.strptime(req["date"], "%Y-%m-%d"),
            user_id=session.get("s_id")
        )
        canteendb.add_rows([order])
        order_id = canteendb.db.session.query(Order).filter_by(
            user_id=session.get("s_id")
        ).order_by(
            sqlalchemy.desc(Order.order_id)
        ).first().order_id

        order_items = list(map(lambda item_details:
            # needs checks
            OrderProduct(
                order_id=order_id,
                p_id=item_details["p_id"],
                amount=item_details["amount"]
            )
        , items))
        canteendb.add_rows(order_items)
    except:
        return False, None
    return True, None