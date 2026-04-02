from __future__ import annotations

import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

from .config import ROOT, Settings
from .service import TradeHunterService


STATIC_ROOT = ROOT / "app" / "static"


def run_server(settings: Settings) -> None:
    service = TradeHunterService(settings)
    service.start()

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:
            if self.path == "/":
                return self._serve_file("index.html", "text/html; charset=utf-8")
            if self.path == "/static/dashboard.css":
                return self._serve_file("dashboard.css", "text/css; charset=utf-8")
            if self.path == "/static/dashboard.js":
                return self._serve_file("dashboard.js", "application/javascript; charset=utf-8")
            if self.path == "/api/state":
                return self._json_response(service.dashboard_state())
            self._json_response({"error": "not found"}, status=HTTPStatus.NOT_FOUND)

        def do_POST(self) -> None:
            if self.path not in {"/api/events", "/api/alerts/polyalerthub", "/api/demo/spike"}:
                return self._json_response({"error": "not found"}, status=HTTPStatus.NOT_FOUND)

            if settings.ingest_api_token:
                auth = self.headers.get("Authorization", "")
                expected = f"Bearer {settings.ingest_api_token}"
                if auth != expected:
                    return self._json_response(
                        {"error": "unauthorized"},
                        status=HTTPStatus.UNAUTHORIZED,
                    )

            if self.path == "/api/demo/spike":
                payload: Any = {
                    "source": "demo-button",
                    "platform": "kalshi",
                    "market_id": "manual-demo",
                    "title": "Manual demo spike",
                    "event_kind": "trade",
                    "yes_price": 0.64,
                    "volume": 450,
                    "volume_kind": "delta",
                    "trade_size": 450,
                    "trade_side": "buy",
                    "live": False,
                    "topic": "crypto",
                }
            else:
                raw = self.rfile.read(int(self.headers.get("Content-Length", "0") or "0"))
                payload = json.loads(raw.decode("utf-8") or "{}")

            source = "polyalerthub" if self.path == "/api/alerts/polyalerthub" else "manual"
            result = service.ingest_payload(payload, default_source=source)
            self._json_response({"ok": True, "signals_triggered": sum(bool(item) for item in result)})

        def log_message(self, format: str, *args: Any) -> None:
            return

        def _serve_file(self, filename: str, content_type: str) -> None:
            body = (STATIC_ROOT / filename).read_bytes()
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _json_response(self, payload: dict[str, Any], status: HTTPStatus = HTTPStatus.OK) -> None:
            body = json.dumps(payload).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

    server = ThreadingHTTPServer((settings.host, settings.port), Handler)
    print(f"Trade Hunter running at http://{settings.host}:{settings.port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        service.stop()
