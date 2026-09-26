from flask import Blueprint, flash, redirect, request, render_template
from ..models.RecordManager import RecordService
from sqlalchemy.exc import IntegrityError


customers = Blueprint("customers", "customer", template_folder="templates")

RECORDS = RecordService()
#------------------------------Customers-----------------------------

@customers.route("/")
def customer():
        CUSTOMERS = RECORDS.search_for_records("CUSTOMER")
        return render_template("search-customers.jinja", customers=CUSTOMERS)

@customers.route("/new-customer", methods=("GET", "POST"))
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
                                RECORDS.new_record("CUSTOMER", customer_attributes)
                        except IntegrityError:
                                error = f"Failed to add customer. {request.form["cname"]} already exists."
                        except Exception as exc:
                                error = f"Failed to add customer. {exc}"
                        else:
                                return redirect("/customers")

                flash(error)
                
        return render_template("new-customer.jinja")

#------------------------------Items-----------------------------

@customers.route("/items")
def items():
        ITEMS = RECORDS.search_for_records("ITEM")
        return render_template("search-items.jinja", items = ITEMS)
