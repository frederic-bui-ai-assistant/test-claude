import json
from http.server import BaseHTTPRequestHandler

from backend.catalog import get_public_wines


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            payload = json.dumps(get_public_wines(), ensure_ascii=False).encode("utf-8")
            status = 200
        except RuntimeError as exc:
            payload = json.dumps({"error": str(exc)}, ensure_ascii=False).encode("utf-8")
            status = 503
        except Exception:
            payload = json.dumps(
                {"error": "Le catalogue est temporairement indisponible."},
                ensure_ascii=False,
            ).encode("utf-8")
            status = 502

        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)
