from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
import sqlalchemy

class CanteenDatabase():
    def init(self, flask_app):
        flask_app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_LOCATION"]
        flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        self.db = SQLAlchemy(flask_app)
        self.migrate = Migrate(flask_app, self.db)
        self.db.create_all()
    
    def add_rows(self, obj):
        self.db.session.add_all(obj)
        try:
            self.db.session.commit()
        except sqlalchemy.exc.IntegrityError as e:
            if e.code == "gkpj":
                return UserError.ALREADY_EXISTS

class CanteenDbError(Exception):
    def __init__(self, f, *args):
        super().__init__(args)
        self.init(f, *args)
    def init(f, *args):
        """ override """

class UserError(CanteenDbError):
    def init(self, f, *args):
        print(f)
    ALREADY_EXISTS = 0

# class UserError(CanteenDbError):


canteendb = CanteenDatabase()