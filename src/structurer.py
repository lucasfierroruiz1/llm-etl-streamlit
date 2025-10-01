import json
import uuid
from pathlib import Path
from openai import OpenAI
from common import Settings, utcnow_iso

RAW = Path("data/raw_blob.txt")
OUT = Path("data/structured.json")

s = Settings()
client = OpenAI(base_url=s.base_url, api_key=s.api_key)

PROMPT = (
    "You will receive raw text. Return JSON list of objects with keys "
    "id, title, summary, topics, source_url, extracted_at, updated_at. "
    "id must be UUIDv4. summary is 2 to 4 sentences. "
    "topics is a short list of tags. updated_at is current UTC in ISO8601. "
    "Respond with JSON only."
)

# read the raw blob
blob = RAW.read_text(encoding="utf-8")

messages = [
    {"role": "developer", "content": "Talk like a pirate."},
    {"role": "system", "content": "You are a strict JSON generator. No prose."},
    {"role": "user", "content": f"{PROMPT}\n\nInput:\n{blob[:75000]}"},
]

resp = client.chat.completions.create(
    model=s.deployment,
    messages=messages,
    temperature=0.2,
    response_format={"type": "json_object"}
)

raw = resp.choices[0].message.content

try:
    obj = json.loads(raw)
except json.JSONDecodeError as e:
    raise SystemExit(f"Model did not return valid JSON, {e}")

# normalize result into a list of dicts
if isinstance(obj, dict) and "items" in obj:
    items = obj["items"]
elif isinstance(obj, list):
    items = obj
else:
    items = [obj]

now = utcnow_iso()
norm = []
for x in items:
    norm.append({
        "id": x.get("id") or str(uuid.uuid4()),
        "title": x.get("title") or "Untitled",
        "summary": x.get("summary") or "",
        "topics": x.get("topics") or [],
        "source_url": x.get("source_url") or "unknown",
        "extracted_at": x.get("extracted_at") or now,
        "updated_at": now
    })

OUT.write_text(json.dumps(norm, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"Wrote {OUT}")

