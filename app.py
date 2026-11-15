"""Local-only HTTP interface; Python 3.10+, no dependencies."""
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from core import analyse, DEMO

class Handler(BaseHTTPRequestHandler):
    def send(self, code, body, kind="application/json"):
        self.send_response(code)
        self.send_header("Content-Type", kind + "; charset=utf-8")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/":
            self.send(200, Path(__file__).with_name("index.html").read_bytes(), "text/html")
        elif self.path == "/api/demo":
            self.send(200, json.dumps(DEMO).encode())
        else:
            self.send(404, b'{"error":"Not found"}')

    def do_POST(self):
        if self.path != "/api/analyse":
            self.send(404, b'{"error":"Not found"}')
            return
        # Prevent other sites from driving this local service from a browser.
        if self.headers.get("Origin") not in (None, "http://127.0.0.1:8000", "http://localhost:8000"):
            self.send(403, b'{"error":"Origin not allowed"}')
            return
        try:
            size=int(self.headers.get("Content-Length", "0"))
            if not 0 < size <= 1000000:
                raise ValueError("Request must be between 1 byte and 1 MB.")
            data=json.loads(self.rfile.read(size))
            if not isinstance(data, dict):
                raise ValueError("Input must be a JSON object.")
            result=analyse(data)
            self.send(200, json.dumps(result, allow_nan=False).encode())
        except (ValueError, KeyError, TypeError, OverflowError) as error:
            self.send(400, json.dumps({"error":str(error)}).encode())

if __name__ == "__main__":
    print("Open http://127.0.0.1:8000 — Ctrl+C to stop")
    ThreadingHTTPServer(("127.0.0.1", 8000), Handler).serve_forever()
