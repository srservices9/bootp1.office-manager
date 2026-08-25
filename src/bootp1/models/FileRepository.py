from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound, MultipleResultsFound

import bootp1.__init__.create_engine_rout
import bootp1.models.Section
import bootp1.models.FileRecord

class Repository:
        def __init__(self):
                self.engine = create_engine_rout()

        def add_file_to_db(self, FileRecord):
                with Session(self.engine) as session:
                        try:
                                # TODO add FileRecord object to db.
                                # handle duplicate pk exception separately.
                        except(Exception e):
                                print(e)

        def find_by_id(self, pk):
                with Session(self.engine) as session:
                        try:
                                result = session.execute(text("SELECT * FROM files WHERE file_id == :pk"),
                                                      {"pk": pk})
                                row = result.one()
                                return row
                        except(Exception e):
                                print(e)
                                return None

        def find_by_section(self, pk):
                with Session(self.engine) as session:
                        # TODO: query for files in section.
                        # Create list of FileRecords and return.
                        # Return None if folder not found.

        def search(self, text, filters):
                with Session(self.engine) as session:
                        # TODO: query for files based on text string and filters.
                        # Create list of FileRecords and return.
                        # Return None if no files found.

        def delete(self, pk):
                with Session(self.engine) as session:
                        # TODO: query to delete file from db.
                        # Returns None regardless of file existence.
