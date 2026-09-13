from sqlalchemy import Update
from sqlalchemy.orm import Session

from bootp1.__init__ import create_engine_link
from bootp1.models.RecordManager import FileRecord

class Repository:
        def __init__(self):
                self.engine = create_engine_link()

        def add_record(self, record):
                with Session(self.engine) as session:
                        try:
                                session.add(record)
                        except:
                                session.rollback()
                                raise
                        else:
                                session.commit()
        def delete_record(self, record_id, record_type):
                with Session(self.engine) as session:
                        try:
                                record = session.get(record_type, record_id)
                                session.delete(record)
                        except:
                                session.rollback()
                                raise
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

