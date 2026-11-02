import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template

from backend.catalog import get_public_wines

ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")

app = Flask(__name__, template_folder="templates")


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
        return jsonify(get_public_wines())
    except RuntimeError as exc:
        app.logger.error("Configuration Supabase invalide: %s", exc)
        return jsonify({"error": str(exc)}), 503
    except Exception:
        app.logger.exception("Impossible de récupérer le catalogue Supabase")
        return jsonify({"error": "Le catalogue est temporairement indisponible."}), 502


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.getenv("PORT", "5000")), debug=False)
