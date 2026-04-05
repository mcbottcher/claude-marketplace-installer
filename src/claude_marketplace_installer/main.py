import json
import subprocess
import sys
from pathlib import Path


SETTINGS_PATH = Path(".claude").joinpath("settings.json")


def load_settings() -> dict:
    if not SETTINGS_PATH.exists():
        print(f"Error: {SETTINGS_PATH} not found in the current directory.", file=sys.stderr)
        sys.exit(1)

    with SETTINGS_PATH.open() as f:
        try:
            return json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error: Failed to parse {SETTINGS_PATH}: {e}", file=sys.stderr)
            sys.exit(1)


def install_marketplace(name: str, config: dict) -> bool:
    source = config.get("source", {})
    if source.get("source") != "github":
        print(f"  Skipping '{name}': unsupported source type '{source.get('source')}'")
        return False

    repo = source.get("repo")
    if not repo:
        print(f"  Skipping '{name}': missing 'repo' field")
        return False

    print(f"  Installing '{name}' from {repo}...")
    result = subprocess.run(
        ["claude", "plugin", "marketplace", "add", repo],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print(f"  Error installing '{name}':\n{result.stderr.strip()}", file=sys.stderr)
        return False

    print(f"  Done.")
    return True


def main():
    settings = load_settings()
    marketplaces = settings.get("extraKnownMarketplaces", {})

    if not marketplaces:
        print("No marketplaces found in extraKnownMarketplaces.")
        return

    print(f"Found {len(marketplaces)} marketplace(s) to install:\n")
    success, failed = 0, 0
    for name, config in marketplaces.items():
        if install_marketplace(name, config):
            success += 1
        else:
            failed += 1

    print(f"\nDone: {success} installed, {failed} skipped/failed.")
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
