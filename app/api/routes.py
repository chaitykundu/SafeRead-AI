from fastapi import APIRouter
from sqlalchemy.orm import Session
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

    # ✅ Clean ISBN FIRST before anything else
    isbn = request.isbn.strip().replace(" ", "").replace("-", "")
    
    db: Session = SessionLocal()

    # Now DB check uses clean ISBN
    existing_scan = db.query(BookScan).filter(BookScan.isbn == isbn).first()

    if existing_scan:
        db.close()
        return {
            "message": "Result fetched from database (cached)",
            "title": existing_scan.title,
            "authors": existing_scan.author,
            "cover_image": existing_scan.cover_image,
            "analysis": existing_scan.analysis
        }

    # get_book_data also receives clean ISBN now
    book = get_book_data(isbn)

    if not book:
        db.close()
        return {"error": "Book not found for this ISBN"}

    ai_result = analyze_book(book["summary"])

    scan = BookScan(
        isbn=isbn,  # ✅ saves clean ISBN to DB
        title=book.get("title", "Unknown Title"),
        author=book.get("authors", "Unknown Author"),
        cover_image=book.get("cover_image"),
        summary=book.get("summary"),
        analysis=ai_result
    )

    db.add(scan)
    db.commit()
    db.refresh(scan)
    db.close()

    return {
        "message": "Book scanned and result saved to database",
        "title": scan.title,
        "authors": scan.author,
        "cover_image": scan.cover_image,
        "analysis": scan.analysis
    }