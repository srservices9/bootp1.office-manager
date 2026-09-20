from flask import Blueprint, request, render_template
from bootp1.models.RecordManager import RecordService

RECORDS = RecordService()

section = Blueprint("section", __name__, template_folder="templates")

@section.route("/invoices")
@section.route("")
def invoice():
        CUSTOMERS = RECORDS.search_for_records("CUSTOMER")
        return render_template("invoice-search.jinja", customers=CUSTOMERS)

@section.route("/customers")
def customer():
        CUSTOMERS = RECORDS.search_for_records("CUSTOMER")
        return render_template("customer-search.jinja", customers=CUSTOMERS)

@section.route("/customers/new-customer")
def new_customer():
        return render_template("new-customer.jinja")
