""" root module"""
from flask import Flask, request
from flask_migrate import Migrate
from src.models.models_base import db
from src.models.account import Account
from src.models.merchant import Merchant
from src.models.transaction import Transaction
from src.routes.account_url import account_bp
from src.routes.merchant_url import merchant_bp
from src.setting import ENV, APP, DATABASE_CONNECTION

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
# app.config['SECRET_KEY'] = "random string"
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_CONNECTION
app.config["ENV"] = ENV
app.config["APPLICATION_ROOT"] = APP
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


db.init_app(app)
migrate = Migrate(app, db)
#
app.register_blueprint(account_bp, url_prefix="/accounts")
app.register_blueprint(merchant_bp, url_prefix="/merchants")
# app.register_blueprint(product_bp.product_bp, url_prefix="/product")
# app.register_blueprint(cart_bp.cart_bp, url_prefix="/cart")


@app.route("/")
def hello_world():
    """
    Server status message
    """

    return "<p>Service still alive</p>{data}"


if __name__ == "__main__":
    app.run()
