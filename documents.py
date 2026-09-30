import json
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.core.database import Base, engine, get_db
from app.models.document import Document
from app.schemas.document import DocumentCreate, DocumentUpdate, DocumentResponse
from app.services.ai_service import ai_service
from app.services.export_service import export_docx, export_pdf, export_txt

Base.metadata.create_all(bind=engine)
router = APIRouter(prefix="/documents", tags=["Documents"])

@router.get("", response_model=list[DocumentResponse])
def list_documents(db: Session = Depends(get_db)):
    return db.query(Document).order_by(Document.id.desc()).all()

@router.post("/generate")
async def generate_document(payload: DocumentCreate, db: Session = Depends(get_db)):
    result = await ai_service.generate_document(payload.document_type, payload.data)
    document = Document(
        title=payload.title,
        document_type=payload.document_type,
        status="generated",
        content=json.dumps(result)
    )
    db.add(document)
    db.commit()
    db.refresh(document)
    return {"id": document.id, "document": result}

@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(document_id: int, db: Session = Depends(get_db)):
    document = db.get(Document, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document

@router.put("/{document_id}", response_model=DocumentResponse)
def update_document(document_id: int, payload: DocumentUpdate, db: Session = Depends(get_db)):
    document = db.get(Document, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    document.content = payload.content
    document.status = "edited"
    db.commit()
    db.refresh(document)
    return document

def _load(document_id, db):
    document = db.get(Document, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    data = json.loads(document.content)
    return document, data

@router.get("/{document_id}/export/{fmt}")
def export_document(document_id: int, fmt: str, db: Session = Depends(get_db)):
    document, data = _load(document_id, db)
    if fmt == "docx":
        stream = export_docx(data["title"], data["sections"])
        media = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        filename = "legalease-document.docx"
    elif fmt == "pdf":
        stream = export_pdf(data["title"], data["sections"])
        media = "application/pdf"
        filename = "legalease-document.pdf"
    elif fmt == "txt":
        stream = export_txt(data["title"], data["sections"])
        media = "text/plain"
        filename = "legalease-document.txt"
    else:
        raise HTTPException(status_code=400, detail="Unsupported format")
    return StreamingResponse(stream, media_type=media, headers={
        "Content-Disposition": f'attachment; filename="{filename}"'
    })
