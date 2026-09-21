from sqlalchemy import Update, select
from sqlalchemy.orm import Session

from bootp1.__init__ import create_engine_link
from bootp1.models.Tables import *

class Repository:
        def __init__(self):
                self.engine = create_engine_link()
                Base.metadata.create_all(self.engine)

        def add_record(self, record) -> int:
                with Session(self.engine) as session:
                        try:
                                session.add(record)
                        except:
                                session.rollback()
                                raise Exception("Failed to add record to database.")
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
                                stmt = select(Customer)
                                if filters == None:
                                        return session.execute(stmt).fetchall()
                                if "name" in filters:
                                        stmt.where(Customer.name.ilike(f"%{filters["name"]}%"))

                                return session.execute(stmt).fetchall()
                        except:
                                session.rollback()
                                raise

        def search_invoices(self, filters=None):
                with Session(self.engine) as session:
                        try:
                                stmt = select(Invoice)
                                if filters == None:
                                        return session.execute(stmt)
                                if "name" in filters:
                                        customer = dict(self.search_customers({"name": filters["name"]})[0])
                                        customer_id = customer["record_id"]
                                        stmt.where(Invoice.customer_id == customer_id)
                                if "invoice_num" in filters:
                                        stmt.where(Invoice.invoice_num.ilike(f"%{filters["invoice_num"]}%"))
                                if "min_total" and "max_total" in filters:
                                        stmt.where(filters["min_total"] <= Invoice.total <= filters["max_total"])

                                return session.execute(stmt).fetchall()
                        except:
                                session.rollback()
                                raise

