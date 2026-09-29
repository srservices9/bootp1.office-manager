from flask import Blueprint, flash, redirect, request, render_template
from ..models.RecordManager import RecordService
from ..forms.ItemForms import *
from sqlalchemy.exc import IntegrityError

RECORDS = RecordService()

items = Blueprint("items", "item", template_folder="templates")

#------------------------------Items-----------------------------

@items.route("/", methods=("GET", "POST"))
def item():
        ITEMS = RECORDS.search_for_records("ITEM")
        FORM = Items()
        if ITEMS:
                data = [item.name for item in ITEMS]
                FORM.name.datalist = data
        else:
                FORM.name.datalist = []

        if request.method == "POST":
                filters = None
                error = None
                no_filters = all(value is None for value in FORM.data)
                if not no_filters:
                        filters = {}
                        if FORM.name.data:
                                filters["name"] = FORM.name.data
                        if FORM.description.data:
                                filters["description"] = FORM.description.data
                        if FORM.min_rate.data:
                                filters["min_rate"] = FORM.min_rate.data
                        if FORM.max_rate.data:
                                filters["max_rate"] = FORM.max_rate.data

                        if "min_rate" in filters and "max_rate" in filters:
                                if filters["min_rate"] > filters["max_rate"]:
                                        error = "Minimum rate cannot be higher than maximum rate"

                        # Flushing form values to prevent previously submitted data from affecting new submits.
                        FORM.name.data = None
                        FORM.description.data = None
                        FORM.min_rate.data = None
                        FORM.max_rate.data = None

                if not error:
                        try:
                                RESULTS = RECORDS.search_for_records("ITEM", filters)
                        except Exception as exc:
                                error = f"Failed to search for items: {exc}"
                        else:
                                return render_template("search-items.jinja", results=RESULTS, form=FORM)

                flash(error)

        return render_template("search-items.jinja", form=FORM)

@items.route("/new-item", methods=("GET", "POST"))
def new_item():
        FORM = NewItem()
        if request.method == "POST":
                attributes = {}
                error = None

                attributes["name"] = FORM.name.data
                attributes["default_description"] = FORM.default_description.data
                attributes["default_rate"] = FORM.default_rate.data

                if not attributes["name"]:
                        error = "Item name is required."
                if not attributes["default_description"]:
                        error = "Description is required."
                if not attributes["default_rate"]:
                        error = "Rate is required."
                # Flushing form values to prevent previously submitted data from affecting new submits.
                FORM.name.data = None
                FORM.default_description.data = None
                FORM.default_rate.data = None
        
                if not error:
                        try:
                                RECORDS.new_record("ITEM", attributes)
                        except IntegrityError:
                                error = f"Failed to add item. {attributes["name"]} already exists."
                        except Exception as exc:
                                error = f"Failed to add item. {exc}"
                        else:
                                return redirect("/items")

                flash(error)

        return render_template("new-item.jinja", form=FORM)
