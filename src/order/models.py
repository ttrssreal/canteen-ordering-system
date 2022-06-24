from db.database import canteendb
from auth.auth_level import AuthLevel

db = canteendb.db

class Product(db.Model):
    p_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), index=True)
    price = db.Column(db.Numeric)

    def __repr__(self):
        return f"<Product {self.name}: ${self.price}>"