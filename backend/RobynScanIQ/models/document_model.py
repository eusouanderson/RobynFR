from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from RobynScanIQ.database.postgree import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String, nullable=False)
    text_content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
