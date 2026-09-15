from flask import render_template, request, Blueprint

home = Blueprint("home", __name__, template_folder="templates")

@home.route("/home")
@home.route("/")
def welcome():
    return render_template("home.html")
