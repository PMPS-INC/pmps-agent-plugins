"""Check that every manifest parses, points at the same MCP URL and carries the same version.

Usage: python scripts/validate.py
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
URL = "https://api.pmps.ai/mcp"
PLUGIN = ROOT / "plugins" / "pmps"

MANIFESTS = {
    ".claude-plugin/marketplace.json": None,
    ".agents/plugins/marketplace.json": None,
    ".cursor-plugin/marketplace.json": None,
    ".github/plugin/marketplace.json": None,
    "plugins/pmps/.claude-plugin/plugin.json": "version",
    "plugins/pmps/.cursor-plugin/plugin.json": "version",
    "plugins/pmps/plugin.json": "version",
    "plugins/pmps/.mcp.json": None,
    "plugins/pmps/mcp.json": None,
    "gemini-extension.json": "version",
    "server.json": "version",
}


def main() -> int:
    errors: list[str] = []
    docs = {}
    for rel in MANIFESTS:
        try:
            docs[rel] = json.loads((ROOT / rel).read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            errors.append(f"{rel}: {exc}")
    if errors:
        print("\n".join(errors))
        return 1

    versions = {rel: docs[rel].get("version") for rel, key in MANIFESTS.items() if key}
    if len(set(versions.values())) != 1:
        errors.append(f"versions differ: {versions}")

    urls = {
        "plugins/pmps/.mcp.json": docs["plugins/pmps/.mcp.json"]["mcpServers"]["pmps"]["url"],
        "plugins/pmps/mcp.json": docs["plugins/pmps/mcp.json"]["mcpServers"]["pmps"]["url"],
        "plugins/pmps/.cursor-plugin/plugin.json": docs["plugins/pmps/.cursor-plugin/plugin.json"]["mcpServers"]["pmps"]["url"],
        "gemini-extension.json": docs["gemini-extension.json"]["mcpServers"]["pmps"]["httpUrl"],
        "server.json": docs["server.json"]["remotes"][0]["url"],
    }
    errors += [f"{rel}: MCP URL {url!r} != {URL!r}" for rel, url in urls.items() if url != URL]

    for rel in ("plugins/pmps/.claude-plugin/plugin.json", "plugins/pmps/.cursor-plugin/plugin.json", "plugins/pmps/plugin.json"):
        if docs[rel]["name"] != "pmps":
            errors.append(f"{rel}: name must be 'pmps'")
    for rel in (".claude-plugin/marketplace.json", ".cursor-plugin/marketplace.json", ".github/plugin/marketplace.json", ".agents/plugins/marketplace.json"):
        for entry in docs[rel]["plugins"]:
            source = entry["source"] if isinstance(entry["source"], str) else entry["source"]["path"]
            if not (ROOT / source).is_dir():
                errors.append(f"{rel}: source {source!r} is not a directory")
            if entry["name"] != "pmps":
                errors.append(f"{rel}: entry name {entry['name']!r} does not match plugin name")

    openai = docs["plugins/pmps/plugin.json"]["extensions"]["com.openai"]
    try:
        apps = json.loads((PLUGIN / openai["apps"]).read_text(encoding="utf-8"))["apps"]
        if not all(str(app.get("id", "")).startswith(("asdk_app_", "plugin_asdk_app")) for app in apps.values()):
            errors.append("plugins/pmps/.app.json: every app needs a ChatGPT app id")
    except (KeyError, OSError, ValueError) as exc:
        errors.append(f"plugins/pmps/.app.json: {exc}")

    interface = openai["interface"]
    for key in ("logo", "composerIcon"):
        if not (PLUGIN / interface[key]).is_file():
            errors.append(f"plugins/pmps/plugin.json: {key} {interface[key]!r} is missing")
    if not (PLUGIN / docs["plugins/pmps/.cursor-plugin/plugin.json"]["logo"]).is_file():
        errors.append("plugins/pmps/.cursor-plugin/plugin.json: logo is missing")

    print("\n".join(errors) or "All manifests are consistent.")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
