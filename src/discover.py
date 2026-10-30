from urllib.parse import urljoin
from bs4 import BeautifulSoup
from config import BASE_URL, MAX_CATALOGUE_PAGES
from fetch import fetch

def discover_book_urls(stats: dict | None = None) -> dict[str, str]:
    discovered: dict[str, str] = {}
    next_url = BASE_URL + "catalogue/page-1.html"

    for _ in range(MAX_CATALOGUE_PAGES):
        html, _ = fetch(next_url, stats=stats)
        soup = BeautifulSoup(html, "html.parser")

        for article in soup.select("article.product_pod"):
            a = article.select_one("h3 a")
            if not a:
                continue
            absolute = urljoin(next_url, a["href"])
            if absolute not in discovered:
                discovered[absolute] = next_url

        next_link = soup.select_one("li.next a")
        if not next_link:
            break
        next_url = urljoin(next_url, next_link["href"])

    return discovered