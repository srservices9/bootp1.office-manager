from bootp1.__init__ import create_engine

class Repository:
    def __init__(self):
        self.engine = create_engine()

    def get_folder(id):
        with engine.connect() as conn:
            //TODO: query for folder.
            //Create Folder and return.
            //return none if folder not found.

    def find_by_id(id):
        with engine.connect() as conn:
            //TODO: query for file.
            //Create FileRecord and return.
            //Return None if file not found.

    def find_by_folder(folder_id):
        with engine.connect() as conn:
            //TODO: query for files in folder.
            //Create list of FileRecords and return.
            //Return None if folder not found.

    def search(text, filters):
        with engine.connect() as conn:
            //TODO: query for files based on text string and filters.
            //Create list of FileRecords and return.
            //Return None if no files found.

    def delete(id):
        with engine.connect() as conn:
            //TODO: query to delete file from db.
            //Returns None regardless of file existence.
