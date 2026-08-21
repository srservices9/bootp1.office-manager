from flask import Flask
from flask import render_template
from bootp1.config import Config
from sqlalchemy import create_engine

def create_app():
    app = Flask("__name__")
    app.config.from_object(Config)


    @app.route("/")
    def root():
        return home()

    @app.route("/home")
    def home():
        return render_template("home.html")
 
    return app

def create_engine():
    engine = create_engine(Config.DATABASE_URL, echo=True)

    return engine

