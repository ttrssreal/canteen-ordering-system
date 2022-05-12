from flask import Flask
from base import base
from auth import auth
from order import order
from user import user

app = Flask(__name__, static_folder="../static")

app.register_blueprint(base.blueprint)
app.register_blueprint(auth.blueprint)
app.register_blueprint(order.blueprint)
app.register_blueprint(user.blueprint)

if __name__ == "__main__":
    app.run(debug=True)