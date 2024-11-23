from fastapi import FastAPI, File, UploadFile, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from sqlalchemy.orm import Session
import uuid

from models import get_db, Document
from services.document_processor import DocumentProcessor

app = FastAPI(title="PDF QA Backend Service")

# Update CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Add your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Initialize DocumentProcessor at module level
document_processor = DocumentProcessor()

# Define the file upload route
@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    try:
        # Generate a unique identifier for the PDF
        pdf_id = str(uuid.uuid4())
        file_name = file.filename
        upload_date = datetime.today()
        
        # Process the document using instance method
        content = document_processor.process_document(file.file)
        
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


# Fix the endpoint format - remove GET from path
@app.get("/chatid/{pdf_id}")  # Changed from "GET/chatid/{data_id}"
async def get_chatid(pdf_id: str):
    try:
        return {"chatid": pdf_id, "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))