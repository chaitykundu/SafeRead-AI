# SafeRead-AI

# SafeRead AI – Child-Safe Book Analysis System

SafeRead AI is an **AI-powered book safety analysis platform** designed to help parents, educators, and guardians determine whether a book is suitable for children.

The system scans a book using its **barcode / ISBN**, fetches metadata from multiple sources, and uses **AI-powered content analysis** to evaluate age suitability and potentially sensitive content.

## Features

- **Barcode / ISBN Scanner**
  - Upload book barcode images
  - Extract ISBN automatically from barcode

- **Multi-source Book Metadata Fetching**
  - Google Books API
  - Open Library API
  - Local database cache

- **AI Content Safety Analysis**
  - Violence detection
  - Profanity analysis
  - Sexual content screening
  - Gender identity theme detection
  - Age recommendation scoring

- **Safety Rating System**
  - Green → Safe
  - Yellow → Caution
  - Red → Sensitive

- **Database Caching**
  - Stores scanned books using SQLAlchemy
  - Reuses previously analyzed ISBNs
  - Reduces API calls and improves speed

-  **FastAPI Backend**
  - RESTful API endpoints
  - JSON responses
  - Production-ready backend structure

## Tech Stack

### Backend
- Python
- FastAPI
- SQLAlchemy
- PostgreSQL

### AI & APIs
- OpenAI API
- Google Books API
- Open Library API

### Image Processing
- Barcode / ISBN extraction
- Image upload support
---
## Project Structure

``bash
SafeReadAI/
│
├── app/
│   ├── main.py
│   ├── database.py
│   │
│   ├── models/
│   │   ├── schema.py
│   │   └── book_model.py
│   │
│   ├── routes/
│   │   └── scan_routes.py
│   │
│   └── services/
│       ├── ai_analyzer.py
│       ├── barcode_reader.py
│       ├── book_fetcher.py
│       ├── openlibrary_fetcher.py
│
├── requirements.txt
├── .env
└── README.md

Workflow

Barcode Image
      ↓
Extract ISBN
      ↓
Check Local Database
      ↓
Google Books API
      ↓
Open Library
      ↓
AI Safety Analysis
      ↓
Store Result in Database
      ↓
Return JSON Response

##Installation

Clone repository
git clone https://github.com/yourusername/saferead-ai.git
cd saferead-ai

##Create virtual environment

python -m venv venv
source venv/bin/activate

##Install dependencies

pip install -r requirements.txt

##Run server

uvicorn app.main:app --reload

🔗 Play Store:
https://play.google.com/store/apps/details?id=com.qandelshield.app


uvicorn app.main:app --reload --port 8002

SELECT * FROM public.book_scans
ORDER BY id ASC
