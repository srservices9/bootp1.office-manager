from datetime import datetime
from enum import Enum, auto

from sqlalchemy import DateTime, ForeignKey, except_, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.ext.declarative import declarative_base

from bootp1.models.DatabaseManager import Repository
from bootp1.models.FileStorage import Storage

BASE = declarative_base()
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
                                        
                except:
                        print(Exception)

        def new_record(self, type_value: str, record_attributes: dict) -> int | None:
                try:
                        record = self.get_record_type(type_value)(record_attributes)
                        record_id = REPO.add_record(record)
                        return record_id
                except Exception:
                        print(Exception)

        def upload_file(self, record_id: int, type_value: str, file_attributes: dict, file_stream) -> None:
                try:
                        stored_name = STORE.store(file_stream, file_attributes["file_name"], 
                                                  file_attributes["file_type"], file_attributes["section_id"])
                        
                        file_attributes["stored_name"] = stored_name
                        file_id = self.new_record("FILE", file_attributes)
                        
                        record_type = self.get_record_type(type_value)
                        REPO.add_file_to_record(file_id, record_id, record_type)
                except Exception:
                        print(Exception)

        def modify_record(self, record_id: int, type_value: str, updates: dict) -> None:
                try:
                        record_type = self.get_record_type(type_value)
                        REPO.update_record(record_id, record_type, updates)
                except Exception:
                        print(Exception)

        def delete_record(self, record_id: int, type_value: str) -> None:
                try:
                        record_type = self.get_record_type(type_value)
                        REPO.delete_record(record_id, record_type)
                except Exception:
                        print(Exception)

        def get_record_type(self, type_value: str):
                match type_value:
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
                        case "ITEM_ENTRY":
                                return ItemEntry
                        case "FILE":
                                return FileRecord
                        case "CUSTOMER":
                                return Customer
                        case _:
                                raise ValueError("Invalid Record Type")

class FileService:

        def download(self, FileRecord):
                STORE.open(FileRecord)
                # TODO: Finds file and returns file from file path.

        def delete(self, record_id, file_id):
                # TODO Call record_delete on RecordService class and FileDelete on FileManager
                record_id

# -----------------------Start of records------------------------------
# Frontend will be separated by sections.
# Each section will have an entry with file upload for supporting documentation.
# NOTE App core will call FileService.upload to add file to db,
# Then it will link the file record with the section record with the file_id returned from upload method.
class Invoice(BASE):
        __tablename__ = "invoices"
        # Attributes
        record_id:Mapped[int] = mapped_column(primary_key=True)
        invoice_num:Mapped[str]
        terms:Mapped[str]
        total:Mapped[float]

        # Foreign Keys
        customer_id:Mapped[int] = mapped_column(ForeignKey("customers.customer_id"))
        file_id:Mapped[int] = mapped_column(ForeignKey("files.file_id"))

        def __init__(self, attributes_dict) -> None:
                self.record_id = attributes_dict["record_id"]
                self.invoice_num = attributes_dict["invoice_num"]
                self.terms = attributes_dict["terms"]
                self.total = attributes_dict["total"]
                self.customer_id = attributes_dict["customer_id"]

class Estimate(BASE):
        __tablename__ = "estimates"
        # Attributes
        record_id:Mapped[int] = mapped_column(primary_key=True)
        estimate_num:Mapped[str]
        approval:Mapped[bool]
        total:Mapped[float]

        # Foreign Keys
        customer_id:Mapped[int] = mapped_column(ForeignKey("customers.record_id"))
        file_id:Mapped[int] = mapped_column(ForeignKey("files.file_id"))

        def __init__(self, attributes_dict) -> None:
                self.record_id = attributes_dict["record_id"]
                self.estimate_num = attributes_dict["estimate_num"]
                self.approval = attributes_dict["approval"]
                self.total = attributes_dict["total"]
                self.customer_id = attributes_dict["customer_id"]

class Vehicle(BASE):
        __tablename__ = "vehicles"
        # Attributes

class Insurance(BASE):
        __tablename__ = "insurances"
        # Attributes

class Customer(BASE):
        # Attributes
        __tablename__ = "customers"
        record_id:Mapped[int] = mapped_column(primary_key=True)
        name:Mapped[str]
        contact_first_name:Mapped[str]
        contact_last_name:Mapped[str]
        contact_phone:Mapped[str]

        def __init__(self, attributes_dict) -> None:
                self.record_id = attributes_dict["record_id"]
                self.name = attributes_dict["name"]
                self.contact_first_name = attributes_dict["contact_first_name"]
                self.contact_last_name = attributes_dict["contact_last_name"]
                self.contact_phone = attributes_dict["contact_phone"]

# -----------------------End of records--------------------------------
# -----------------------Start of items---------------------------------
class Item(BASE):
        __tablename__ = "items"
        # Attributes
        record_id:Mapped[int] = mapped_column(primary_key=True)
        name:Mapped[str]
        description:Mapped[str]
        cost:Mapped[float]

        def __init__(self, attributes_dict) -> None:
                self.record_id = attributes_dict["record_id"]
                self.name = attributes_dict["name"]
                self.description = attributes_dict["description"]
                self.cost = attributes_dict["cost"]

class ItemEntry(BASE):
        __tablename__ = "item_entries"
        # Attributes
        record_id:Mapped[int] = mapped_column(primary_key=True)
        description:Mapped[str]
        quantity:Mapped[int]
        rate:Mapped[float]
        amount:Mapped[float]

        # Foreign Keys
        invoice_id:Mapped[int] = mapped_column(ForeignKey("invoices.invoice_id"))
        estimate_id:Mapped[int] = mapped_column(ForeignKey("estimates.estimate_id"))
        item_id:Mapped[int] = mapped_column(ForeignKey("items.item_id"))
        
# -----------------------End of items-----------------------------------
# -----------------------Start of Files---------------------------------
class FileRecord(BASE):
        __tablename__ = "files"
        # Attributes
        record_id:Mapped[int] = mapped_column(primary_key=True)
        name:Mapped[str]
        size_bytes:Mapped[int]
        mime_type:Mapped[str]
        date_uploaded:Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                                       server_default=func.now())
        # Foreign Keys
        section_id:Mapped[int] = mapped_column(ForeignKey("sections.section_id"))
        
        # Relationships
        invoices:Mapped[Invoice] = relationship(back_populates="invoices")

        # Special Attribute
        stored_name:Mapped[str]

        def __init__(self, attributes_dict) -> None:
                self.record_id = attributes_dict["record_id"]
                self.name = attributes_dict["name"]
                self.size_bytes = attributes_dict["size_bytes"]
                self.mime_type = attributes_dict["mime_type"]
                self.date_uploaded = attributes_dict["date_uploaded"]
                self.section_id = attributes_dict["section_id"]
                self.stored_name = attributes_dict["stored_name"]

        def is_previewable(self):
                if (self.mime_type == "pdf"):
                        return True
                else: return False

class SectionTag(BASE):
        __tablename__ = "sections"
        # Attributes
        section_id:Mapped[int] = mapped_column(primary_key=True)
        name:Mapped[str]
        # Relationships
        files:Mapped[FileRecord] = relationship(back_populates="sections")

class Filters(Enum):
        # Declaring filters for the search function in REPO as enums to specify filter options
        FILE_NAME = auto()
        DATE_RANGE = auto()
        SECTION = auto()
        AMOUNT = auto()

# ----------------------End of Files--------------------------------------
