from sqlalchemy import Update, select
from sqlalchemy.orm import Session

from bootp1.__init__ import create_engine_link
from bootp1.models.Tables import *

class Repository:
        def __init__(self):
                self.engine = create_engine_link()
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
                                        stmt.where(Customer.name == filters["name"])
                                        result = session.scalars(stmt).one_or_none()
                                elif "name" not in filters and "match" in filters:
                                        raise ValueError("Name not provided.")

                                else:
                                        if "name" in filters:
                                                stmt.where(Customer.name.ilike(f"%{filters["name"]}%"))

                                        result = session.scalars(stmt).all()
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
                                        result = session.execute(stmt).all()
                                # "match" key provided determines if trying to find specific row.
                                elif "invoice_num" in filters and "match" in filters:
                                        stmt.where(Invoice.invoice_num == filters["invoice_num"])
                                        result = session.execute(stmt).one_or_none()
                                elif "invoice_num" not in filters and "match" in filters:
                                        raise ValueError("Invoice number not provided")

                                else:
                                        if "customer_id" in filters:
                                                stmt.where(Invoice.customer_id == filters["customer_id"])
                                        if "invoice_num" in filters:
                                                stmt.where(Invoice.invoice_num.ilike(f"%{filters["invoice_num"]}%"))
                                        if "min_total" and "max_total" in filters:
                                                stmt.where(filters["min_total"] <= Invoice.total <= filters["max_total"])
                                        if "min_total" in filters and "max_total" not in filters:
                                                stmt.where(filters["min_total"] <= Invoice.total)
                                        if "max_total" in filters and "min_total" not in filters:
                                                stmt.where(Invoice.total <= filters["max_total"])

                                        result = session.scalars(stmt).all()
                        except:
                                session.rollback()
                                raise
                        else:
                                return result

