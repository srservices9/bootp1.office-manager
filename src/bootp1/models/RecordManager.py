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
        def new_record(self, type_value, record_attributes):
                record = self.get_record_type(type_value)
                REPO.add_record(record)
                # TODO Finish record method.
                # TODO For both new_record and upload_file methods:
                # Need to figure out way to take list or dict of attributes
                # and dynamically create record to pass to db manager

        def upload_file(self, record_id, record_type, file_attributes, file_stream):
                # TODO adapt method to use dynamic record system and create and add file & FileRecord
                stored_name = STORE.store(file_stream, file_name, file_type, section_id)

                file = FileRecord(name=file_name, stored_name=stored_name, size_bytes=file_size, 
                                  mime_type=file_type, section_id=section_id)
                file_id = RecordService.new_record(file)

                REPO.add_file_to_record(record_id, file_id)

        def modify_record(self, record_id, type_value, updates_dict):
                try:
                        record_type = self.get_record_type(type_value)
                        REPO.update_record(record_id, record_type, updates_dict)
                except Exception:
                        print(Exception)

        def delete_record(self, record_id, type_value):
                try:
                        record_type = self.get_record_type(type_value)
                        REPO.delete_record(record_id, record_type)
                except Exception:
                        print(Exception)

        def get_record_type(self, type_value):
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
                        case _:
                                return ValueError("Invalid Record Type")

class FileService:

        def download(self, FileRecord):
                STORE.open(FileRecord)
                # TODO: Finds file and returns file from file path.

        def delete(self, record_id, file_id):
                # TODO Call record_delete on RecordService class and FileDelete on FileManager

# -----------------------Start of sections------------------------------
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

class Estimate(BASE):
        __tablename__ = "estimates"
        # Attributes
        record_id:Mapped[int] = mapped_column(primary_key=True)
        estimate_num:Mapped[str]
        approval:Mapped[bool]
        total:Mapped[float]

        # Foreign Keys
        customer_id:Mapped[int] = mapped_column(ForeignKey("customers.customer_id"))
        file_id:Mapped[int] = mapped_column(ForeignKey("files.file_id"))

class Vehicle(BASE):
        __tablename__ = "vehicles"
        # Attributes

class Insurance(BASE):
        __tablename__ = "insurances"
        # Attributes

# -----------------------End of sections--------------------------------
# -----------------------Start of items---------------------------------
class Item(BASE):
        __tablename__ = "items"
        # Attributes
        record_id:Mapped[int] = mapped_column(primary_key=True)
        name:Mapped[str]
        description:Mapped[str]
        cost:Mapped[float]

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
