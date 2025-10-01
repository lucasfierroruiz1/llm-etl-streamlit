from pathlib import Path
from bs4 import BeautifulSoup
import requests
import time

DATA = Path("data")
DATA.mkdir(parents=True, exist_ok=True)
RAW = DATA / "raw_blob.txt"

URL = "https://www.espn.com/soccer/team/stats/_/id/83/barcelona"

# Single line headers only
HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-US,en;q=0.9",
}

def fetch_with_retries(url: str, tries: int = 3, delay: float = 1.0) -> str:
    last_exc = None
    for _ in range(tries):
        try:
            r = requests.get(url, headers=HEADERS, timeout=30)
            r.raise_for_status()
            return r.text
        except Exception as e:
            last_exc = e
            time.sleep(delay)
    raise last_exc

html = fetch_with_retries(URL)

soup = BeautifulSoup(html, "html.parser")
for t in soup(["script", "style", "noscript"]):
    t.decompose()

main = soup.find("main") or soup.find("article") or soup
text = "\n".join(x.strip() for x in main.get_text("\n").splitlines() if x.strip())

RAW.write_text(text, encoding="utf-8")
print(f"Saved {RAW}")

