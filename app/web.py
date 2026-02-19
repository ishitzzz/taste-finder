from __future__ import annotations

import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from app.service import build_recommendation_payload

ROOT = Path(__file__).resolve().parents[1]
WEB_DIR = ROOT / "web"


class TasteWebHandler(BaseHTTPRequestHandler):
    def _request_path(self) -> str:
        return urlparse(self.path).path

    def _send_json(
        self,
        payload: dict,
        status: int = HTTPStatus.OK,
        include_body: bool = True,
    ) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if include_body:
            self.wfile.write(body)

    def _send_file(self, filename: str, content_type: str, include_body: bool = True) -> None:
        path = WEB_DIR / filename
        if not path.exists():
            self.send_error(HTTPStatus.NOT_FOUND)
            return

        content = path.read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        if include_body:
            self.wfile.write(content)

    def _handle_static_or_index(self, include_body: bool = True) -> None:
        path = self._request_path()
        if path in {"/", "/index.html"}:
            self._send_file("index.html", "text/html; charset=utf-8", include_body=include_body)
            return
        if path == "/styles.css":
            self._send_file("styles.css", "text/css; charset=utf-8", include_body=include_body)
            return
        if path == "/app.js":
            self._send_file("app.js", "application/javascript; charset=utf-8", include_body=include_body)
            return
        if path == "/api/health":
            self._send_json({"status": "ok"}, include_body=include_body)
            return

        if path.startswith("/api/"):
            self._send_json({"error": "Not Found"}, status=HTTPStatus.NOT_FOUND, include_body=include_body)
            return

        # SPA-style fallback so preview routes like /preview or /foo render app shell.
        self._send_file("index.html", "text/html; charset=utf-8", include_body=include_body)

    def do_GET(self) -> None:  # noqa: N802
        self._handle_static_or_index(include_body=True)

    def do_HEAD(self) -> None:  # noqa: N802
        self._handle_static_or_index(include_body=False)

    def do_POST(self) -> None:  # noqa: N802
        if self._request_path() != "/api/recommend":
            self._send_json({"error": "Not Found"}, status=HTTPStatus.NOT_FOUND)
            return

        content_length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(content_length)

        try:
            payload = json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError:
            self._send_json({"error": "Invalid JSON body."}, status=HTTPStatus.BAD_REQUEST)
            return

        signals = payload.get("signals", [])
        if not isinstance(signals, list):
            self._send_json(
                {"error": "`signals` must be a list of {domain, text} objects."},
                status=HTTPStatus.BAD_REQUEST,
            )
            return

        result = build_recommendation_payload(signals)
        self._send_json(result)


def run_server(host: str = "0.0.0.0", port: int = 8000) -> None:
    httpd = ThreadingHTTPServer((host, port), TasteWebHandler)
    print(f"Taste Finder web app running at http://{host}:{port}")
    httpd.serve_forever()


if __name__ == "__main__":
    run_server()
