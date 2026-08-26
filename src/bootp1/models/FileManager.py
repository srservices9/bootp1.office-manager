from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.ext.declarative import declarative_base

from bootp1.models.FileRepository import Repository
from bootp1.models.FileStorage import Storage

BASE = declarative_base()
REPO = Repository()
STORE = Storage()

class FileService:
        def upload(self, FileRecord):
                # NOTE Method called by upload form method, only for upload purposes.
                # NOTE This method adds files to the management system.
                REPO.add_file_to_db(FileRecord)
                STORE.store(FileRecord)
                # TODO: Uploads/*saves file to uploads directory.

        def download(self, pk):
                REPO.find_by_id(pk)
                # TODO: Finds file and returns file from file path.

        def delete(self, pk):
                REPO.delete(pk)
                # TODO: deletes file from uploads directory and db.

class FileRecord(BASE):
        __tablename__ = "files"
        # Attributes
        file_id:Mapped[int] = mapped_column(primary_key=True)
        name:Mapped[str]
        stored_name:Mapped[str]
        size_bytes:Mapped[int]
        mime_type:Mapped[str]
        date_created:Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                                       server_default=func.now())
        date_modified:Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                                       server_default=func.now())
        section_id:Mapped[int] = mapped_column(ForeignKey("sections.section_id"))

        def is_previewable(self):
                if (self.mime_type == "pdf"):
                        return True
                else: return False

class Section(BASE):
        __tablename__ = "sections"
        # Attributes
        section_id:Mapped[int] = mapped_column(primary_key=True)
        name:Mapped[str]
        # Relationships
        files:Mapped[FileRecord] = relationship(back_populates="sections")
