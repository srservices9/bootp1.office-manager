from flask import Flask
from .config import Config
from .routes import home, invoices, customers, items

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.register_blueprint(home.home, url_prefix="")
    app.register_blueprint(invoices.invoices, url_prefix="/invoices")
    app.register_blueprint(customers.customers, url_prefix="/customers")
    app.register_blueprint(items.items, url_prefix="/items")

    return app


