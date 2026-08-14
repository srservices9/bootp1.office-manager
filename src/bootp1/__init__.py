from flask import Flask
from bootp1.config import Config
from sqlalchemy import create_engine

def create_app():
    app = Flask("__name__")
    app.config.from_object(Config)

    engine = create_engine(Config.DATABASE_URL, echo=True)

    @app.route("/home")
    def home():
        return render_template("home.html")
 
    return app, engine

