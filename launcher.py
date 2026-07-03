"""
Trade Hunter Launcher
Professional entry point for PyInstaller bundles to ensure correct package resolution.
Handles single-instance locking, kernel-level stealth startup, and automatic browser dashboard launch.
"""
import sys
import ctypes
import os
import platform
import re
import threading
import time
import datetime
from pathlib import Path

# --- ATOMIC STEALTH & MUTEX ---
# This block must execute in sub-milliseconds before heavy imports.
_MUTEX_HANDLE = None

# Deterministic tracking root directly matching the true binary environment context directory
EXE_DIR = os.path.dirname(os.path.abspath(sys.executable if getattr(sys, "frozen", False) else __file__))


def ensure_single_instance():
    global _MUTEX_HANDLE

    if platform.system() != "Windows":
        return True

    if _MUTEX_HANDLE:
        return True

    kernel32 = ctypes.windll.kernel32
    mutex_name = os.getenv("TRADE_HUNTER_MUTEX_NAME", "Global\\TradeHunter_v029_Atomic")
    mutex = kernel32.CreateMutexW(None, False, mutex_name)
    if kernel32.GetLastError() == 183: # ERROR_ALREADY_EXISTS
        return False

    _MUTEX_HANDLE = mutex
    return True


def _boot_log_candidates():
    # Force anchoring to the static pathing frame to avoid runtime working directory drift issues
    paths = [os.path.join(EXE_DIR, "trade-hunter-boot.log")]
    data_root = os.getenv("TRADE_HUNTER_DATA_ROOT")
    if data_root:
        paths.append(os.path.join(data_root, "trade-hunter-boot.log"))
    local_app_data = os.getenv("LOCALAPPDATA") or os.getenv("APPDATA")
    if local_app_data:
        paths.append(os.path.join(local_app_data, "Trade Hunter", "trade-hunter-boot.log"))
    return paths


def _early_boot_log(message):
    try:
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = f"[{timestamp}] {message}\n"
        for log_path in _boot_log_candidates():
            try:
                os.makedirs(os.path.dirname(log_path), exist_ok=True)
                with open(log_path, "a", encoding="utf-8") as f:
                    f.write(line)
                return
            except Exception:
                pass
    except Exception:
        pass


def _read_port_from_env_file(env_path):
    try:
        with open(env_path, encoding="utf-8") as f:
            for raw_line in f:
                line = raw_line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                if key.strip() in {"APP_PORT", "PORT"}:
                    p = int(value.strip().strip('"').strip("'"))
                    # Assert network assignment boundaries safely
                    if 1 <= p <= 65535:
                        return p
    except Exception:
        return None
    return None


def _existing_dashboard_port():
    env_paths = []
    data_root = os.getenv("TRADE_HUNTER_DATA_ROOT")
    if data_root:
        env_paths.append(os.path.join(data_root, ".env"))

    env_paths.append(os.path.join(EXE_DIR, ".env"))

    local_app_data = os.getenv("LOCALAPPDATA") or os.getenv("APPDATA")
    if local_app_data:
        env_paths.append(os.path.join(local_app_data, "Trade Hunter", ".env"))

    for env_path in env_paths:
        port = _read_port_from_env_file(env_path)
        if port:
            return port
    return 8765


def _wait_for_dashboard_ready(port, timeout_seconds=8.0):
    import urllib.error
    import urllib.request

    url = f"http://127.0.0.1:{port}/api/health"
    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=0.75) as response:
                if response.status == 200:
                    return True
        except (OSError, urllib.error.URLError, TimeoutError):
            time.sleep(0.25)
    return False


def _open_existing_dashboard_from_mutex_conflict():
    port = _existing_dashboard_port()
    ready = _wait_for_dashboard_ready(port)
    url = f"http://127.0.0.1:{port}"
    _early_boot_log(
        f"LAUNCH: Existing instance detected; opening dashboard at {url}"
        if ready else
        f"LAUNCH: Existing instance detected but health check did not answer; opening {url} anyway"
    )
    try:
        if platform.system() == "Windows":
            os.startfile(url)
        else:
            import webbrowser
            webbrowser.open(url)
    except Exception as e:
        _early_boot_log(f"ERROR: Failed to open existing dashboard: {e}")


def atomic_init():
    if platform.system() != "Windows":
        return True
    
    # 1. Hide Console (Zero-Flicker)
    kernel32 = ctypes.windll.kernel32
    user32 = ctypes.windll.user32
    
    # Tiny delay to ensure console window is registered by OS
    hwnd = kernel32.GetConsoleWindow()
    if not hwnd:
        time.sleep(0.05) 
        hwnd = kernel32.GetConsoleWindow()
        
    if hwnd:
        user32.ShowWindow(hwnd, 0) # SW_HIDE
    
    # 2. Single Instance Mutex
    return ensure_single_instance()

if __name__ == "__main__" and not atomic_init():
    _open_existing_dashboard_from_mutex_conflict()
    sys.exit(0)

# --- HEAVY IMPORTS ---
# Add the project root to sys.path
root = Path(__file__).resolve().parent
if str(root) not in sys.path:
    sys.path.insert(0, str(root))

def _boot_log_paths():
    unique_paths = []
    seen = set()
    for raw_path in _boot_log_candidates():
        path = Path(raw_path)
        key = str(path).lower() if platform.system() == "Windows" else str(path)
        if key not in seen:
            unique_paths.append(path)
            seen.add(key)
    return unique_paths


def log_boot(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {message}\n"
    wrote = False
    for log_path in _boot_log_paths():
        try:
            log_path.parent.mkdir(parents=True, exist_ok=True)
            with open(log_path, "a") as f:
                f.write(line)
            wrote = True
        except Exception:
            pass
    if wrote:
        return
    try:
        print(line, end="")
    except:
        pass

from app.__main__ import main
from app.config import load_settings, record_runtime_status


def _sanitize_startup_detail(value):
    text = str(value)
    # Target complex spacing variations, assignments, and structural wrappers
    patterns = [
        r'(?i)(\btoken\b|\bapi_key\b|\bwebhook\b|\bprivate_key\b|\bsecret\b|\baccess_token\b|\brefresh_token\b)\s*[:=]\s*[^\s,;}]+',
        r'(?i)\bbearer\s+[^\s,;}]+'
    ]
    for pat in patterns:
        text = re.sub(pat, r'\1=[redacted]', text)
        
    # Multi-pattern check matching explicit JSON object formats
    json_pat = r'"(token|api_key|webhook|private_key|secret|access_token|refresh_token)"\s*:\s*"[^"]*"'
    text = re.sub(json_pat, r'"\1":"[redacted]"', text, flags=re.I)
    
    return text[:500]


def _is_port_busy_error(exc):
    message = str(exc).lower()
    errno = getattr(exc, "errno", None)
    winerror = getattr(exc, "winerror", None)
    return (
        errno in {48, 98, 10048}
        or winerror == 10048
        or "address already in use" in message
        or "only one usage of each socket address" in message
        or "port" in message and "use" in message
    )


def _record_startup_failure_diagnostic(settings, exc):
    if not _is_port_busy_error(exc):
        return

    port = getattr(settings, "port", _existing_dashboard_port())
    buyer_headline = "Trade Hunter could not start because the dashboard port is already in use."
    support_detail = (
        f"category=port_busy port={port} "
        f"exception={exc.__class__.__name__}: {_sanitize_startup_detail(exc)}"
    )
    try:
        record_runtime_status(
            "port_busy",
            buyer_headline,
            support_detail,
            details={
                "category": "port_busy",
                "port": port,
                "exception_class": exc.__class__.__name__,
                "message": _sanitize_startup_detail(exc),
            },
        )
    except Exception:
        pass
    log_boot(f"STARTUP DIAGNOSTIC: {buyer_headline} Support detail: {support_detail}")


def auto_launch_dashboard(host, port):
    """Wait for server health, then open the browser silently."""
    url = f"http://127.0.0.1:{port}" # Use explicit loopback for authority
    if not _wait_for_dashboard_ready(port, timeout_seconds=20.0):
        log_boot(f"WARN: Dashboard health check timed out; opening {url} anyway")
    log_boot(f"LAUNCH: Opening dashboard at {url}")
    
    try:
        if platform.system() == "Windows":
            os.startfile(url)
        else:
            import webbrowser
            webbrowser.open(url)
    except Exception as e:
        log_boot(f"ERROR: Failed to launch browser: {e}")
        import webbrowser
        webbrowser.open(url)


def run_launcher():
    log_boot("--- ATOMIC BOOT v0.3.0 ---")
    launch_browser = os.getenv("TRADE_HUNTER_NO_BROWSER") != "1"

    while True:
        try:
            settings = load_settings()
            log_boot(f"CONFIG: Loaded settings (Port: {settings.port})")
        except Exception as e:
            log_boot(f"ERROR: Settings load failed: {e}")
            return 1

        if launch_browser:
            threading.Thread(
                target=auto_launch_dashboard,
                args=(settings.host, settings.port),
                daemon=True
            ).start()
            launch_browser = False

        try:
            log_boot("ENGINE: Starting Core Logic")
            exit_code = main()
        except Exception as e:
            _record_startup_failure_diagnostic(settings, e)
            log_boot(f"FATAL: Engine crashed: {e}")
            return 1

        if exit_code == 3:
            log_boot("ENGINE: Restart requested; relaunching server")
            time.sleep(0.5)
            continue

        return exit_code


if __name__ == "__main__":
    sys.exit(run_launcher())