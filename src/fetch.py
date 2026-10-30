import hashlib
import time
from pathlib import Path
import requests
from config import USER_AGENT, TIMEOUT, DELAY, CACHE_DIR

_session = requests.Session()
_session.headers.update({"User-Agent": USER_AGENT})

class FetchError(Exception):
    def __init__(self, url: str, status: int | None = None, reason: str = ""):
        self.url = url
        self.status = status
        self.reason = reason
        super().__init__(f"{url} → {reason or status}")

def _cache_path(url: str) -> Path:
    digest = hashlib.sha256(url.encode()).hexdigest()[:16]
    return CACHE_DIR / f"{digest}.html"

def fetch(url: str, *, force: bool = False, retries: int = 1, stats: dict | None = None) -> tuple[str, bool]:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    path = _cache_path(url)

    if path.exists() and not force:
        if stats is not None:
            stats["cache_hits"] += 1
        return path.read_text(encoding="utf-8"), True

    last_exc: FetchError | None = None

    for attempt in range(retries + 1):
        try:
            time.sleep(DELAY)
            resp = _session.get(url, timeout=TIMEOUT)

            if resp.status_code == 200:
                html = resp.text
                path.write_text(html, encoding="utf-8")
                if stats is not None:
                    stats["pages_fetched"] += 1
                return html, False

            if resp.status_code in (404, 403):
                raise FetchError(url, resp.status_code, f"HTTP {resp.status_code}")
            if 500 <= resp.status_code < 600:
                last_exc = FetchError(url, resp.status_code, f"HTTP {resp.status_code}")
                time.sleep(1.0 * (attempt + 1))
                continue
            raise FetchError(url, resp.status_code, f"HTTP {resp.status_code}")
        except requests.Timeout:
            last_exc = FetchError(url, None, "timeout")
            time.sleep(1.0 * (attempt + 1))
            continue
        except requests.RequestException as exc:
            raise FetchError(url, None, str(exc)) from exc

    raise last_exc