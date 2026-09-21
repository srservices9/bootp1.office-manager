from flask import Blueprint, flash, redirect, request, render_template
from bootp1.models.RecordManager import RecordService

RECORDS = RecordService()

section = Blueprint("section", __name__, template_folder="templates")

def get_customer_list():
        CUSTOMERS = RECORDS.search_for_records("CUSTOMER")
        return CUSTOMERS

#------------------------------Invoices-----------------------------
@section.route("/invoices")
@section.route("")
def invoice():
        CUSTOMERS = get_customer_list()
        return render_template("invoice-search.jinja", customers=CUSTOMERS)

@section.route("/invoices/new-invoice", methods=("GET", "POST"))
def new_invoice():
        CUSTOMERS = get_customer_list()
        TERMS = ["net 30", "net 15", "net 0"]

        if request.method == "POST":
                invoice_attributes = {}
                error = None 
                invoice_attributes["invoice_num"] = request.form["inv_num"]
                invoice_attributes["terms"] = request.form["terms"]
                invoice_attributes["total"] = request.form["total"]
                invoice_attributes["customer_id"] = request.form["customer"]
                if not invoice_attributes["invoice_num"]:
                        error = "Customer name is required"
                elif not invoice_attributes["terms"] or invoice_attributes["terms"] not in TERMS:
                        error = "Terms are missing or not valid"
                elif not invoice_attributes["total"]:
                        error = "Total amount is required"
                elif not invoice_attributes["customer_id"]:
                        error = "Customer is required"

                if error is None:
                        try:
                                print(invoice_attributes)
                                RECORDS.new_record("INVOICE", invoice_attributes)
                        except:
                                error = "Failed to add invoice"
                        else:
                                return redirect("/sections/invoices")

                flash(error)
                
        return render_template("new-invoice.jinja", customers=CUSTOMERS, terms=TERMS)
#------------------------------Customers-----------------------------

@section.route("/customers")
def customer():
        CUSTOMERS = get_customer_list()
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

#------------------------------Customers-----------------------------
