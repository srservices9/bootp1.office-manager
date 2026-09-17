from flask import Blueprint, request, render_template

section = Blueprint("section", __name__, template_folder="templates")

customers = ["Bill", "Bob"]

@section.route("/invoices/inv-search")
@section.route("/invoices")
@section.route("")
def invoice():
    return render_template("invoice-search.html", customers=customers)
