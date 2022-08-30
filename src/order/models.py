from db.database import canteendb
from auth.auth_level import AuthLevel
from user.models import User

db = canteendb.db

class Product(db.Model):
    p_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), index=True)
    price = db.Column(db.Numeric)

    def __repr__(self):
        return f"<Product {self.name}: ${self.price}>"

class Order(db.Model):
    order_id = db.Column(db.Integer, primary_key=True)
    date_of_creation = db.Column(db.DateTime)
    target_date = db.Column(db.DateTime)
    user = db.relationship("User")
    user_id = db.Column(db.Integer, db.ForeignKey(User.s_id))

    def __repr__(self):
        return f"<Order id: {self.order_id}, User id: {self.user_id}, for: {self.target_date}>"

class OrderProduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey(Order.order_id))
    p_id = db.Column(db.Integer, db.ForeignKey(Product.p_id))
    amount = db.Column(db.Integer)
    order = db.relationship("Order")
    product = db.relationship("Product")

    def __repr__(self):
        return f"<OrderItem from order: {self.order_id}, Product id: {self.p_id}, Quantity: {self.amount}>"