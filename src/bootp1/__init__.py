from flask import Flask
from bootp1.config import Config
from bootp1.routes import home, section
from sqlalchemy import create_engine

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.register_blueprint(home.home, url_prefix="")
    app.register_blueprint(section.section, url_prefix="/sections")

    return app

def create_engine_link():
    engine = create_engine(Config.DATABASE_URL, echo=True)

    return engine

