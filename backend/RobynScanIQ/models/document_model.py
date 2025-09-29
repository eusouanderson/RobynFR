from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text, text
from sqlalchemy.orm import Mapped, mapped_column

from RobynScanIQ.database.postgres import Base


class Document(Base):
    """Modelo SQLAlchemy para a tabela de documentos."""

    __tablename__ = 'documents'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    file_name: Mapped[str] = mapped_column(String, nullable=False)
    text_content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text('NOW()'),
    )

    def to_dict(self) -> dict:
        """Converte o objeto em dict serializável para JSON."""
        created_at_value = (
            self.created_at.isoformat()
            if hasattr(self.created_at, 'isoformat')
            else self.created_at
        )

        return {
            'id': self.id,
            'file_name': self.file_name,
            'text_content': self.text_content,
            'created_at': created_at_value,
        }
