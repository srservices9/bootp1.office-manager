from flask import Blueprint, flash, redirect, request, render_template
from bootp1.models.RecordManager import RecordService

RECORDS = RecordService()

section = Blueprint("section", __name__, template_folder="templates")

@section.route("/invoices")
@section.route("")
def invoice():
        customer_rows = RECORDS.search_for_records("CUSTOMER")
        CUSTOMERS = None
        if customer_rows:
                CUSTOMERS = []
                for customer in customer_rows:
                        customer_name = customer[0].name
                        CUSTOMERS.append(customer_name)
        return render_template("invoice-search.jinja", customers=CUSTOMERS)

@section.route("/customers")
def customer():
        customer_rows = RECORDS.search_for_records("CUSTOMER")
        CUSTOMERS = None
        if customer_rows:
                CUSTOMERS = []
                for customer in customer_rows:
                        customer_name = customer[0].name
                        CUSTOMERS.append(customer_name)
        return render_template("customer-search.jinja", customers=CUSTOMERS)

@section.route("/customers/new-customer", methods=("GET", "POST"))
def new_customer():
        if request.method == "POST":
                customer_attributes = {}
                error = None 
                customer_attributes["name"] = request.form["cname"]
                if not customer_attributes["name"]:
                        error = "Customer name is required"
                elif request.form["ct_fname"]:
                        customer_attributes["contact_first_name"] = request.form["ct_fname"]
                elif request.form["ct_lname"]:
                        customer_attributes["contact_last_name"] = request.form["ct_lname"]
                elif request.form["ct_phone"]:
                        customer_attributes["contact_phone"] = request.form["ct_phone"]

                if error is None:
                        try:
                                print(customer_attributes)
                                RECORDS.new_record("CUSTOMER", customer_attributes)
                        except:
                                error = "Failed to add customer"
                        else:
                                return redirect("/sections/customers")

                flash(error)
                
        return render_template("new-customer.jinja")
