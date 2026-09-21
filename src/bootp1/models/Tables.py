from datetime import datetime
from typing import List, Optional

from sqlalchemy import DateTime, ForeignKey, func, null
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column

class Base(DeclarativeBase):
        pass
# -----------------------Start of records------------------------------
class Invoice(Base):
        __tablename__ = "invoices"
        # Attributes
        record_id:Mapped[int] = mapped_column(primary_key=True)
        invoice_num:Mapped[str]
        terms:Mapped[str]
        total:Mapped[float]

        # Foreign Keys
        customer_id:Mapped[int] = mapped_column(ForeignKey("customers.record_id"))
        file_id:Mapped[int] = mapped_column(ForeignKey("files.record_id"), nullable=True)

        # Relationships
        file:Mapped[Optional["FileRecord"]] = relationship(back_populates="invoice")

        def __init__(self, attributes_dict) -> None:
                self.record_id = attributes_dict["record_id"]
                self.invoice_num = attributes_dict["invoice_num"]
                self.terms = attributes_dict["terms"]
                self.total = attributes_dict["total"]
                self.customer_id = attributes_dict["customer_id"]

class Estimate(Base):
        __tablename__ = "estimates"
        # Attributes
        record_id:Mapped[int] = mapped_column(primary_key=True)
        estimate_num:Mapped[str]
        approval:Mapped[bool]
        total:Mapped[float]

        # Foreign Keys
        customer_id:Mapped[int] = mapped_column(ForeignKey("customers.record_id"))
        file_id:Mapped[int] = mapped_column(ForeignKey("files.record_id"), nullable=True)

        def __init__(self, attributes_dict) -> None:
                self.record_id = attributes_dict["record_id"]
                self.estimate_num = attributes_dict["estimate_num"]
                self.approval = attributes_dict["approval"]
                self.total = attributes_dict["total"]
                self.customer_id = attributes_dict["customer_id"]

class Vehicle(Base):
        __tablename__ = "vehicles"
        # Attributes
        record_id:Mapped[int] = mapped_column(primary_key=True)

        def __init__(self, attributes_dict) -> None:
                self.record_id = attributes_dict["record_id"]

class Insurance(Base):
        __tablename__ = "insurances"
        # Attributes
        record_id:Mapped[int] = mapped_column(primary_key=True)

        def __init__(self, attributes_dict) -> None:
                self.record_id = attributes_dict["record_id"]

class Customer(Base):
        # Attributes
        __tablename__ = "customers"
        record_id:Mapped[int] = mapped_column(primary_key=True)
        name:Mapped[str]
        contact_first_name:Mapped[Optional[str]]
        contact_last_name:Mapped[Optional[str]]
        contact_phone:Mapped[Optional[str]]

        def __init__(self, attributes_dict) -> None:
                if "record_id" in attributes_dict: 
                        self.record_id = attributes_dict["record_id"]
                if "name" in attributes_dict: 
                        self.name = attributes_dict["name"]
                if "contact_first_name" in attributes_dict: 
                        self.contact_first_name = attributes_dict["contact_first_name"]
                if "contact_last_name" in attributes_dict: 
                        self.contact_last_name = attributes_dict["contact_last_name"]
                if "contact_phone" in attributes_dict: 
                        self.contact_phone = attributes_dict["contact_phone"]

# -----------------------End of records--------------------------------
# -----------------------Start of items---------------------------------
class Item(Base):
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

class ItemEntry(Base):
        __tablename__ = "item_entries"
        # Attributes
        record_id:Mapped[int] = mapped_column(primary_key=True)
        description:Mapped[str]
        quantity:Mapped[int]
        rate:Mapped[float]
        amount:Mapped[float]

        # Foreign Keys
        invoice_id:Mapped[int] = mapped_column(ForeignKey("invoices.record_id"), nullable=True)
        estimate_id:Mapped[int] = mapped_column(ForeignKey("estimates.record_id"), nullable=True)
        item_id:Mapped[int] = mapped_column(ForeignKey("items.record_id"))
        
# -----------------------End of items-----------------------------------
# -----------------------Start of Files---------------------------------
class FileRecord(Base):
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
        section:Mapped[List["SectionTag"]] = relationship(back_populates="file")
        invoice:Mapped[Invoice] = relationship(back_populates="file")

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

class SectionTag(Base):
        __tablename__ = "sections"
        # Attributes
        section_id:Mapped[int] = mapped_column(primary_key=True)
        name:Mapped[str]
        # Relationships
        file:Mapped[FileRecord] = relationship(back_populates="section")

# ----------------------End of Files--------------------------------------
