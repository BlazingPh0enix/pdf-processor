# PDF Document Chat Application

A web application that allows users to upload PDF documents and chat with their contents using AI.

## Features

- PDF document upload and processing
- Real-time chat with document contents using AI
- WebSocket-based communication
- Vector-based document search
- Responsive UI with drag-and-drop support

## Prerequisites

- Python 3.8 or higher
- OpenAI API key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/BlazingPh0enix/pdf-processor
cd pdf-processor
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory and add the following environment variables:
```bash
OPENAI_API_KEY=your_openai_api_key_here
DATABASE_URL=sqlite:///./pdf_database.db
```

# Running the Application

1. Start the backend server:
```bash
cd src
uvicorn main:app --reload
```

2. Serve the frontend using Microsoft's [Live Server](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer) extension for Visual Studio Code.

# Usage

1. Upload a PDF document by dragging and dropping it onto the upload area.
2. Wait for the document to be processed.
3. Chat with the document using the chat interface.
4. Use the back button to upload a different document.

# Project Structure

```
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
├── src/
│   ├── models.py
│   ├── main.py
│   └── services/
│       ├── document_processor.py
│       └── websocket_manager.py
├── .env
├── requirements.txt
└── README.md
```

# Technical Details

- Backend: FastAPI, Uvicorn, SQLAlchemy, WebSockets
- Frontend: HTML, CSS, JavaScript
- Document Processing: PyPDF2, LangChain with OpenAI
- Vector Store: FAISS
- Database: SQLite

# Limitations

- Maximum document size: 10 MB
- Supported document formats: PDF
- Requires active internet connection for AI processing