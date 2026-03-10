from fastapi import APIRouter
from app.models.schema import ISBNRequest
from app.services.book_fetcher import get_book_data
from app.services.ai_analyzer import analyze_book

router = APIRouter()

@router.post("/scan-book")
def scan_book(req: ISBNRequest):

    book = get_book_data(req.isbn)

    if not book:
        return {"error":"Book not found"}

    ai_result = analyze_book(book["summary"])

    return {
        "title": book["title"],
        "authors": book.get("authors", "Unknown Author"),
        "analysis": ai_result
    }