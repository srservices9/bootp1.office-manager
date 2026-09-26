from sqlalchemy import Update, create_engine, select
from sqlalchemy.exc import MultipleResultsFound
from sqlalchemy.orm import Session

from .Tables import *
from ..config import Config

class Repository:
        def __init__(self):
                self.engine = create_engine(Config.DATABASE_URL, echo=True)
                # Base.metadata.drop_all(self.engine)
                Base.metadata.create_all(self.engine)

        def add_record(self, record) -> int:
                with Session(self.engine) as session:
                        try:
                                session.add(record)
                        except:
                                session.rollback()
                                raise
                        else:
                                session.commit()
                                return record.record_id
        def delete_record(self, record_id, record_type):
                with Session(self.engine) as session:
                        try:
                                record = session.get(record_type, record_id)
                                session.delete(record)
                        except:
                                session.rollback()
                                raise Exception("Failed to delete record from database.")
                        else:
                                session.commit()
        
        def add_file_to_record(self, file_id, record_id, record_type):
                with Session(self.engine) as session:
                        try:
                                # Update record to hold file_id
                                record = session.get(record_type, record_id)
                                if record == None:
                                        raise Exception("Record not found.")
                                file = session.get(FileRecord, file_id)
                                if file == None:
                                        raise Exception("FileRecord not found")

                                session.execute(Update(record).where(
                                        record.record_id == record_id).values({"file_id": file_id}))
                                if not session.is_modified(record):
                                        raise Exception(f"Unable to add file: {file} to record: {record}")
                        except:
                                session.rollback()
                                raise
                        else:
                                session.commit()

        def update_record(self, record_id, record_type, updates):
                with Session(self.engine) as session:
                        try:
                                record = session.get(record_type, record_id)
                                if record == None:
                                        raise Exception("Record not found.")

                                session.execute(Update(record).where(
                                        record.record_id == record_id).values(updates))
                                if not session.is_modified(record):
                                        raise Exception(f"Unable to update record: {record}")
                        except:
                                session.rollback()
                                raise
                        else:
                                session.commit()

#------------------------------SECTION SEARCH METHODS----------------------------------
        def search_customers(self, filters):
                with Session(self.engine) as session:
                        try:
                                result = None
                                stmt = select(Customer)

                                if filters == None:
                                        result = session.scalars(stmt).all()
                                # "match" key provided determines if trying to find specific row.
                                elif "name" in filters and "match" in filters:
                                        stmt = stmt.where(Customer.name == filters["name"])
                                        result = session.scalars(stmt).one_or_none()
                                elif "name" not in filters and "match" in filters:
                                        raise ValueError("Name not provided.")

                                else:
                                        if "name" in filters:
                                                stmt = stmt.where(Customer.name.ilike(f"%{filters["name"]}%"))

                                        result = session.scalars(stmt).all()
                        except MultipleResultsFound:
                                session.rollback()
                                raise ValueError("Multiple results found")
                        except:
                                session.rollback()
                                raise
                        else:
                                return result

        def search_invoices(self, filters):
                with Session(self.engine) as session:
                        try:
                                result = None
                                stmt = select(Invoice)

                                if filters == None:
                                        result = session.scalars(stmt).all()
                                # "match" key provided determines if trying to find specific row.
                                elif "invoice_num" in filters and "match" in filters:
                                        stmt = stmt.where(Invoice.invoice_num == filters["invoice_num"])
                                        result = session.scalars(stmt).one_or_none()
                                elif "invoice_num" not in filters and "match" in filters:
                                        raise ValueError("Invoice number not provided")

                                else:
                                        if "customer_id" in filters:
                                                stmt = stmt.where(Invoice.customer_id == filters["customer_id"])
                                        if "invoice_num" in filters:
                                                stmt = stmt.where(Invoice.invoice_num.ilike(f"%{filters["invoice_num"]}%"))
                                        if "min_total" and "max_total" in filters:
                                                if filters["min_total"] > filters["max_total"]:
                                                        raise ValueError("Minimum total cannot be higher than maximum total")
                                                stmt = stmt.where(filters["min_total"] <= Invoice.total <= filters["max_total"])
                                        elif "min_total" in filters:
                                                stmt = stmt.where(filters["min_total"] <= Invoice.total)
                                        elif "max_total" in filters:
                                                stmt = stmt.where(Invoice.total <= filters["max_total"])

                                        result = session.scalars(stmt).all()
                        except:
                                session.rollback()
                                raise
                        else:
                                return result

        def search_items(self, filters):
                with Session(self.engine) as session:
                        try:
                                result = None
                                stmt = select(Item)

                                if filters == None:
                                        result = session.scalars(stmt).all()
                                elif "name" in filters and "match" in filters:
                                        stmt = stmt.where(Item.name == filters["name"])
                                        result = session.scalars(stmt).one_or_none()
                                elif "name" not in filters and "match" in filters:
                                        raise ValueError("Item name not provided")

                                else:
                                        if "name" in filters:
                                                stmt = stmt.where(Item.name.ilike(f"%{filters["name"]}%"))
                                        if "description" in filters:
                                                stmt = stmt.where(Item.default_description.ilike(f"%{filters["description"]}%"))
                                        if "min_rate" and "max_rate" in filters:
                                                if filters["min_rate"] > filters["max_rate"]:
                                                        raise ValueError("Minimum rate cannot be higher than maximum rate")
                                                stmt = stmt.where(filters["min_rate"] <= Item.default_rate <= filters["max_rate"])
                                        elif "min_rate" in filters:
                                                stmt = stmt.where(filters["min_rate"] <= Item.default_rate)
                                        elif "max_rate" in filters:
                                                stmt = stmt.where(Item.default_rate <= filters["max_rate"])

                                        result = session.scalars(stmt).all()
                        except:
                                session.rollback()
                                raise
                        else:
                                return result
