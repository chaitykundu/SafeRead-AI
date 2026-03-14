import os
from dotenv import load_dotenv
import requests
from app.services.openlibrary_fetcher import get_openlibrary_data

# Load .env file
load_dotenv()

GOOGLE_BOOKS_API_KEY = os.getenv("GOOGLE_BOOKS_API_KEY")

def get_book_data(isbn):
    isbn = isbn.replace("-", "")
    url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}&key={GOOGLE_BOOKS_API_KEY}"
    
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        data = res.json()
        print(f"[DEBUG] Google Books response received for ISBN {isbn}")
    except requests.RequestException as e:
        print("Request failed:", e)
        print(f"[DEBUG] Failed to fetch data for ISBN {isbn}")
        return None

    if data.get("totalItems", 0) == 0:
        print(f"[DEBUG] No books found for ISBN {isbn}")
        return None

    book_info = data["items"][0]["volumeInfo"]

    # Handle authors and categories safely
    authors_list = book_info.get("authors") or ["Unknown Author"]
    authors = ", ".join(authors_list)

    categories = book_info.get("categories")
    if not categories or not isinstance(categories, list):
        categories = []

    # ✅ Get cover image
    image_links = book_info.get("imageLinks", {})
    cover_image = image_links.get("thumbnail", "")

    google_data = {
        "title": book_info.get("title", "Unknown Title"),
        "authors": authors,
        "summary": book_info.get("description", "No description available"),
        "categories": categories,
        "published_date": book_info.get("publishedDate", ""),
        "gender_identity": "Unknown",  # Placeholder, as Google Books API does not provide this
        "page_count": book_info.get("pageCount", 0),
        "cover_image": cover_image   # ✅ added
    }
    print(f"[DEBUG] Google Books data extracted for ISBN {isbn}: {google_data}")

    # If Google Books data is incomplete, try Open Library
    if not google_data["summary"] or google_data["summary"] == "No description available":
        openlibrary_data = get_openlibrary_data(isbn)
        if openlibrary_data:
            google_data["summary"] = openlibrary_data.get("summary", google_data["summary"])
            if not google_data["cover_image"]:
                google_data["cover_image"] = openlibrary_data.get("cover_image", "")
    
    print(f"[DEBUG] Final book data for ISBN {isbn}: {google_data}")

    return google_data
