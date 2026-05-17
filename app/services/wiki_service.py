import requests


def get_wikipedia_data(query):
    headers = {
        "User-Agent": "SafeReadAI/1.0 (contact: chaity@example.com)"
    }

    try:
        search_url = "https://en.wikipedia.org/w/api.php"

        params = {
            "action": "query",
            "list": "search",
            "srsearch": query,
            "format": "json"
        }

        res = requests.get(
            search_url,
            params=params,
            headers=headers,
            timeout=5
        )
        res.raise_for_status()

        data = res.json()

        results = data.get("query", {}).get("search", [])

        if not results:
            print(f"[DEBUG] No Wikipedia results found for {query}")
            return None

        title = results[0]["title"].replace(" ", "_")

        summary_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{title}"

        summary_res = requests.get(
            summary_url,
            headers=headers,
            timeout=5
        )
        summary_res.raise_for_status()

        summary_data = summary_res.json()

        return {
            "title": summary_data.get("title", "Unknown Title"),
            "authors": "Unknown Author",
            "summary": summary_data.get("extract", "No description available"),
            "categories": [],
            "published_date": "",
            "gender_identity": "Unknown",
            "page_count": 0,
            "cover_image": summary_data.get("thumbnail", {}).get("source", "")
        }

    except requests.RequestException as e:
        print(f"[DEBUG] Wikipedia fetch failed: {e}")
        return None