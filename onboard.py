"""
Developer Onboarding Check Script.

Verifies that a new developer's Python environment is correctly configured.
"""

import sys
import os
import importlib
import subprocess


def check_python_version():
    """Check if Python version is 3.10 or higher."""
    v = sys.version_info
    version_str = f"{v.major}.{v.minor}.{v.micro}"
    if v.major >= 3 and v.minor >= 10:
        return True, f"Python version: {version_str} (>= 3.10 required)"
    return False, f"Python version: {version_str} — WARNING: requires 3.10+"


def check_virtual_env():
    """Check if running inside a virtual environment."""
    in_venv = sys.prefix != sys.base_prefix
    if in_venv:
        env_name = os.path.basename(sys.prefix)
        return True, f"Virtual environment: Active ({env_name})"
    return False, "Virtual environment: NOT active — please activate one!"


def check_package_installed(package_name):
    """Check if a package is installed and return its version."""
    try:
        mod = importlib.import_module(package_name)
        version = getattr(mod, "__version__", "unknown")
        return True, f"{package_name} installed: version {version}"
    except ImportError:
        return False, f"{package_name} NOT installed"


def check_internet_connectivity():
    """Test internet connectivity by making a request to a public URL."""
    try:
        import requests  # pylint: disable=import-outside-toplevel

        response = requests.get("https://httpbin.org/get", timeout=5)
        if response.status_code == 200:
            return True, "Internet connectivity: OK"
        return False, f"Internet connectivity: FAILED (status {response.status_code})"
    except Exception:  # pylint: disable=broad-except
        return False, "Internet connectivity: FAILED (no connection)"


def list_installed_packages():
    """List all installed packages with versions."""
    result = subprocess.run(
        [sys.executable, "-m", "pip", "list", "--format=columns"],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.stdout


def run_all_checks():
    """Run all onboarding checks and return results."""
    checks = [
        check_python_version(),
        check_virtual_env(),
        check_package_installed("pylint"),
        check_package_installed("black"),
        check_internet_connectivity(),
        check_package_installed("numpy"),
    ]
    return checks


def generate_report(checks):
    """Generate and print a summary report, then save it to a file."""
    lines = ["=== Developer Onboarding Check ===\n"]

    passed = 0
    for status, message in checks:
        prefix = "[PASS]" if status else "[FAIL]"
        line = f"{prefix} {message}"
        print(line)
        lines.append(line + "\n")
        if status:
            passed += 1

    total = len(checks)
    symbol = "✓" if passed == total else "✗"
    summary = f"\n---\nResult: {passed}/{total} checks passed {symbol}"
    print(summary)
    lines.append(summary + "\n")

    lines.append("\n--- Installed Packages ---\n")
    lines.append(list_installed_packages())

    report_path = "setup_report.txt"
    with open(report_path, "w", encoding="utf-8") as report_file:
        report_file.writelines(lines)

    print(f"Report saved to: {report_path}")


def main():
    """Entry point for the onboarding script."""
    checks = run_all_checks()
    generate_report(checks)


if __name__ == "__main__":
    main()
