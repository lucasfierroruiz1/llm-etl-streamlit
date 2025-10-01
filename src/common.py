from dataclasses import dataclass
from datetime import datetime, timezone
from dotenv import load_dotenv
import os

# load environment variables from .env
load_dotenv()

@dataclass
class Settings:
    base_url: str = os.getenv("OPENAI_BASE_URL", "")
    api_key: str = os.getenv("OPENAI_API_KEY", "")
    deployment: str = os.getenv("OPENAI_DEPLOYMENT", "gpt-4o")
    supabase_url: str = os.getenv("SUPABASE_URL", "")
    supabase_anon: str = os.getenv("SUPABASE_ANON_KEY", "")
    supabase_service: str = os.getenv("SUPABASE_SERVICE_ROLE", "")
    table: str = os.getenv("SUPABASE_TABLE", "etl_items")

def utcnow_iso():
    return datetime.now(timezone.utc).isoformat()

