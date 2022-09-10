from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
import sqlalchemy

# Util class for interfacing with the database
class CanteenDatabase():
    def init(self, flask_app):
        db_loc = os.environ.get("DATABASE_LOCATION")
        if not db_loc:
            print("ERROR: DATABASE_LOCATION environment variable is not set.")
            quit(1)
        flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_loc
        flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        self.db = SQLAlchemy(flask_app)
        # setup migrations
        self.migrate = Migrate(flask_app, self.db)
        self.db.create_all()
    
    def add_rows(self, obj):
        self.db.session.add_all(obj)
        try:
            self.db.session.commit()
        except sqlalchemy.exc.IntegrityError as e:
            if e.code == "gkpj":
                return UserError.ALREADY_EXISTS
    
    def get_items(self, table):
        return [ item for item in table.query.all()]

# An attempt at makeing somthing of a custom
# error wrapper around sqlite's
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

# The class is instantiated as a sort of global static instance
canteendb = CanteenDatabase()