from __future__ import annotations

import hmac
import json
import os
import threading
import time
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

from .config import (
    ROOT,
    TUNING_BACKLOG_PATH,
    Settings,
    build_setup_diagnostics,
    load_settings,
    persist_runtime_settings,
    read_runtime_status,
)
from .service import TradeHunterService
from .ruleset import RulesetStore


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
            "anthropic_api_key": bool(os.getenv("ANTHROPIC_API_KEY")),
            "perplexity_api_key": bool(os.getenv("PERPLEXITY_API_KEY")),
            "openai_api_key": bool(os.getenv("OPENAI_API_KEY")),
            "xai_api_key": bool(os.getenv("XAI_API_KEY")),
            "gemini_api_key": bool(os.getenv("GEMINI_API_KEY")),
            "groq_api_key": bool(os.getenv("GROQ_API_KEY")),
        },
    }


def runtime_status_payload(extra_diagnostics: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    entries = [*read_runtime_status(), *(extra_diagnostics or [])]
    latest = entries[-1] if entries else None
    return {"latest": latest, "entries": entries}


def settings_response_payload(settings: Settings, *, is_admin: bool) -> dict[str, Any]:
    return {
        "settings": serialize_settings(settings),
        "is_admin": is_admin,
        "runtime_status": runtime_status_payload(),
    }


def ruleset_response_payload(service: TradeHunterService) -> dict[str, Any]:
    """Read-only snapshot of the tuning ruleset for the Settings panel."""
    store: RulesetStore | None = getattr(service, "ruleset", None)
    if store is None:
        return {"ruleset": None}
    counts = store.counts()
    candidates = store.compaction_candidate()
    # Preview every active rule (scoped ones included), best-first like
    # rules_for_scope orders them: priority, then hits, then recency.
    prio_rank = {"high": 2, "normal": 1, "low": 0}
    active = sorted(
        store.active_rules(),
        key=lambda r: (prio_rank.get(r.priority, 1), r.hit_count, r.created_at),
        reverse=True,
    )
    preview = []
    for r in active[:20]:
        preview.append({
            "id": r.id,
            "text": r.text,
            "scope": {"topic": r.scope.topic, "tier": r.scope.tier},
            "status": r.status,
            "priority": r.priority,
            "hits": r.hit_count,
            "source_tb": r.source_tb,
            "created_at": r.created_at,
        })
    return {
        "ruleset": {
            "counts": counts,
            "compaction_candidate_count": len(candidates),
            "compaction_groups": list(candidates.values())[:20],
            "preview": preview,
        }
    }


def run_server(settings: Settings) -> bool:
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
                state = service.dashboard_state(is_admin=is_admin)
                state["runtime_status"] = runtime_status_payload(
                    build_setup_diagnostics(
                        settings,
                        feed_state=state.get("feeds", {}),
                        invalid_tickers=state.get("config", {}).get("dead_kalshi_markets", []),
                    )
                )
                return self._json_response(state)
            if path == "/api/settings":
                latest_settings = load_settings()
                is_admin = self._require_admin_token(silent=True)
                return self._json_response(settings_response_payload(latest_settings, is_admin=is_admin))
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
                setup_diagnostics = build_setup_diagnostics(
                    settings,
                    feed_state=state.get("feeds", {}),
                    invalid_tickers=state.get("config", {}).get("dead_kalshi_markets", []),
                )
                return self._json_response({
                    "app": "trade-hunter",
                    "feeds": state.get("feeds", {}),
                    "retention": cleanup_status,
                    "runtime_status": runtime_status_payload(setup_diagnostics),
                })
            if path == "/api/tuning/backlog":
                return self._json_response(service.get_tuning_backlog())
            if path == "/api/ruleset":
                return self._json_response(ruleset_response_payload(service))
            if path == "/api/eval/status":
                return self._json_response(service.get_eval_status())
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
                # A hostile page in the user's browser is also a loopback client,
                # so block cross-origin browser requests. Native clients (the
                # launcher replacing an old instance) send no Origin and pass.
                if not self._reject_cross_origin_browser():
                    return

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
                if not hmac.compare_digest(auth, expected):
                    return self._json_response(
                        {"error": "unauthorized"},
                        status=HTTPStatus.UNAUTHORIZED,
                    )
            elif self.path == "/api/events" and settings.ingest_api_token:
                # Generic /api/events endpoint uses INGEST_API_TOKEN
                auth = self.headers.get("Authorization", "")
                expected = f"Bearer {settings.ingest_api_token}"
                if not hmac.compare_digest(auth, expected):
                    return self._json_response(
                        {"error": "unauthorized"},
                        status=HTTPStatus.UNAUTHORIZED,
                    )

            if self.path == "/api/demo/spike":
                # Dashboard-only trigger; block hostile cross-origin browser POSTs
                # that would otherwise inject fake spikes into a loopback instance.
                if not self._require_same_origin():
                    return
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
                try:
                    content_length = int(self.headers.get("Content-Length") or 0)
                except ValueError:
                    return self._json_response({"error": "invalid content-length"}, status=HTTPStatus.BAD_REQUEST)
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
                    "runtime_status": runtime_status_payload(),
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
                try:
                    result = service.ingest_payload(payload, default_source=source)
                except ValueError as exc:
                    return self._json_response({"error": str(exc)}, status=HTTPStatus.BAD_REQUEST)
                except Exception:
                    return self._json_response(
                        {"error": "internal server error"},
                        status=HTTPStatus.INTERNAL_SERVER_ERROR,
                    )

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
                if hmac.compare_digest(token, settings.admin_token):
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
                if hmac.compare_digest(token, settings.ingest_api_token):
                    return True
            self._json_response({"error": "unauthorized ingest"}, status=HTTPStatus.UNAUTHORIZED)
            return False

        @staticmethod
        def _netloc_parts(value: str) -> tuple[str, int | None] | None:
            """Return (hostname, port) for an Origin/Referer/Host value.

            Returns None when the value is malformed (e.g. a non-numeric port, as
            in the classic ``http://127.0.0.1:8765.evil.com`` bypass). Loopback
            aliases are normalized so 127.0.0.1 / localhost / ::1 compare equal.
            """
            # The Host header has no scheme; give urlsplit an authority to parse.
            if "://" not in value:
                value = "//" + value
            try:
                parts = urlsplit(value)
                host = parts.hostname
                port = parts.port  # raises ValueError on a non-numeric port
            except ValueError:
                return None
            if not host:
                return None
            if host in {"127.0.0.1", "localhost", "::1"}:
                host = "localhost"
            return (host, port)

        def _require_same_origin(self) -> bool:
            """CSRF protection: the request's Origin/Referer must have the exact
            same host:port the browser connected to (the Host header).

            Substring matching is deliberately avoided — an attacker page at
            ``http://localhost.evil.com`` or ``http://127.0.0.1:8765.evil.com``
            must not pass.
            """
            origin = self.headers.get("Origin") or self.headers.get("Referer")
            if not origin:
                self._json_response({"error": "missing origin/referer"}, status=HTTPStatus.BAD_REQUEST)
                return False

            host = self.headers.get("Host")
            if not host:
                self._json_response({"error": "missing host header"}, status=HTTPStatus.BAD_REQUEST)
                return False

            origin_parts = self._netloc_parts(origin)
            host_parts = self._netloc_parts(host)
            if origin_parts is None or host_parts is None or origin_parts != host_parts:
                self._json_response({"error": "csrf origin mismatch"}, status=HTTPStatus.FORBIDDEN)
                return False
            return True

        def _reject_cross_origin_browser(self) -> bool:
            """Guard for endpoints reachable by BOTH the dashboard and native
            loopback clients (e.g. the launcher's instance-replacement shutdown).

            A browser cross-origin POST always carries an Origin header, so if one
            is present we enforce same-origin. Native clients send no Origin and
            are allowed (they are already loopback-gated by the caller).
            Returns True when the request may proceed.
            """
            if not self.headers.get("Origin") and not self.headers.get("Referer"):
                return True
            return self._require_same_origin()

    try:
        server = ThreadingHTTPServer((settings.host, settings.port), Handler)
    except Exception:
        service.stop()
        raise
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
