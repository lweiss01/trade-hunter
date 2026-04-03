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
            if self.path == "/api/kalshi/markets":
                return self._json_response({"markets": service.get_kalshi_markets()})
            if self.path.split("?")[0] == "/api/kalshi/categories":
                from urllib.parse import urlparse, parse_qs
                qs = parse_qs(urlparse(self.path).query)
                category = (qs.get("q") or qs.get("category") or [""])[0].strip()
                limit = int((qs.get("limit") or ["20"])[0])
                return self._json_response({"results": service.search_kalshi_by_category(category, limit=limit)})
            if self.path == "/api/health":
                # Return feed health status and retention cleanup status
                state = service.dashboard_state()
                cleanup_status = service.get_cleanup_status()
                return self._json_response({
                    "feeds": state.get("feeds", {}),
                    "retention": cleanup_status,
                })
            self._json_response({"error": "not found"}, status=HTTPStatus.NOT_FOUND)

        def do_POST(self) -> None:
            if self.path not in {
                "/api/events",
                "/api/alerts/polyalerthub",
                "/api/demo/spike",
                "/api/kalshi/markets",
                "/api/kalshi/markets/remove",
            }:
                return self._json_response({"error": "not found"}, status=HTTPStatus.NOT_FOUND)

            # Token validation based on endpoint
            if self.path == "/api/alerts/polyalerthub" and settings.polyalerthub_token:
                auth = self.headers.get("Authorization", "")
                expected = f"Bearer {settings.polyalerthub_token}"
                if auth != expected:
                    print(f"PolyAlertHub auth failed: expected Bearer token, got {auth[:20]}...")
                    return self._json_response(
                        {"error": "unauthorized"},
                        status=HTTPStatus.UNAUTHORIZED,
                    )
                print("PolyAlertHub auth validated")
            elif self.path == "/api/events" and settings.ingest_api_token:
                # Generic /api/events endpoint uses INGEST_API_TOKEN
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

            if self.path == "/api/kalshi/markets":
                ticker = str(payload.get("ticker") or "").strip()
                try:
                    markets = service.add_kalshi_market(ticker)
                except ValueError as exc:
                    return self._json_response({"error": str(exc)}, status=HTTPStatus.BAD_REQUEST)
                return self._json_response({"ok": True, "markets": markets})

            if self.path == "/api/kalshi/markets/remove":
                ticker = str(payload.get("ticker") or "").strip()
                try:
                    markets = service.remove_kalshi_market(ticker)
                except ValueError as exc:
                    return self._json_response({"error": str(exc)}, status=HTTPStatus.BAD_REQUEST)
                return self._json_response({"ok": True, "markets": markets})

            source = "polyalerthub" if self.path == "/api/alerts/polyalerthub" else "manual"
            
            # Update feed health status for polyalerthub endpoint
            if self.path == "/api/alerts/polyalerthub":
                from datetime import UTC, datetime
                try:
                    result = service.ingest_payload(payload, default_source=source)
                    service.store.update_feed_status(
                        "polyalerthub",
                        {
                            "running": True,
                            "last_event_at": datetime.now(UTC).isoformat(),
                            "detail": "relay endpoint active",
                            "error_count": 0,
                        }
                    )
                except Exception as exc:
                    service.store.update_feed_status(
                        "polyalerthub",
                        {
                            "running": False,
                            "detail": f"error: {exc}",
                            "error_count": 1,
                        }
                    )
                    return self._json_response(
                        {"error": "internal server error"},
                        status=HTTPStatus.INTERNAL_SERVER_ERROR,
                    )
            else:
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
