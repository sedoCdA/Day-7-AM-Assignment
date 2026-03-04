"""
Advanced Developer Onboarding Script.

Includes CLI arguments, disk space check, and execution timing.
"""

import sys
import os
import importlib
import subprocess
import shutil
import time
import argparse


def check_python_version(verbose=False):
    """Check Python version is 3.10+."""
    start = time.time()
    v = sys.version_info
    version_str = f"{v.major}.{v.minor}.{v.micro}"
    passed = v.major >= 3 and v.minor >= 10
    message = f"Python version: {version_str} (>= 3.10 required)"
    if verbose:
        message += f"\n         Full: {sys.version}"
    elapsed = time.time() - start
    return passed, message, elapsed


def check_virtual_env(verbose=False):
    """Check if inside a virtual environment."""
    start = time.time()
    in_venv = sys.prefix != sys.base_prefix
    env_name = os.path.basename(sys.prefix) if in_venv else "N/A"
    message = (
        f"Virtual environment: Active ({env_name})"
        if in_venv
        else "Virtual environment: NOT active"
    )
    if verbose and in_venv:
        message += f"\n         Path: {sys.prefix}"
    elapsed = time.time() - start
    return in_venv, message, elapsed


def check_package_installed(package_name, verbose=False, fix=False):
    """Check if a package is importable; optionally auto-install."""
    start = time.time()
    try:
        mod = importlib.import_module(package_name)
        version = getattr(mod, "__version__", "unknown")
        message = f"{package_name} installed: version {version}"
        elapsed = time.time() - start
        return True, message, elapsed
    except ImportError:
        if fix:
            print(f"  Attempting to install {package_name}...")
            subprocess.run(
                [sys.executable, "-m", "pip", "install", package_name],
                check=False,
            )
            try:
                mod = importlib.import_module(package_name)
                version = getattr(mod, "__version__", "unknown")
                elapsed = time.time() - start
                return True, f"{package_name} auto-installed: version {version}", elapsed
            except ImportError:
                pass
        elapsed = time.time() - start
        return False, f"{package_name} NOT installed", elapsed


def check_internet_connectivity(verbose=False):
    """Test internet connectivity."""
    start = time.time()
    try:
        import requests  # pylint: disable=import-outside-toplevel

        response = requests.get("https://httpbin.org/get", timeout=5)
        message = "Internet connectivity: OK"
        if verbose:
            message += f"\n         Response time: {response.elapsed.total_seconds():.2f}s"
        elapsed = time.time() - start
        return True, message, elapsed
    except Exception:  # pylint: disable=broad-except
        elapsed = time.time() - start
        return False, "Internet connectivity: FAILED", elapsed


def check_disk_space(verbose=False):
    """Warn if available disk space is less than 1 GB."""
    start = time.time()
    usage = shutil.disk_usage("/")
    gb_free = usage.free / (1024**3)
    gb_total = usage.total / (1024**3)
    passed = gb_free >= 1.0
    message = f"Disk space: {gb_free:.1f} GB free of {gb_total:.1f} GB"
    if not passed:
        message += " — WARNING: Less than 1 GB free!"
    if verbose:
        gb_used = usage.used / (1024**3)
        message += f"\n         Used: {gb_used:.1f} GB"
    elapsed = time.time() - start
    return passed, message, elapsed


def list_installed_packages():
    """Return string listing all pip packages."""
    result = subprocess.run(
        [sys.executable, "-m", "pip", "list", "--format=columns"],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.stdout


def run_all_checks(verbose=False, fix=False):
    """Run all checks and return results with timing."""
    return [
        check_python_version(verbose),
        check_virtual_env(verbose),
        check_package_installed("pylint", verbose, fix),
        check_package_installed("black", verbose, fix),
        check_internet_connectivity(verbose),
        check_package_installed("numpy", verbose, fix),
        check_disk_space(verbose),
    ]


def generate_report(checks, total_time):
    """Print and save the final report."""
    lines = ["=== Developer Onboarding Check (Advanced) ===\n"]
    passed = 0

    for status, message, elapsed in checks:
        prefix = "[PASS]" if status else "[FAIL]"
        line = f"{prefix} {message}  ({elapsed * 1000:.1f}ms)"
        print(line)
        lines.append(line + "\n")
        if status:
            passed += 1

    total = len(checks)
    symbol = "✓" if passed == total else "✗"
    summary = (
        f"\n---\nResult: {passed}/{total} checks passed {symbol}\n"
        f"Total execution time: {total_time:.3f}s"
    )
    print(summary)
    lines.append(summary + "\n")
    lines.append("\n--- Installed Packages ---\n")
    lines.append(list_installed_packages())

    report_path = "setup_report.txt"
    with open(report_path, "w", encoding="utf-8") as report_file:
        report_file.writelines(lines)
    print(f"\nReport saved to: {report_path}")


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Developer Onboarding Check")
    parser.add_argument(
        "--verbose", action="store_true", help="Show extra details for each check"
    )
    parser.add_argument(
        "--fix", action="store_true", help="Auto-install any missing packages"
    )
    return parser.parse_args()


def main():
    """Entry point."""
    args = parse_args()
    overall_start = time.time()
    checks = run_all_checks(verbose=args.verbose, fix=args.fix)
    total_time = time.time() - overall_start
    generate_report(checks, total_time)


if __name__ == "__main__":
    main()
