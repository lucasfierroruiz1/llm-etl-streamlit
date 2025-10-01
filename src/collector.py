from pathlib import Path
from bs4 import BeautifulSoup
import requests

DATA = Path("data")
DATA.mkdir(parents=True, exist_ok=True)
RAW = DATA / "raw_blob.txt"

URL = "https://www.charlottefootballclub.com/news"

r = requests.get(URL, timeout=30)
r.raise_for_status()

soup = BeautifulSoup(r.text, "html.parser")
for t in soup(["script", "style", "noscript"]):
    t.decompose()

main = soup.find("main") or soup.find("article") or soup
text = "\n".join(x.strip() for x in main.get_text("\n").splitlines() if x.strip())

RAW.write_text(text, encoding="utf-8")
print(f"Saved {RAW}")

