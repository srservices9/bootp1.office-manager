from flask_wtf import FlaskForm

from bootp1.models.filemanager.FileManager import FileRecord, SectionTag

class Storage:
    def store(self, file_stream, file_name, file_type, section_id):
        stored_name = file_name + file_type
        # TODO: generate stored_name == uuid + safe extension
        # Write file and count size.
        # return stored_name and file_size
        return stored_name

    def open(self, stored_name):
        # TODO: opens file and return file stream.

    def delete(self, stored_name):
        # TODO: removes file from uploads directory.
