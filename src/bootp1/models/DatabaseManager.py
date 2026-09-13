from sqlalchemy import Update
from sqlalchemy.orm import Session

from bootp1.__init__ import create_engine_link
from bootp1.models.RecordManager import *

class Repository:
        def __init__(self):
                self.engine = create_engine_link()

        def add_record_to_db(self, record):
                with Session(self.engine) as session:
                        try:
                                session.add(record)
                                print(session.new)
                                session.commit()
                        except Exception:
                                print(Exception)
        
        def add_file_to_record(self, file_id, record):
                with Session(self.engine) as session:
                        session.execute(Update(record).where())
                        # TODO Update record to hold foreign-key of file

        def update_record(self, record, record_type, updates):
                with Session(self.engine) as session:
                        try:
                                session.execute(Update(record_type).where(
                                        record_type.record_id == record.record_id).values(updates))
                                session.commit()
                                print(record)
                        except Exception:
                                print(Exception)
                        

        def delete(self, pk):
                with Session(self.engine) as session:
                        file = session.get(FileRecord, pk)
                        session.delete(file)
                        session.commit()
                        # TODO check if FileRecord not found.
