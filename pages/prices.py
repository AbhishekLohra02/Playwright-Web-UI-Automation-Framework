from decimal import Decimal


def parse_price(price_text: str) -> Decimal:
    """Convert a displayed price such as ``Total: $32.39`` into a Decimal."""
    amount = price_text.rsplit("$", 1)[-1].strip()
    return Decimal(amount)
