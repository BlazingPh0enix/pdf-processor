from fastapi import FastAPI, File, UploadFile, Depends, HTTPException
from datetime import datetime
from sqlalchemy.orm import Session
import uuid

from .models import get_db, Document
from .services.document_processor import DocumentProcessor

app = FastAPI(title="PDF QA Backend Service")

# Define the file upload route
@app.post("/upload")
def upload_pdf(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    try:
        # Generate a unique identifier for the PDF
        pdf_id = str(uuid.uuid4())
        file_name = file.filename
        upload_date = datetime.today()
        content = DocumentProcessor.process_document(file.file)
        # Save the PDF metadata to the database
        doc = Document(
            pdf_id=pdf_id,
            filename=file_name,
            upload_date=upload_date,
            content=content
        )
        db.add(doc)
        db.commit()

        return {"document_id": pdf_id, "message": "Document uploaded successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


# Send the chatid to the frontend
@app.get("GET/chatid/{data_id}")
def get_chatid(pdf_id: int):
    return {"chatid": pdf_id}