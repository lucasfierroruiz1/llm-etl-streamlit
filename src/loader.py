import json
import pandas as pd
from pathlib import Path
from supabase import create_client
from common import Settings

s = Settings()
key = s.supabase_service or s.supabase_anon
client = create_client(s.supabase_url, key)

items = json.loads(Path("data/structured.json").read_text(encoding="utf-8"))

if isinstance(items, dict):
    items = [items]  # <-- this line must be indented

df = pd.DataFrame(items)

res = client.table(s.table).upsert(df.to_dict(orient="records")).execute()
print(f"Upserted {len(df)} rows")

