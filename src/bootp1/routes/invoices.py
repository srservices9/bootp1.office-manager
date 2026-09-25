from flask import Blueprint, flash, redirect, request, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, DateTimeLocalField
from wtforms import validators
from bootp1.models.RecordManager import RecordService

RECORDS = RecordService()

invoices = Blueprint("invoices", __name__, template_folder="templates")

#------------------------------Invoices-----------------------------
@invoices.route("/", methods=("GET", "POST"))
def invoice():
        CUSTOMERS = RECORDS.search_for_records("CUSTOMER")

        if request.method == "POST":
                filters = {}
                error = None
                no_filters = all(value is None for value in request.form.values())
                if not no_filters:
                        if request.form["customer"]:
                                customer_obj = RECORDS.search_for_records("CUSTOMER", {"name": request.form["customer"], "match": None})
                                # search_for_records method will always return a list of ORM Objects or None.
                                if not customer_obj:
                                        error = "Customer not found"
                                else:
                                        filters["customer_id"] = customer_obj.record_id

                        if request.form["inv_num"]:
                                filters["invoice_num"] = request.form["inv_num"]
                        if request.form["min_total"]:
                                filters["min_total"] = request.form["min_total"]
                        if request.form["max_total"]:
                                filters["max_total"] = request.form["max_total"]

                        if error is None:
                                try:
                                        INVOICES = RECORDS.search_for_records("INVOICE", filters)
                                except:
                                        error = "Failed to find invoices"
                                else:
                                        return render_template("search-invoices.jinja", customers=CUSTOMERS, invoices=INVOICES)

                        flash(error)
                
        return render_template("search-invoices.jinja", customers=CUSTOMERS)

@invoices.route("/new-invoice", methods=("GET", "POST"))
def new_invoice():
        CUSTOMERS = RECORDS.search_for_records("CUSTOMER")
        ITEMS = RECORDS.search_for_records("ITEM")
        TERMS = ["net 30", "net 15", "net 0"]

        if request.method == "POST":
                invoice_attributes = {}
                items = {}
                error = None 
                invoice_attributes["invoice_num"] = request.form["inv_num"]
                invoice_attributes["terms"] = request.form["terms"]
                invoice_attributes["total"] = request.form["total"]
                customer_name = request.form["customer"]
                if not invoice_attributes["invoice_num"]:
                        error = "Invoice Number is required"
                elif not invoice_attributes["terms"] or invoice_attributes["terms"] not in TERMS:
                        error = "Terms are missing or not valid"
                elif not invoice_attributes["total"]:
                        error = "Total amount is required"
                elif not customer_name:
                        error = "Customer is required"
                else: 
                        customer_obj = RECORDS.search_for_records("CUSTOMER", {"name": customer_name, "match": None})
                        # search_for_records method will always return a list of ORM Objects or None.
                        if not customer_obj:
                                error = "Customer not found"
                        else:
                                invoice_attributes["customer_id"] = customer_obj.record_id

                if error is None:
                        try:
                                RECORDS.new_record("INVOICE", invoice_attributes)
                        except:
                                error = "Failed to add invoice"
                        else:
                                return redirect("/invoices")

                flash(error)
                
        return render_template("new-invoice.jinja", customers=CUSTOMERS, terms=TERMS, items=ITEMS)
