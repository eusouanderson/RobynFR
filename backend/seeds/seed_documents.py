# pylint: skip-file

from sqlalchemy.orm import Session
from RobynScanIQ.database.postgres import SessionLocal
from RobynScanIQ.models.document_model import Document

documents_seed = [
    {"file_name": "documento_1.txt", "text_content": "Conteúdo do primeiro documento."},
    {"file_name": "documento_2.txt", "text_content": "Conteúdo do segundo documento."},
    {"file_name": "documento_3.txt", "text_content": "Conteúdo do terceiro documento."},
    {"file_name": "documento_4.txt", "text_content": "Conteúdo do quarto documento."},
    {"file_name": "documento_5.txt", "text_content": "Conteúdo do quinto documento."},
    {"file_name": "documento_6.txt", "text_content": "Conteúdo do sexto documento."},
    {"file_name": "documento_7.txt", "text_content": "Conteúdo do sétimo documento."},
    {"file_name": "documento_8.txt", "text_content": "Conteúdo do oitavo documento."},
    {"file_name": "documento_9.txt", "text_content": "Conteúdo do nono documento."},
    {"file_name": "documento_10.txt", "text_content": "Conteúdo do décimo documento."},
]


def seed_documents(db: Session):
    for doc in documents_seed:
        existing = db.query(Document).filter_by(file_name=doc["file_name"]).first()
        if not existing:
            new_doc = Document(
                file_name=doc["file_name"], text_content=doc["text_content"]
            )
            db.add(new_doc)
    db.commit()
    print("Seed de documentos finalizada!")


if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed_documents(db)
    finally:
        db.close()
