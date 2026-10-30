import re

def parse_price_gbp(price_text: str | None) -> float:
    if not price_text:
        raise ValueError("empty price_text")
    cleaned = re.sub(r"[^\d.]", "", price_text)
    if not cleaned:
        raise ValueError(f"no digits found in price_text: {price_text!r}")
    return float(cleaned)