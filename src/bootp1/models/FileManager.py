from datetime import datetime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.ext.declarative import declarative_base

import bootp1.models.FileRepository
import bootp1.models.FileStorage

BASE = declarative_base

class FileService:
        def upload(self, stream, file_name, section_id):
                # TODO: Uploads/*saves file to uploads directory.
                # Updated db accordingly (adds file entry)

        def download(self, pk):
                # TODO: Finds file and returns file stream.

        def delete(self, pk):
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
                if (self.mime_type == pdf):
                        return True
                else: return False

class Section(BASE):
        __tablename__ = "sections"
        # Attributes
        section_id:Mapped[int] = mapped_column(primary_key=True)
        name:Mapped[str]
        # Relationships
        files:Mapped[FileRecord] = relationship(back_populates("sections")
