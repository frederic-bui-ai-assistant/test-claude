import os
from pathlib import Path

from dotenv import load_dotenv
from supabase import Client, create_client

ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")

_supabase: Client | None = None


def get_supabase() -> Client:
    global _supabase
    if _supabase is None:
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_PUBLISHABLE_KEY")
        if not url or not key:
            raise RuntimeError("La configuration Supabase est incomplète.")
        _supabase = create_client(url, key)
    return _supabase


def get_public_wines() -> list[dict]:
    response = (
        get_supabase()
        .table("wines")
        .select(
            "id,name,slug,description,vintage,wine_type,appellation,region,country,"
            "grapes,volume_ml,alcohol_percentage,price_cents,compare_at_price_cents,"
            "image_url,tasting_notes,food_pairings,is_featured,producers(name),categories(name)"
        )
        .eq("is_published", True)
        .order("name")
        .execute()
    )
    return response.data
