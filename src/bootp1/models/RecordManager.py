import traceback
from bootp1.models.Tables import *
from bootp1.models.DatabaseManager import Repository
from bootp1.models.FileStorage import Storage

REPO = Repository()
STORE = Storage()

class RecordService:
        def search_for_records(self, type_value: str, filters=None):
                try:
                        record_type = self.get_record_type(type_value)
                        if record_type is Invoice:
                                return REPO.search_invoices(filters)
                        if record_type is Customer:
                                return REPO.search_customers(filters)
                        if record_type is Item:
                                return REPO.search_items(filters)
                except:
                        raise

        def new_record(self, type_value: str, record_attributes: dict) -> None:
                try:
                        record = self.get_record_type(type_value)(record_attributes)
                        if record is Invoice:
                                invoice_id = REPO.add_record(record)
                                for item in record_attributes["items"]:
                                        item["invoice_id"] = invoice_id
                                        item_entry = ItemEntry(item)
                                        REPO.add_record(item_entry)
                        else:
                                REPO.add_record(record)
                except:
                        traceback.print_exc()

        def upload_file(self, record_id: int, type_value: str, file_attributes: dict, file_stream) -> None:
                try:
                        stored_name = STORE.store(file_stream, file_attributes["file_name"], 
                                                  file_attributes["file_type"], file_attributes["section_id"])
                        
                        file_attributes["stored_name"] = stored_name
                        file_id = self.new_record("FILE", file_attributes)
                        
                        record_type = self.get_record_type(type_value)
                        REPO.add_file_to_record(file_id, record_id, record_type)
                except:
                        traceback.print_exc()

        def modify_record(self, record_id: int, type_value: str, updates: dict) -> None:
                try:
                        record_type = self.get_record_type(type_value)
                        REPO.update_record(record_id, record_type, updates)
                except:
                        traceback.print_exc()

        def delete_record(self, record_id: int, type_value: str) -> None:
                try:
                        record_type = self.get_record_type(type_value)
                        REPO.delete_record(record_id, record_type)
                except:
                        traceback.print_exc()

        def get_record_type(self, type_value: str):
                match type_value:
                        case "CUSTOMER":
                                return Customer
                        case "INVOICE":
                                return Invoice
                        case "ESTIMATE":
                                return Estimate
                        case "VEHICLE":
                                return Vehicle
                        case "INSURANCE":
                                return Insurance
                        case "ITEM":
                                return Item
                        case "FILE":
                                return FileRecord
                        case _:
                                raise ValueError("Invalid Record Type")

class FileService:

        def download(self, FileRecord):
                STORE.open(FileRecord)
                # TODO: Finds file and returns file from file path.

        def delete(self, record_id, file_id):
                # TODO Call record_delete on RecordService class and FileDelete on FileManager
                pass

