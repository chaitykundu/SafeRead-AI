import os
from dotenv import load_dotenv
import requests

# Load .env file
load_dotenv()

GOOGLE_BOOKS_API_KEY = os.getenv("GOOGLE_BOOKS_API_KEY")

def get_book_data(isbn: str) -> dict:
    """
    Fetch book information by ISBN.
    Tries Google Books first, then Open Library, then local fallback.
    """
    # Clean ISBN
    isbn_clean = isbn.replace("-", "").replace(" ", "")
    
    # --- Step 1: Google Books API ---
    url_google = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn_clean}&key={GOOGLE_BOOKS_API_KEY}"
    try:
        res = requests.get(url_google, timeout=5)
        res.raise_for_status()
        data = res.json()
    except requests.RequestException as e:
        print("Google Books API request failed:", e)
        data = {}

    if data.get("totalItems", 0) > 0:
        book_info = data["items"][0]["volumeInfo"]
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
            "gender_identity": "Unknown",
            "page_count": book_info.get("pageCount", 0)
        }

    # --- Step 2: Open Library API fallback ---
    url_ol = f"https://openlibrary.org/isbn/{isbn_clean}.json"
    try:
        res_ol = requests.get(url_ol, timeout=5)
        if res_ol.status_code == 200:
            ol_data = res_ol.json()
            # Fetch authors' names
            authors = []
            for author in ol_data.get("authors", []):
                try:
                    author_res = requests.get(f"https://openlibrary.org{author['key']}.json", timeout=5)
                    author_res.raise_for_status()
                    author_data = author_res.json()
                    authors.append(author_data.get("name", "Unknown Author"))
                except:
                    authors.append("Unknown Author")
            return {
                "title": ol_data.get("title", "Unknown Title"),
                "authors": ", ".join(authors) if authors else "Unknown Author",
                "summary": "No description available",
                "categories": ol_data.get("subjects", []),
                "published_date": ol_data.get("publish_date", ""),
                "gender_identity": "Unknown",
                "page_count": ol_data.get("number_of_pages", 0)
            }
    except requests.RequestException as e:
        print("Open Library API request failed:", e)

    # --- Step 3: Local fallback ---
    return {
        "title": "Unknown Book",
        "authors": "Unknown Author",
        "summary": "No description available",
        "categories": [],
        "published_date": "",
        "gender_identity": "Unknown",
        "page_count": 0
    }