from pathlib import Path

BASE_URL = "https://books.toscrape.com/"
USER_AGENT = "FlyRankInternship-A9/1.0 (+https://github.com/yourusername/polite-scraper)"
TIMEOUT = 10
DELAY = 0.5
MAX_CATALOGUE_PAGES = 3

BASE_DIR = Path(__file__).resolve().parent.parent
CACHE_DIR = BASE_DIR / "cache"
OUTPUT_DIR = BASE_DIR / "output"