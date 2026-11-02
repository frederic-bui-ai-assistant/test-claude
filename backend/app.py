import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template
from supabase import Client, create_client

ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")

app = Flask(__name__, template_folder="templates")
_supabase: Client | None = None


def get_supabase() -> Client:
    """Create the Supabase client lazily so health checks do not need DB access."""
    global _supabase
    if _supabase is None:
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_PUBLISHABLE_KEY")
        if not url or not key:
            raise RuntimeError("La configuration Supabase est incomplète.")
        _supabase = create_client(url, key)
    return _supabase


@app.get("/")
def home():
    return render_template("index.html")


@app.get("/api/health")
def health():
    return jsonify({
        "status": "ok",
        "service": "la-cave-des-canuts-api",
        "supabase_configured": bool(
            os.getenv("SUPABASE_URL") and os.getenv("SUPABASE_PUBLISHABLE_KEY")
        ),
    })


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
        app.logger.error("Configuration Supabase invalide: %s", exc)
        return jsonify({"error": str(exc)}), 503
    except Exception:
        app.logger.exception("Impossible de récupérer le catalogue Supabase")
        return jsonify({"error": "Le catalogue est temporairement indisponible."}), 502


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.getenv("PORT", "5000")), debug=False)
