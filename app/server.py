from __future__ import annotations

import json
import os
import threading
import time
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

from .config import ROOT, TUNING_BACKLOG_PATH, Settings, load_settings, persist_runtime_settings
from .service import TradeHunterService


STATIC_ROOT = ROOT / "app" / "static"


def _is_loopback_client(host: str) -> bool:
    return host in {"127.0.0.1", "::1", "localhost"}


def serialize_settings(settings: Settings) -> dict[str, Any]:
    return {
        "host": settings.host,
        "port": settings.port,
        "enable_simulation": settings.enable_simulation,
        "enable_kalshi": settings.enable_kalshi,
        "quiet_mode": settings.quiet_mode,
        "retention_days": settings.retention_days,
        "is_commercial": settings.is_commercial,
        "discord_alert_mode": settings.discord_alert_mode,
        "discord_analyst_followup": settings.discord_analyst_followup,
        "discord_analyst_min_confidence": settings.discord_analyst_min_confidence,
        "spike_min_volume_delta": settings.spike_min_volume_delta,
        "spike_min_price_move": settings.spike_min_price_move,
        "spike_score_threshold": settings.spike_score_threshold,
        "spike_baseline_points": settings.spike_baseline_points,
        "spike_cooldown_seconds": settings.spike_cooldown_seconds,
        "kalshi_markets": settings.kalshi_markets,
        "presence": {
            "discord_webhook_url": bool(settings.discord_webhook_url),
            "discord_webhook_routes": sorted(settings.discord_webhook_routes.keys()),
            "ingest_api_token": bool(settings.ingest_api_token),
            "polyalerthub_token": bool(settings.polyalerthub_token),
            "kalshi_api_key_id": bool(settings.kalshi_api_key_id),
            "kalshi_private_key_path": bool(settings.kalshi_private_key_path),
        },
    }


def run_server(settings: Settings) -> None:
    service = TradeHunterService(settings)
    service.start()

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:
            from urllib.parse import urlparse, parse_qs

            raw_path = urlparse(self.path).path or self.path
            path = raw_path.rstrip("/") or "/"
            if path == "/":
                return self._serve_file("index.html", "text/html; charset=utf-8")
            if path.endswith("favicon.ico"):
                return self._serve_file("favicon.ico", "image/x-icon")
            if path.endswith("apple-touch-icon.png"):
                return self._serve_file("apple-touch-icon.png", "image/png")
            if path.endswith("/static/dashboard.css"):
                return self._serve_file("dashboard.css", "text/css; charset=utf-8")
            if path.endswith("/static/dashboard.js"):
                return self._serve_file("dashboard.js", "application/javascript; charset=utf-8")
            if path.endswith("/static/favicon.svg"):
                return self._serve_file("favicon.svg", "image/svg+xml; charset=utf-8")
            if path.endswith("/static/favicon-32x32.png"):
                return self._serve_file("favicon-32x32.png", "image/png")
            if path.endswith("/static/trade-hunter-logo4.png"):
                return self._serve_file("trade-hunter-logo4.png", "image/png")
            if path == "/api/state":
                is_admin = self._require_admin_token(silent=True)
                return self._json_response(service.dashboard_state(is_admin=is_admin))
            if path == "/api/settings":
                latest_settings = load_settings()
                is_admin = self._require_admin_token(silent=True)
                return self._json_response({
                    "settings": serialize_settings(latest_settings),
                    "is_admin": is_admin
                })
            if path == "/api/kalshi/markets":
                return self._json_response({"markets": service.get_kalshi_markets()})
            if path == "/api/kalshi/categories":
                qs = parse_qs(urlparse(self.path).query)
                category = (qs.get("q") or qs.get("category") or [""])[0].strip()
                limit = int((qs.get("limit") or ["20"])[0])
                return self._json_response({"results": service.search_kalshi_by_category(category, limit=limit)})
            if path in {"/api/health", "/api/status"}:
                # Return feed health status and retention cleanup status
                state = service.dashboard_state()
                cleanup_status = service.get_cleanup_status()
                return self._json_response({
                    "app": "trade-hunter",
                    "feeds": state.get("feeds", {}),
                    "retention": cleanup_status,
                })
            if path == "/api/tuning/backlog":
                return self._json_response(service.get_tuning_backlog())
            if path == "/docs/TUNING-BACKLOG.md":
                md_path = TUNING_BACKLOG_PATH
                body = md_path.read_bytes() if md_path.exists() else b"# Not found"
                self.send_response(HTTPStatus.OK)
                self.send_header("Content-Type", "text/plain; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
                return
            self._json_response({"error": "not found"}, status=HTTPStatus.NOT_FOUND)

        def do_POST(self) -> None:
            if self.path not in {
                "/api/events",
                "/api/alerts/polyalerthub",
                "/api/demo/spike",
                "/api/kalshi/markets",
                "/api/kalshi/markets/remove",
                "/api/config/apply-tuning",
                "/api/tuning/mark-applied",
                "/api/settings",
                "/api/admin/shutdown",
            } and not self.path.startswith("/api/tuning/") and not self.path.startswith("/api/heartbeat"):
                return self._json_response({"error": "not found"}, status=HTTPStatus.NOT_FOUND)

            if self.path.startswith("/api/heartbeat"):
                if not _is_loopback_client(self.client_address[0]):
                    return self._json_response({"error": "forbidden"}, status=HTTPStatus.FORBIDDEN)

                # Browser refresh/navigation also emits page lifecycle events. Treat
                # legacy close beacons as heartbeats so refresh cannot kill the app.
                self.server.last_heartbeat = time.time()
                return self._json_response({"ok": True, "pulse": "steady"})

            if self.path == "/api/admin/shutdown":
                if not _is_loopback_client(self.client_address[0]):
                    return self._json_response({"error": "forbidden"}, status=HTTPStatus.FORBIDDEN)
                
                # Check for restart mode
                restart = False
                try:
                    content_length = int(self.headers.get("Content-Length", 0))
                    if content_length > 0:
                        body = json.loads(self.rfile.read(content_length).decode("utf-8"))
                        if body.get("mode") == "restart":
                            restart = True
                except Exception:
                    pass

                self._json_response({"ok": True, "status": "restarting" if restart else "shutting-down"})
                if restart:
                    self.server.restart_requested = True
                threading.Thread(target=self.server.shutdown, daemon=True).start()
                return

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
                content_length = int(self.headers.get("Content-Length", 0))
                if content_length > 1_000_000: # 1MB limit
                     return self._json_response({"error": "payload too large"}, status=HTTPStatus.REQUEST_ENTITY_TOO_LARGE)
                
                body = self.rfile.read(content_length)
                try:
                    payload = json.loads(body) if body else {}
                except json.JSONDecodeError:
                    return self._json_response({"error": "invalid json"}, status=HTTPStatus.BAD_REQUEST)

            if self.path == "/api/settings":
                if not self._require_same_origin():
                    return
                if not self._require_admin_token():
                    return

                editable = payload.get("settings") if isinstance(payload, dict) and isinstance(payload.get("settings"), dict) else payload
                try:
                    updated = persist_runtime_settings(editable)
                    latest_settings = load_settings()
                except ValueError as exc:
                    return self._json_response({"error": str(exc)}, status=HTTPStatus.BAD_REQUEST)
                return self._json_response({
                    "ok": True,
                    "updated": sorted(updated.keys()),
                    "restart_required": True,
                    "settings": serialize_settings(latest_settings),
                })

            if self.path == "/api/kalshi/markets":
                if not self._require_same_origin():
                    return
                if not self._require_admin_token():
                    return
                ticker = str(payload.get("ticker") or "").strip()
                try:
                    markets = service.add_kalshi_market(ticker)
                except ValueError as exc:
                    return self._json_response({"error": str(exc)}, status=HTTPStatus.BAD_REQUEST)
                return self._json_response({"ok": True, "markets": markets})

            if self.path == "/api/kalshi/markets/remove":
                if not self._require_same_origin():
                    return
                if not self._require_admin_token():
                    return
                ticker = str(payload.get("ticker") or "").strip()
                try:
                    markets = service.remove_kalshi_market(ticker)
                except ValueError as exc:
                    return self._json_response({"error": str(exc)}, status=HTTPStatus.BAD_REQUEST)
                return self._json_response({"ok": True, "markets": markets})

            if self.path == "/api/tuning/mark-applied":
                if not self._require_same_origin():
                    return
                if not self._require_admin_token():
                    return
                tb_id = str(payload.get("id") or "").strip()
                if not tb_id:
                    return self._json_response({"error": "id required"}, status=HTTPStatus.BAD_REQUEST)
                try:
                    service.mark_tuning_item_applied(tb_id)
                except ValueError as exc:
                    return self._json_response({"error": str(exc)}, status=HTTPStatus.BAD_REQUEST)
                return self._json_response({"ok": True, "id": tb_id})

            if self.path == "/api/config/apply-tuning":
                if not self._require_same_origin():
                    return
                if not self._require_admin_token():
                    return
                try:
                    applied = service.apply_tuning_suggestions()
                except ValueError as exc:
                    return self._json_response({"error": str(exc)}, status=HTTPStatus.BAD_REQUEST)
                return self._json_response({
                    "ok": True,
                    "applied": applied,
                    "applied_thresholds": service.dashboard_state().get("config", {}).get("applied_thresholds", {}),
                })

            source = "polyalerthub" if self.path == "/api/alerts/polyalerthub" else "manual"
            
            # Update feed health status for polyalerthub endpoint
            if self.path == "/api/alerts/polyalerthub":
                if not self._require_ingest_token():
                    return
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
            file_path = STATIC_ROOT / filename
            if not file_path.exists():
                return
            try:
                self.send_response(HTTPStatus.OK)
                self.send_header("Content-Type", content_type)
                self.send_header("Content-Length", str(file_path.stat().st_size))
                self.end_headers()
                with open(file_path, "rb") as f:
                    while chunk := f.read(65536):
                        self.wfile.write(chunk)
            except (ConnectionError, BrokenPipeError):
                pass

        def _json_response(self, payload: dict[str, Any], status: HTTPStatus = HTTPStatus.OK) -> None:
            body = json.dumps(payload).encode("utf-8")
            try:
                self.send_response(status)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.send_header("X-Content-Type-Options", "nosniff")
                self.send_header("X-Frame-Options", "DENY")
                self.end_headers()
                self.wfile.write(body)
            except (ConnectionError, BrokenPipeError):
                pass

        def _require_admin_token(self, silent: bool = False) -> bool:
            """Check for admin token in Authorization header, or allow loopback clients (M016-UX)."""
            if _is_loopback_client(self.client_address[0]):
                return True
            
            if not settings.admin_token:
                return True
            
            auth_header = self.headers.get("Authorization", "")
            if auth_header.startswith("Bearer "):
                token = auth_header[7:].strip()
                if token == settings.admin_token:
                    return True
            if not silent:
                self._json_response({"error": "unauthorized"}, status=HTTPStatus.UNAUTHORIZED)
            return False

        def _require_ingest_token(self) -> bool:
            """Check for ingest token in Authorization header (M015)."""
            if not settings.ingest_api_token:
                return True
            auth_header = self.headers.get("Authorization", "")
            if auth_header.startswith("Bearer "):
                token = auth_header[7:].strip()
                if token == settings.ingest_api_token:
                    return True
            self._json_response({"error": "unauthorized ingest"}, status=HTTPStatus.UNAUTHORIZED)
            return False

        def _require_same_origin(self) -> bool:
            """CSRF protection: verify Origin matches Host (lenient for localhost)."""
            origin = self.headers.get("Origin")
            if not origin:
                referer = self.headers.get("Referer")
                if not referer:
                    self._json_response({"error": "missing origin/referer"}, status=HTTPStatus.BAD_REQUEST)
                    return False
                origin = referer
            
            host = self.headers.get("Host")
            if not host:
                self._json_response({"error": "missing host header"}, status=HTTPStatus.BAD_REQUEST)
                return False

            # M017-UX: Lenient check for local development/bundles
            # If both are localhost-like, allow it
            is_host_local = any(h in host for h in {"127.0.0.1", "localhost", "::1"})
            is_origin_local = any(o in origin for o in {"127.0.0.1", "localhost", "::1"})
            
            if is_host_local and is_origin_local:
                return True

            if host not in origin:
                self._json_response({"error": "csrf origin mismatch"}, status=HTTPStatus.FORBIDDEN)
                return False
            return True

    server = ThreadingHTTPServer((settings.host, settings.port), Handler)
    server.last_heartbeat = time.time()
    server.start_time = time.time()
    server.restart_requested = False

    def heartbeat_monitor():
        """Background thread to monitor for 'No Pulse' (browser closed)."""
        time.sleep(10) # Initial soak time
        while not getattr(server, "_is_shutting_down", False):
            # Grace period: allow 60s at startup before enforcing shutdown
            uptime = time.time() - server.start_time
            timeout = 15.0 if uptime > 60 else 60.0
            
            idle_time = time.time() - server.last_heartbeat
            if idle_time > timeout:
                if not settings.quiet_mode:
                    print(f"--- No heartbeat detected for {idle_time:.1f}s. Entering Smart Shutdown. ---")
                server.shutdown()
                break
            time.sleep(5)

    if os.getenv("TRADE_HUNTER_ENABLE_SMART_SHUTDOWN", "").strip().lower() in {"1", "true", "yes", "on"}:
        monitor_thread = threading.Thread(target=heartbeat_monitor, daemon=True)
        monitor_thread.start()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server._is_shutting_down = True
        requested_restart = getattr(server, "restart_requested", False)
        server.server_close()
        service.stop()

    return requested_restart
