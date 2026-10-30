import argparse
import json
import time
from datetime import datetime, timezone
from config import OUTPUT_DIR
from discover import discover_book_urls
from extract import extract_book
from fetch import FetchError
from models import BookRecord
from normalize import parse_price_gbp

FAKE_URL = "https://books.toscrape.com/catalogue/this-page-does-not-exist_9999/index.html"

def main(include_fake: bool = False) -> dict:
    start = datetime.now(timezone.utc)
    t0 = time.perf_counter()

    OUTPUT_DIR.mkdir(exist_ok=True)

    stats = {"pages_fetched": 0, "cache_hits": 0, "valid_records": 0, "invalid_records": 0, "failed_pages": 0}

    discovered = discover_book_urls(stats=stats)
    book_urls = list(discovered.keys())

    if include_fake:
        discovered[FAKE_URL] = "https://books.toscrape.com/catalogue/page-1.html"
        book_urls.append(FAKE_URL)

    records: list[BookRecord] = []
    errors: list[dict] = []

    for url in book_urls:
        source_page = discovered[url]
        try:
            raw = extract_book(url, source_page=source_page, stats=stats)
            raw["price_gbp"] = parse_price_gbp(raw["price_text"])
            record = BookRecord(**raw)
            records.append(record)
        except FetchError as exc:
            stats["failed_pages"] += 1
            errors.append({"url": url, "type": "fetch", "error": str(exc)})
        except Exception as exc:
            stats["invalid_records"] += 1
            errors.append({"url": url, "type": "validation", "error": str(exc)})

    seen: set[str] = set()
    unique_records: list[BookRecord] = []
    for record in records:
        key = str(record.product_url)
        if key not in seen:
            seen.add(key)
            unique_records.append(record)

    stats["valid_records"] = len(unique_records)

    with (OUTPUT_DIR / "books.json").open("w", encoding="utf-8") as fh:
        json.dump([r.model_dump(mode="json") for r in unique_records], fh, indent=2, ensure_ascii=False)

    with (OUTPUT_DIR / "errors.json").open("w", encoding="utf-8") as fh:
        json.dump(errors, fh, indent=2, ensure_ascii=False)

    duration = round(time.perf_counter() - t0, 2)
    report = {
        "start_time": start.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "duration_seconds": duration,
        "pages_fetched": stats["pages_fetched"],
        "cache_hits": stats["cache_hits"],
        "valid_records": stats["valid_records"],
        "invalid_records": stats["invalid_records"],
        "failed_pages": stats["failed_pages"],
    }

    with (OUTPUT_DIR / "run-report.json").open("w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2)

    print(json.dumps(report, indent=2))
    return report

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Polite Books to Scrape scraper")
    parser.add_argument("--test-failure", action="store_true", help="Add one deliberately broken URL to prove the run survives it.")
    args = parser.parse_args()
    main(include_fake=args.test_failure)