from datetime import datetime, timezone
from bs4 import BeautifulSoup
from fetch import fetch

RATING_WORDS = {"One", "Two", "Three", "Four", "Five"}

def extract_book(product_url: str, source_page: str, stats: dict | None = None) -> dict:
    html, _ = fetch(product_url, stats=stats)
    soup = BeautifulSoup(html, "html.parser")

    main = soup.select_one("div.product_main")
    if main is None:
        raise ValueError("product_main not found — page shape changed?")

    title_el = main.select_one("h1")
    if title_el is None:
        raise ValueError("title not found")

    price_el = main.select_one("p.price_color")
    availability_el = main.select_one("p.instock.availability")
    rating_el = main.select_one("p.star-rating")

    rating_text = None
    if rating_el:
        rating_text = next((c for c in rating_el.get("class", []) if c in RATING_WORDS), None)

    description = None
    desc_anchor = soup.select_one("div#product_description")
    if desc_anchor:
        p = desc_anchor.find_next_sibling("p")
        if p:
            description = p.get_text(strip=True) or None

    return {
        "title": title_el.get_text(strip=True),
        "product_url": product_url,
        "price_text": price_el.get_text(strip=True) if price_el else None,
        "availability_text": availability_el.get_text(strip=True) if availability_el else None,
        "rating_text": rating_text,
        "description": description,
        "source_page": source_page,
        "fetched_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }