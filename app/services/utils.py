# app/services/utils.py

def is_valid_isbn(isbn: str) -> bool:
    """Check if ISBN is structurally valid (ISBN-10 or ISBN-13)."""
    isbn = isbn.replace("-", "").replace(" ", "")
    if len(isbn) == 10 and isbn[:-1].isdigit():
        total = sum((i + 1) * int(d) for i, d in enumerate(isbn[:-1]))
        check = isbn[-1].upper()
        check_value = 10 if check == "X" else int(check)
        return (total + 10 * check_value) % 11 == 0
    elif len(isbn) == 13 and isbn.isdigit():
        total = sum(int(d) * (1 if i % 2 == 0 else 3) for i, d in enumerate(isbn[:-1]))
        check = int(isbn[-1])
        return (10 - total % 10) % 10 == check
    return False