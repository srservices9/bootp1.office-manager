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
        TERMS = [(30, "Net 30"), (15, "Net 15"), (0, "Net 0")]

        item_names = []
        item_ids = {}
        if ITEMS:
                for item in ITEMS:
                        item_names.append(item.name)
                        item_ids[item.name] = item.record_id

        customer_names = []
        customer_ids = {}
        if CUSTOMERS:
                for customer in CUSTOMERS:
                        customer_names.append(customer.name)
                        customer_ids[customer.name] = customer.record_id

        FORM = NewInvoice(item_names)
        FORM.customer.datalist = customer_names
        FORM.terms.choices = TERMS

        if FORM.validate_on_submit():
                attributes = {}
                items = []
                total = 0.0
                error = None 

                attributes["invoice_num"] = FORM.invoice_num.data
                attributes["terms"] = FORM.terms.data
                if not attributes["invoice_num"]:
                        error = "Invoice Number is required"
                elif not attributes["terms"] or attributes["terms"] not in TERMS:
                        error = "Terms are missing or not valid"
                # Separate Items and Customer validation
                elif not FORM.items.entries:
                        error = "At least one item is required"
                elif not FORM.customer:
                        error = "Customer is required"
                # Validate customer existence and get customer_id
                if FORM.customer.data not in customer_names:
                        error = f"Customer not found: {FORM.customer.data}"
                else:
                        attributes["customer_id"] = customer_ids[FORM.customer]
                # Validate items and get items
                for item in FORM.items.entries:
                        if item.form.name.data not in item_names:
                                error = f"Item not recognized: {item.form.name.data}."
                                break
                        if not item.form.rate.data:
                                error = f"Rate is required for item: {item.form.name.data}"
                                break
                        total += item.form.rate.data
                        items.append(item)
                
                attributes["total"] = total
                attributes["items"] = items

                if error is None:
                        try:
                                RECORDS.new_record("INVOICE", attributes)
                        except:
                                error = "Failed to add invoice"
                        else:
                                return redirect("/invoices")

                flash(error)

        return render_template("new-invoice.jinja", customers=CUSTOMERS, terms=TERMS, items=ITEMS)
