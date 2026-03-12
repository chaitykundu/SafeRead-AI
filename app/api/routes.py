from fastapi import APIRouter
from app.models.schema import ISBNRequest
from app.services.book_fetcher import get_book_data
from app.services.ai_analyzer import analyze_book
from app.models.book_model import BookScan
from app.database import SessionLocal

router = APIRouter()

@router.get("/")
def root():
    return {"message": "SafeRead AI API running"}

@router.post("/scan-book")
def scan_book(request: ISBNRequest):

    isbn = request.isbn

    book = get_book_data(isbn)

    # NEW CHECK
    if not book:
        return {"error": "Book not found for this ISBN"}

    ai_result = analyze_book(book["summary"])

    db = SessionLocal()

    scan = BookScan(
        isbn=isbn,
        title=book.get("title", "Unknown Title"),
        author=book.get("authors", "Unknown Author"),
        violence=ai_result.get("violence", {}).get("level", "Unknown"),
        profanity=ai_result.get("profanity", {}).get("level", "Unknown"),
        sexual_content=ai_result.get("sexual_content", {}).get("level", "Unknown"),
        summary=book.get("summary", "")
    )

    db.add(scan)
    db.commit()
    db.refresh(scan)
    db.close()

    return {
        "title": book["title"],
        "authors": book.get("authors", "Unknown Author"),
        "cover_image": book.get("cover_image"),
        "analysis": ai_result
    }