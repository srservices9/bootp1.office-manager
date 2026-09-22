from flask import Blueprint, flash, redirect, request, render_template
from bootp1.models.RecordManager import RecordService
from bootp1.models.DatabaseManager import Repository
from sqlalchemy.exc import IntegrityError

RECORDS = RecordService()

section = Blueprint("section", __name__, template_folder="templates")

def get_customer_list():
        CUSTOMERS = RECORDS.search_for_records("CUSTOMER")
        return CUSTOMERS

#------------------------------Invoices-----------------------------
@section.route("/invoices", methods=("GET", "POST"))
@section.route("")
def invoice():
        CUSTOMERS = get_customer_list()

        if request.method == "POST":
                filters = {}
                error = None
                no_filters = all(value is None for value in request.form.values())
                if not no_filters:
                        if request.form["customer"]:
                                customer_obj_list = RECORDS.search_for_records("CUSTOMER", {"name": request.form["customer"], "match": None})
                                # search_for_records method will always return a list of ORM Objects or None.
                                if not customer_obj_list:
                                        error = "Customer not found"
                                else:
                                        filters["customer_id"] = customer_obj_list[0].record_id

                        elif request.form["inv_num"]:
                                filters["invoice_num"] = request.form["inv_num"]
                        elif request.form["min_total"]:
                                filters["min_total"] = request.form["min_total"]
                        elif request.form["max_total"]:
                                filters["max_total"] = request.form["max_total"]

                        if request.form["min_total"] and request.form["max_total"]:
                                if request.form["min_total"] > request.form["max_total"]:
                                        error = "Minimum total cannot be more than maximum total"

                        if error is None:
                                try:
                                        INVOICES = RECORDS.search_for_records("INVOICE", filters)
                                        print(INVOICES)
                                except:
                                        error = "Failed to find invoices"
                                else:
                                        return render_template("invoice-search.jinja", customers=CUSTOMERS, invoices=INVOICES)

                        flash(error)
                
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
                customer_name = request.form["customer"]
                print(customer_name)
                if not invoice_attributes["invoice_num"]:
                        error = "Invoice Number is required"
                elif not invoice_attributes["terms"] or invoice_attributes["terms"] not in TERMS:
                        error = "Terms are missing or not valid"
                elif not invoice_attributes["total"]:
                        error = "Total amount is required"
                elif not customer_name:
                        error = "Customer is required"
                else: 
                        customer_obj_list = RECORDS.search_for_records("CUSTOMER", {"name": customer_name, "match": None})
                        # search_for_records method will always return a list of ORM Objects or None.
                        if not customer_obj_list:
                                error = "Customer not found"
                        else:
                                invoice_attributes["customer_id"] = customer_obj_list[0].record_id

                if error is None:
                        try:
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
                        except IntegrityError:
                                error = f"Failed to add customer. {request.form["cname"]} already exists."
                        except Exception as exc:
                                error = f"Failed to add customer. {exc}"
                        else:
                                return redirect("/sections/customers")

                flash(error)
                
        return render_template("new-customer.jinja")

#------------------------------Customers-----------------------------
