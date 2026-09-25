from flask import Blueprint, flash, redirect, request, render_template
from bootp1.models.RecordManager import RecordService
from sqlalchemy.exc import IntegrityError

RECORDS = RecordService()

items = Blueprint("items", __name__, template_folder="templates")

#------------------------------Items-----------------------------

@items.route("/")
def item():
        ITEMS = RECORDS.search_for_records("ITEM")
        return render_template("search-items.jinja", items = ITEMS)

@items.route("/new-item", methods=("GET", "POST"))
def new_item():
        if request.method == "POST":
                item_attributes = {}
                error = None

                item_attributes["name"] = request.form["iname"]
                item_attributes["default_description"] = request.form["description"]
                item_attributes["default_rate"] = request.form["rate"]

                if not item_attributes["name"]:
                        error = "Item name is required."
                if not item_attributes["default_description"]:
                        error = "Description is required."
                if not item_attributes["default_rate"]:
                        error = "Rate is required."
        
                if not error:
                        try:
                                RECORDS.new_record("ITEM", item_attributes)
                        except IntegrityError:
                                error = f"Failed to add item. {request.form["name"]} already exists."
                        except Exception as exc:
                                error = f"Failed to add item. {exc}"
                        else:
                                return redirect("/items")

                flash(error)

        return render_template("new-item.jinja")
