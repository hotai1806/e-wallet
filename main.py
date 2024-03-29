""" root module"""
from flask import Flask
from flask_migrate import Migrate
from src.models.models_base import db
from src.routes.account_url import account_bp
from src.routes.merchant_url import merchant_bp
from src.routes.transaction_url import transaction_bp
from src.setting import ENV, APP, DATABASE_CONNECTION

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_CONNECTION
app.config["ENV"] = ENV
app.config["APPLICATION_ROOT"] = APP
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True


db.init_app(app)
migrate = Migrate(app, db)
#
app.register_blueprint(account_bp, url_prefix="/accounts")
app.register_blueprint(merchant_bp, url_prefix="/merchants")
app.register_blueprint(transaction_bp, url_prefix="/transactions")


@app.route("/")
def hello_world():
    """
    Server status message
    """

    return "<p>Service still alive</p>{data}"


if __name__ == "__main__":
    app.run()
