from flask import Flask

app = Flask(__name__, static_folder="../static")

# sessions
from flask_session import Session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

from db.database import canteendb
canteendb.init(app)

from base import base
from auth import auth
from order import order
from user import user

app.register_blueprint(base.blueprint)
app.register_blueprint(auth.blueprint)
app.register_blueprint(order.blueprint)
app.register_blueprint(user.blueprint)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')