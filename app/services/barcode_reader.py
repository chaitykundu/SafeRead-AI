import openai
import base64
import re
from fastapi import UploadFile


def extract_isbn_from_image(image_file: UploadFile) -> str | None:
    """
    Takes an uploaded barcode image and uses OpenAI vision (GPT-4o)
    to extract the ISBN number from it.
    Returns clean ISBN string or None if not found.
    """

    # Read and encode image to base64
    image_bytes = image_file.file.read()
    image_b64 = base64.standard_b64encode(image_bytes).decode("utf-8")

    # Detect media type
    content_type = image_file.content_type or "image/jpeg"
    if image_file.filename:
        ext = image_file.filename.lower().rsplit(".", 1)[-1]
        ext_map = {
            "jpg": "image/jpeg",
            "jpeg": "image/jpeg",
            "png": "image/png",
            "gif": "image/gif",
            "webp": "image/webp",
        }
        content_type = ext_map.get(ext, content_type)

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        max_tokens=100,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{content_type};base64,{image_b64}"
                        },
                    },
                    {
                        "type": "text",
                        "text": (
                            "This image contains a book barcode. "
                            "Please extract the ISBN number from the barcode. "
                            "Return ONLY the raw digits of the ISBN (10 or 13 digits), "
                            "with no dashes, spaces, labels, or extra text. "
                            "If you cannot find an ISBN, reply with exactly: NOT_FOUND"
                        ),
                    },
                ],
            }
        ],
    )

    raw = response["choices"][0]["message"]["content"].strip()

    if raw == "NOT_FOUND" or not raw:
        return None

    # Keep only digits and clean up
    isbn = re.sub(r"[^0-9X]", "", raw.upper())

    # Validate length (ISBN-10 or ISBN-13)
    if len(isbn) in (10, 13):
        return isbn

    # If Claude returned extra text, try to pull out a 10/13-digit sequence
    match = re.search(r"\b(\d{13}|\d{10})\b", raw)
    if match:
        return match.group(1)

    return None