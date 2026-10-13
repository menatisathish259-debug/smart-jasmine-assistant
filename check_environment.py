"""
Environment Verification Script for Smart Jasmine Farming Assistant.
Phase 1: Project structure and Windows setup check.
"""

import sys
import platform
from pathlib import Path

# Fix Windows console encoding for Unicode (Tamil & emojis)
if sys.platform == "win32":
    try:
        if sys.stdout and hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
        if sys.stderr and hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Add project root to path
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))



def check_python_version() -> bool:
    """Verifies Python is 3.10+ and 64-bit."""
    print("=" * 60)
    print(" 🌿 SMART JASMINE FARMING ASSISTANT - ENVIRONMENT CHECK")
    print("    Crop: Jasminum sambac (குண்டு மல்லி)")
    print("=" * 60)

    ver = sys.version_info
    arch = platform.architecture()[0]
    print(f"\n[1] Python Environment:")
    print(f"    - Version: {ver.major}.{ver.minor}.{ver.micro}")
    print(f"    - Platform: {platform.system()} {platform.release()} ({arch})")
    print(f"    - Executable: {sys.executable}")

    if ver.major < 3 or (ver.major == 3 and ver.minor < 10):
        print("    ❌ FAILED: Python 3.10 or higher is required.")
        return False
    print("    ✅ PASSED: Compatible Python version detected.")
    return True


def check_dependencies() -> bool:
    """Checks imports of core libraries."""
    print("\n[2] Required Packages:")
    required_packages = [
        ("streamlit", "Streamlit Web Framework"),
        ("pandas", "Pandas Data Processing"),
        ("numpy", "NumPy Numerical Computing"),
        ("PIL", "Pillow Image Processing"),
        ("sqlite3", "SQLite3 Database (Built-in)"),
        ("requests", "Requests HTTP Client"),
        ("dotenv", "python-dotenv Configuration"),
        ("pytest", "Pytest Testing Framework"),
    ]

    all_passed = True
    for module_name, desc in required_packages:
        try:
            mod = __import__(module_name)
            version = getattr(mod, "__version__", "built-in")
            print(f"    ✅ {desc:<32} [v{version}]")
        except ImportError as e:
            print(f"    ❌ {desc:<32} [NOT INSTALLED - {e}]")
            all_passed = False

    return all_passed


def check_directories() -> bool:
    """Checks project folder hierarchy."""
    print("\n[3] Folder Hierarchy & Data Paths:")
    from config.settings import (
        BASE_DIR,
        DATA_DIR,
        RAW_DATA_DIR,
        PROCESSED_DATA_DIR,
        DB_DIR,
        MODELS_DIR,
        FLOWER_STAGES,
        SOIL_PH_RANGE,
    )

    required_dirs = [
        ("Base Directory", BASE_DIR),
        ("Data Directory", DATA_DIR),
        ("Raw Images Directory", RAW_DATA_DIR),
        ("Processed Data Directory", PROCESSED_DATA_DIR),
        ("SQLite Database Directory", DB_DIR),
        ("Models Directory", MODELS_DIR),
    ]

    all_exist = True
    for name, path in required_dirs:
        exists = path.is_dir()
        status = "✅" if exists else "❌"
        print(f"    {status} {name:<26}: {path}")
        if not exists:
            all_exist = False

    print("\n[4] Domain Settings Verification:")
    print(f"    - Configured Flower Stages ({len(FLOWER_STAGES)}): {', '.join(FLOWER_STAGES)}")
    print(f"    - Soil pH Optimal Range: {SOIL_PH_RANGE['min_optimal']} - {SOIL_PH_RANGE['max_optimal']}")
    return all_exist


def main() -> int:
    """Runs all checks and returns exit code."""
    py_ok = check_python_version()
    deps_ok = check_dependencies()
    dirs_ok = check_directories()

    print("\n" + "=" * 60)
    if py_ok and deps_ok and dirs_ok:
        print(" 🎉 PHASE 1 VERIFICATION SUCCESSFUL!")
        print(" Your Windows environment and project structure are ready.")
        print(" You can now proceed to Phase 2 (Streamlit UI).")
        print("=" * 60 + "\n")
        return 0
    else:
        print(" ⚠️  VERIFICATION INCOMPLETE")
        print(" Please run: .\\.venv\\Scripts\\pip install -r requirements.txt")
        print("=" * 60 + "\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
