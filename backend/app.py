import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, jsonify, send_from_directory
from supabase import Client, create_client

ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")

app = Flask(__name__)
_supabase: Client | None = None


def get_supabase() -> Client:
    global _supabase
    if _supabase is None:
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_PUBLISHABLE_KEY")
        if not url or not key:
            raise RuntimeError("SUPABASE_URL et SUPABASE_PUBLISHABLE_KEY doivent être configurées.")
        _supabase = create_client(url, key)
    return _supabase


@app.get("/")
def home():
    return send_from_directory(ROOT_DIR, "index.html")


@app.get("/api/health")
def health():
    return jsonify({"status": "ok", "service": "la-cave-des-canuts-api"})


@app.get("/api/wines")
def list_wines():
    try:
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
        return jsonify(response.data)
    except RuntimeError as exc:
        return jsonify({"error": str(exc)}), 500
    except Exception:
        app.logger.exception("Impossible de récupérer le catalogue Supabase")
        return jsonify({"error": "Le catalogue est temporairement indisponible."}), 502


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.getenv("PORT", "5000")), debug=True)
