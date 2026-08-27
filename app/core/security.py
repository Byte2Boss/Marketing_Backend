import random
import string


def generate_confirmation_code(prefix: str = "RM") -> str:
    """Generate a clean, readable confirmation code like RM-83921."""
    digits = "".join(random.choices(string.digits, k=5))
    return f"{prefix}-{digits}"


def normalize_email(email: str) -> str:
    """Trim and lowercase email address."""
    return email.strip().lower() if email else ""
