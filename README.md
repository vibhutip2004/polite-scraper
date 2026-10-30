# Polite Scraper — Books to Scrape

A small, polite scraping pipeline that collects the first three catalogue pages of Books to Scrape, visits all 60 book pages, normalises the data, validates every record against a schema, and writes clean JSON plus an honest run report.

## Target classification

- **Site:** Books to Scrape — `https://books.toscrape.com/`
- **Why:** It is a public practice sandbox built specifically for learning scraping. The site itself describes the catalogue as fictional and intended for scraping practice.
- **Scope:** Exactly the first **3 catalogue pages** (60 unique books). Nothing else on the site is touched.
- **Data collected:** title, product URL, raw price text, numeric price in GBP, availability text, rating text, description (optional), source catalogue page, and fetch timestamp.
- **robots.txt:** `https://books.toscrape.com/robots.txt` returns **no robots file found**. A missing file is not permission; it simply means there is no robots exclusion file. The sandbox's own purpose makes scraping appropriate here.
- **Ethics:** I will not reuse this code on another site without checking its rules and terms first.

## Lane and installation

**Lane:** Python 3.10+ (Requests + Beautiful Soup + Pydantic).

```bash
git clone https://github.com/vibhutip2004/polite-scraper.git
cd polite-scraper
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

#