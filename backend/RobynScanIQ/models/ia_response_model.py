from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, text
from sqlalchemy.orm import Mapped, mapped_column

from RobynScanIQ.database.postgres import Base


class IAResponse(Base):
    """Modelo SQLAlchemy para a tabela de respostas de IA."""

    __tablename__ = 'ia_responses'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    question: Mapped[str] = mapped_column(String, nullable=False)
    answer: Mapped[str] = mapped_column(Text, nullable=False)
    document_id: Mapped[int] = mapped_column(Integer, ForeignKey('documents.id'), nullable=False)
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
            'question': self.question,
            'answer': self.answer,
            'document_id': self.document_id,
            'created_at': created_at_value,
        }
