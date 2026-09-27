from flask import Blueprint, flash, redirect, request, render_template
from ..models.RecordManager import RecordService
from sqlalchemy.exc import IntegrityError

from ..forms.CustomerForms import *

customers = Blueprint("customers", "customer", template_folder="templates")

RECORDS = RecordService()
#------------------------------Customers-----------------------------

@customers.route("/", methods=("GET", "POST"))
def customer():
        CUSTOMERS = RECORDS.search_for_records("CUSTOMER")
        FORM = Customers()
        if CUSTOMERS:
                data = [customer.name for customer in CUSTOMERS]
                FORM.name.datalist = data
        else:
                FORM.name.datalist = []

        if request.method == "POST":
                filters = {}
                error = None
                no_filters = all(value is None for value in FORM.data)
                if not no_filters:
                        if FORM.name.data:
                                filters["name"] = FORM.name.data
                        if FORM.contact_first_name.data:
                                filters["contact_first_name"] = FORM.contact_first_name.data
                        if FORM.contact_last_name.data:
                                filters["contact_last_name"] = FORM.contact_last_name.data
                        if FORM.contact_phone.data:
                                filters["contact_phone"] = FORM.contact_phone.data

                        # Flushing form values to prevent previously submitted data from affecting new submits.
                        FORM.name.data = None
                        FORM.contact_first_name.data = None
                        FORM.contact_last_name.data = None
                        FORM.contact_phone.data = None

                        if not error:
                                try:
                                        RESULTS = RECORDS.search_for_records("CUSTOMER", filters)
                                except Exception as exc:
                                        error = f"Failed to search for customers: {exc}"
                                else:
                                        return render_template("search-customers.jinja", form=FORM, results=RESULTS)

                        flash(error)

        return render_template("search-customers.jinja", form=FORM)

@customers.route("/new-customer", methods=("GET", "POST"))
def new_customer():
        FORM = NewCustomer()
        if request.method == "POST":
                attributes = {}
                error = None 

                attributes["name"] = FORM.name.data
                if not attributes["name"]:
                        error = "Customer name is required"

                elif FORM.contact_first_name.data:
                        attributes["contact_first_name"] = FORM.contact_first_name.data
                if FORM.contact_last_name:
                        attributes["contact_last_name"] = FORM.contact_last_name.data
                if FORM.contact_phone:
                        attributes["contact_phone"] = FORM.contact_phone.data

                # Flushing form values to prevent previously submitted data from affecting new submits.
                FORM.name.data = None
                FORM.contact_first_name.data = None
                FORM.contact_last_name.data = None
                FORM.contact_phone.data = None

                if error is None:
                        try:
                                RECORDS.new_record("CUSTOMER", attributes)
                        except IntegrityError:
                                error = f"Failed to add customer. {request.form["cname"]} already exists."
                        except Exception as exc:
                                error = f"Failed to add customer. {exc}"
                        else:
                                return redirect("/customers")

                flash(error)

        return render_template("new-customer.jinja", form=FORM)
