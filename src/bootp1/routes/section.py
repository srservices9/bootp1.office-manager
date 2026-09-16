from flask import Blueprint, request, render_template

section = Blueprint("section", __name__, template_folder="templates")

@section.route("/invoices")
def invoice():
    return render_template("invoices.html")
