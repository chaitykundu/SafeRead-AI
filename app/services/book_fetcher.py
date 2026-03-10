import os
from dotenv import load_dotenv
import requests

# Load .env file
load_dotenv()

GOOGLE_BOOKS_API_KEY = os.getenv("GOOGLE_BOOKS_API_KEY")

def get_book_data(isbn):
    isbn = isbn.replace("-", "")
    url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}&key={GOOGLE_BOOKS_API_KEY}"
    
    try:
        res = requests.get(url, timeout=5)
        res.raise_for_status()
        data = res.json()
    except requests.RequestException as e:
        print("Request failed:", e)
        return None

    if data.get("totalItems", 0) == 0:
        return None

    book_info = data["items"][0]["volumeInfo"]

    # Handle authors and categories safely
    authors_list = book_info.get("authors") or ["Unknown Author"]
    authors = ", ".join(authors_list)

    categories = book_info.get("categories")
    if not categories or not isinstance(categories, list):
        categories = []

    return {
        "title": book_info.get("title", "Unknown Title"),
        "authors": authors,
        "summary": book_info.get("description", "No description available"),
        "categories": categories,
        "published_date": book_info.get("publishedDate", ""),
        "gender_identity": "Unknown",  # Placeholder, as Google Books API does not provide this
        "page_count": book_info.get("pageCount", 0)
    }