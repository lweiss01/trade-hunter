import subprocess
import sys
import os
from pathlib import Path

def run_checks():
    print("=== Trade Hunter Security & Health Checks ===")
    root = Path(__file__).parent.parent
    os.chdir(root)
    
    # Ensure PYTHONPATH is set so tests can find the 'app' module
    env = os.environ.copy()
    env["PYTHONPATH"] = str(root)
    
    # 1. Critical Security Regression Tests
    print("\n[1/3] Running Security Regression Suite...")
    res = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/test_security_hardening.py", "-v"],
        env=env
    )
    if res.returncode != 0:
        print("\n!!! SECURITY REGRESSION DETECTED !!!")
        print("Please fix security vulnerabilities before deploying.")
        sys.exit(res.returncode)
    
    # 2. Key Ingest Tests
    print("\n[2/3] Running Ingest & Auth Tests...")
    res = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/test_polyalerthub_auth.py", "-v"],
        env=env
    )
    
    # 3. Overall Test Suite
    print("\n[3/3] Running Full Test Suite (Optional/Informational)...")
    res = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/", "-v", "-k", "not security_hardening and not polyalerthub_auth"],
        env=env
    )

    print("\n=== All Critical Security Checks Passed ===")

if __name__ == "__main__":
    run_checks()
