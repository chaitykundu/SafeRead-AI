from fastapi import APIRouter, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.models.schema import ISBNRequest
from app.services.book_fetcher import get_book_data
from app.services.ai_analyzer import analyze_book
from app.services.barcode_reader import extract_isbn_from_image
from app.models.book_model import BookScan
from app.database import SessionLocal
from app.services.utils import is_valid_isbn, is_api_quota_available
from openai.error import RateLimitError

router = APIRouter()

ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp"}


@router.get("/")
def root():
    return {"message": "SafeRead AI API running"}


@router.post("/scan-book")
def scan_book(request: ISBNRequest):

    # ✅ Clean ISBN FIRST before anything else
    isbn = request.isbn.strip().replace(" ", "").replace("-", "")
    
    # ✅ Validate ISBN structure
    if not is_valid_isbn(isbn):
        raise HTTPException(
            status_code=400,
            detail="Invalid ISBN. The check digit is incorrect."
        )

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
            "age_recommendation": existing_scan.analysis.get("age_recommendation"),
            "overall_score": existing_scan.analysis.get("overall_score"),
            "ai_insights": existing_scan.analysis.get("ai_insights")
        }

    # get_book_data also receives clean ISBN now
    book = get_book_data(isbn)

    if not book:
        db.close()
        return {"error": "Book not found for this ISBN"}
    
    try:
        ai_result = analyze_book(book["summary"])
    except RateLimitError:
        db.close()
        raise HTTPException(
            status_code=429,
            detail="API token quota is filled. Please try again later."
        )

    #ai_result = analyze_book(book["summary"])

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
        "age_recommendation": scan.analysis.get("age_recommendation"),
        "overall_score": scan.analysis.get("overall_score"),
        "ai_insights": scan.analysis.get("ai_insights")
    }


@router.post("/scan-book-image")
async def scan_book_image(file: UploadFile = File(...)):
    """
    Accepts a barcode image upload, extracts the ISBN using GPT-4o vision,
    then runs the full book analysis pipeline — same result as /scan-book.
    """

    # Validate file type
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{file.content_type}'. "
                   f"Please upload a JPEG, PNG, GIF, or WebP image."
        )

    # Step 1: Extract ISBN from barcode image
    isbn = extract_isbn_from_image(file)

    if not isbn:
        raise HTTPException(
            status_code=422,
            detail="Could not detect a valid ISBN barcode in the uploaded image. "
                   "Please ensure the barcode is clearly visible and try again."
        )

    db: Session = SessionLocal()

    # Step 2: Check DB cache (same logic as /scan-book)
    existing_scan = db.query(BookScan).filter(BookScan.isbn == isbn).first()

    if existing_scan:
        db.close()
        return {
            "message": "Result fetched from database (cached)",
            "detected_isbn": isbn,
            "title": existing_scan.title,
            "authors": existing_scan.author,
            "cover_image": existing_scan.cover_image,
            "age_recommendation": existing_scan.analysis.get("age_recommendation"),
            "overall_score": existing_scan.analysis.get("overall_score"),
            "ai_insights": existing_scan.analysis.get("ai_insights")
        }

    # Step 3: Fetch book data
    book = get_book_data(isbn)

    if not book:
        db.close()
        raise HTTPException(
            status_code=404,
            detail=f"ISBN {isbn} was detected in the barcode but no book data was found."
        )

    # Step 4: Run AI analysis (same as manual flow)
    ai_result = analyze_book(book["summary"])

    scan = BookScan(
        isbn=isbn,
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
        "message": "Book scanned from barcode image and result saved to database",
        "detected_isbn": isbn,
        "title": scan.title,
        "authors": scan.author,
        "cover_image": scan.cover_image,
        "age_recommendation": scan.analysis.get("age_recommendation"),
        "overall_score": scan.analysis.get("overall_score"),
        "ai_insights": scan.analysis.get("ai_insights")
    }