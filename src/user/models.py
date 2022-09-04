from db.database import canteendb
from auth.auth_level import AuthLevel

db = canteendb.db

class User(db.Model):
    s_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(32), index=True)
    last_name = db.Column(db.String(32), index=True)
    student_id = db.Column(db.Integer, index=True, unique=True)
    password = db.Column(db.String(32))
    permissions = db.Column(db.Integer)

    def __repr__(self):
        return f"<User {self.first_name} {self.last_name}, {self.permissions}>"