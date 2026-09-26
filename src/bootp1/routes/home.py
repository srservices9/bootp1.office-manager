from flask import render_template, Blueprint

home = Blueprint("home", __name__, template_folder="templates")

@home.route("/login")
@home.route("/")
def welcome():
    return render_template("login.jinja")

