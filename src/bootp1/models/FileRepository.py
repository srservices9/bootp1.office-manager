from sqlalchemy import select
from sqlalchemy.orm import Session

from bootp1.__init__ import create_engine_link
from bootp1.models.FileManager import FileRecord, Section

class Repository:
        def __init__(self):
                self.engine = create_engine_link()

        def add_file_to_db(self, FileRecord):
                with Session(self.engine) as session:
                        try:
                                session.add(FileRecord)
                                print(session.new)
                                session.commit()
                        except Exception:
                                print(Exception)

        def find_by_id(self, pk):
                with Session(self.engine) as session:
                        try:
                                # TODO Check if FileRecord not found.
                                result = session.get(FileRecord, pk)
                                return result
                        except Exception:
                                print(Exception)
                                return None

        def find_by_section(self, pk):
                with Session(self.engine) as session:
                        result = session.execute(select(FileRecord).where(FileRecord.section_id == pk))
                        return result

        def search(self, text, filters):
                with Session(self.engine) as session:
                        result = session.execute(select(FileRecord).where(FileRecord.stored_name.in_(text)))
                        # TODO: Search by filters and append to result.
                        return result

        def delete(self, pk):
                with Session(self.engine) as session:
                        file = session.get(FileRecord, pk)
                        session.delete(file)
                        session.commit()
                        # TODO check if FileRecord not found.
