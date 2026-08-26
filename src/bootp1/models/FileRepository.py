from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound, MultipleResultsFound

from bootp1.__init__ import create_engine_link
from bootp1.models.FileManager import FileRecord, Section

class Repository:
        def __init__(self):
                self.engine = create_engine_link()

        def add_file_to_db(self, FileRecord):
                with Session(self.engine) as session:
                        try:
                                session.add(FileRecord)
                                # TODO add FileRecord object to db.
                                # handle duplicate pk exception separately.
                        except Exception:
                                print(Exception)

        def find_by_id(self, pk):
                with Session(self.engine) as session:
                        try:
                                result = session.get(FileRecord, pk)
                                return result
                        except Exception:
                                print(Exception)
                                return None

        def find_by_section(self, pk):
                with Session(self.engine) as session:
                        result = session.execute(select(FileRecord).where(FileRecord.section_id == pk))
                        # TODO: query for files in section.
                        # Create list of FileRecords and return.
                        # Return None if folder not found.

        def search(self, text, filters):
                with Session(self.engine) as session:
                        result = session.execute(select(FileRecord).where(FileRecord.stored_name.in_(text)))
                        # TODO: query for files based on text string and filters.
                        # Create list of FileRecords and return.
                        # Return None if no files found.

        def delete(self, pk):
                with Session(self.engine) as session:
                        file = session.get(FileRecord, pk)
                        session.delete(file)
                        session.commit()
                        # TODO: query to delete file from db.
                        # Returns None regardless of file existence.
