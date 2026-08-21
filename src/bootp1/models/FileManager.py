import bootp1.models.FileRepository
import bootp1.models.FileStorage

class FileService:
    def upload(stream, file_name, folder_id):
        //TODO: Uploads/saves file to uploads directory.
        //Updated db accordingly (adds file entry)

    def download(id):
        //TODO: Finds file and returns file stream.

    def delete(id):
        //TODO: deletes file from uploads directory and db.

class FileRecord:
    def __init__(self, id, file_name, folder_id, size_bytes, mime_type, date_created, date_modified):
        self.id = id
        self.file_name = file_name
        self.stored_name = file_name
        self.folder_id = folder_id
        self.size_bytes = size_bytes
        self.mime_type = mime_type
        self.date_created = date_created
        self.date_modified = date_modified

    def is_previewable():
        if (self.mime_type == pdf):
            return True
        else: return False

class Folder:
    def __init__(self, id, name, parent_id):
        self.id = id
        self.name = name
        self.parent_id = parent_id

    def get_full_path():
        //recursively calls on parent Folder object.
        //object created by get_folder method in FolderRepository class.
        if (self.parent_id == None):
            return self.name

        parent = Folder(Repository.get_folder(parent_id))
        if (parent == None):
            return self.name

        return self.name + '/' + parent.get_full_path()
