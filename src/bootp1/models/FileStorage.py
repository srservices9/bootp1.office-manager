from flask-wtf import FlaskForm

from bootp1.models.FileManager import FileRecord, Section

class Storage:
    def store(self, FileRecord):
        # TODO: generate stored_name == uuid + safe extension
        # Write file and count size.
        # return stored_name and file_size

    def open(self, stored_name):
        # TODO: opens file and return file stream.

    def delete(self, stored_name):
        # TODO: removes file from uploads directory.
