from fastapi import FastAPI, File, UploadFile, Depends, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from sqlalchemy.orm import Session
import uuid
from pydantic import BaseModel

from models import get_db, Document
from services.document_processor import DocumentProcessor
from services.websocket_manager import manager

app = FastAPI(title="PDF QA Backend Service")

# Update CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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

class Question(BaseModel):
    question: str

@app.post("/chat/{pdf_id}")
async def chat_with_pdf(pdf_id: str, question: Question, db: Session = Depends(get_db)):
    try:
        # Retrieve the document from database
        doc = db.query(Document).filter(Document.pdf_id == pdf_id).first()
        if not doc:
            raise HTTPException(status_code=404, detail="Document not found")

        # Get answer using DocumentProcessor
        answer = document_processor.answer_question(doc.content, question.question)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Add WebSocket endpoint
@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str, db: Session = Depends(get_db)):
    print(f"New WebSocket connection request from client: {client_id}")  # Debug log
    try:
        await manager.connect(websocket, client_id)
        print(f"Client {client_id} connected successfully")  # Debug log
        
        while True:
            try:
                data = await websocket.receive_json()
                print(f"Received message from client {client_id}: {data}")  # Debug log
                
                # Process the question and get answer
                doc = db.query(Document).filter(Document.pdf_id == data["document_id"]).first()
                if not doc:
                    await manager.send_message({
                        "error": "Document not found"
                    }, client_id)
                    continue

                answer = document_processor.answer_question(doc.content, data["question"])
                
                # Send response back to client
                await manager.send_message({
                    "answer": answer,
                    "question": data["question"]
                }, client_id)

            except WebSocketDisconnect:
                print(f"Client {client_id} disconnected")  # Debug log
                break
            except Exception as e:
                print(f"Error processing message: {str(e)}")  # Debug log
                await manager.send_message({
                    "error": f"Error processing message: {str(e)}"
                }, client_id)
                
    except Exception as e:
        print(f"WebSocket error: {str(e)}")  # Debug log
        manager.disconnect(client_id)