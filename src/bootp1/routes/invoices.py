from flask import Blueprint, flash, redirect, request, render_template
from ..models.RecordManager import RecordService
from ..forms.InvoiceForms import Invoices, NewInvoice

RECORDS = RecordService()

invoices = Blueprint("invoices", "invoice", template_folder="templates")

#------------------------------Invoices-----------------------------
@invoices.route("/", methods=("GET", "POST"))
def invoice():
        CUSTOMERS = RECORDS.search_for_records("CUSTOMER")
        FORM = Invoices()
        customer_ids = {}
        customer_names = []
        if CUSTOMERS:
                for customer in CUSTOMERS:
                        customer_ids[customer.name] = customer.record_id
                        customer_names.append(customer.name)

        FORM.customer.datalist = customer_names

        if request.method == "POST":
                filters = None
                error = None
                no_filters = all(value is None for value in FORM.data)
                if not no_filters:
                        filters = {}
                        if FORM.customer.data:
                                if FORM.customer.data not in customer_ids:
                                        error = "Customer not found"
                                else:
                                        filters["customer_id"] = customer_ids[FORM.customer.data]

                        if FORM.invoice_num.data:
                                filters["invoice_num"] = FORM.invoice_num.data
                        if FORM.min_total.data:
                                filters["min_total"] = FORM.min_total.data
                        if FORM.max_total.data:
                                filters["max_total"] = FORM.max_total.data

                        # Flushing form values to prevent previously submitted data from affecting new submits.
                        FORM.customer.data = None
                        FORM.invoice_num.data = None
                        FORM.min_total.data = None
                        FORM.max_total.data = None

                if error is None:
                        try:
                                RESULTS = RECORDS.search_for_records("INVOICE", filters)
                        except:
                                error = "Failed to find invoices"
                        else:
                                return render_template("search-invoices.jinja", form=FORM, results=RESULTS)

                flash(error)
                
        return render_template("search-invoices.jinja", form=FORM)

@invoices.route("/new-invoice", methods=("GET", "POST"))
def new_invoice():
        CUSTOMERS = RECORDS.search_for_records("CUSTOMER")
        ITEMS = RECORDS.search_for_records("ITEM")
        TERMS = ["net 30", "net 15", "net 0"]

        FORM = NewInvoice()

        if request.method == "POST":
                attributes = {}
                items = {}
                error = None 
                attributes["invoice_num"] = request.form["inv_num"]
                attributes["terms"] = request.form["terms"]
                attributes["total"] = request.form["total"]
                customer_name = request.form["customer"]
                if not attributes["invoice_num"]:
                        error = "Invoice Number is required"
                elif not attributes["terms"] or attributes["terms"] not in TERMS:
                        error = "Terms are missing or not valid"
                elif not attributes["total"]:
                        error = "Total amount is required"
                elif not customer_name:
                        error = "Customer is required"
                else: 
                        customer_obj = RECORDS.search_for_records("CUSTOMER", {"name": customer_name, "match": None})
                        # search_for_records method will always return a list of ORM Objects or None.
                        if not customer_obj:
                                error = "Customer not found"
                        else:
                                attributes["customer_id"] = customer_obj.record_id

                if error is None:
                        try:
                                RECORDS.new_record("INVOICE", attributes)
                        except:
                                error = "Failed to add invoice"
                        else:
                                return redirect("/invoices")

                flash(error)

        return render_template("new-invoice.jinja", customers=CUSTOMERS, terms=TERMS, items=ITEMS)
