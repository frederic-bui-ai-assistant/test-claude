import json
import os
from http.server import BaseHTTPRequestHandler


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = {
            "status": "ok",
            "service": "la-cave-des-canuts-api",
            "supabase_configured": bool(
                os.getenv("SUPABASE_URL") and os.getenv("SUPABASE_PUBLISHABLE_KEY")
            ),
        }
        payload = json.dumps(body).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)
