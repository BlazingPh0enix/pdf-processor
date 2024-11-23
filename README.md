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
git clone <repository-url>
cd <repository-name>
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
uvicorn main:app --reload --port 8000 --host 127.0.0.1
```

2. Serve the frontend using either Python's built-in HTTP server or any other static file server:
```bash
python -m http.server 5500 --directory frontend
```

3. Open `http://localhost:5500` in your browser.

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