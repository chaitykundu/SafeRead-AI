# app/services/utils.py
def is_valid_isbn(isbn: str) -> bool:
    """Validate ISBN-10 or ISBN-13 properly with checksum."""
    
    isbn = isbn.replace("-", "").replace(" ", "")

    # ISBN-10 validation
    if len(isbn) == 10:
        if not isbn[:-1].isdigit():
            return False

        total = 0
        for i in range(9):
            total += int(isbn[i]) * (10 - i)

        check = isbn[-1].upper()
        check_value = 10 if check == "X" else int(check)

        total += check_value

        return total % 11 == 0

    # ISBN-13 validation
    elif len(isbn) == 13 and isbn.isdigit():
        total = 0
        for i in range(12):
            multiplier = 1 if i % 2 == 0 else 3
            total += int(isbn[i]) * multiplier

        check = int(isbn[-1])
        calculated_check = (10 - (total % 10)) % 10

        return check == calculated_check

    return False

def is_api_quota_available() -> bool:
    """
    Check if your AI API token has remaining quota.
    Replace this logic with your real quota tracking or API call.
    """
    # Placeholder example: always returns True for now
    # Later you can implement:
    # - track API usage in database
    # - call AI provider API to check remaining credits
    remaining_quota = 10  # example static number
    return remaining_quota > 0