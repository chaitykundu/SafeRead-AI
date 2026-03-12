import requests

def get_openlibrary_data(isbn):

    url = f"https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data"

    try:
        res = requests.get(url, timeout=5)
        res.raise_for_status()
        data = res.json()
        print(f"[DEBUG] Open Library response received for ISBN {isbn}")
    except requests.RequestException:
        print(f"[DEBUG] Failed to fetch data for ISBN {isbn}")
        return None

    key = f"ISBN:{isbn}"

    if key not in data:
        print(f"[DEBUG] No data found for ISBN {isbn}")
        return None

    book = data[key]

    authors = ", ".join([a["name"] for a in book.get("authors", [])]) or "Unknown Author"

    cover = book.get("cover", {}).get("medium", "")

    print(f"[DEBUG] Open Library data extracted for ISBN {isbn}: {book}")
    return {
        "title": book.get("title", "Unknown Title"),
        "authors": authors,
        "summary": book.get("notes", "No description available"),
        "categories": [],
        "published_date": book.get("publish_date", ""),
        "page_count": book.get("number_of_pages", 0),
        "cover_image": cover
    }