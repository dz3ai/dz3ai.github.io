#!/usr/bin/env python3
"""Import blog posts from dz3ai source repos into this site.

Reads _data/sources.yml, lists each source repo's _posts/ directory via the
GitHub API, and copies any post that does not already exist in the local
_posts/. Imported posts get `source_repo` and `canonical_url` front matter
stamped so the site can attribute and link back to the original.

Usage:
    python scripts/sync_source_posts.py

Environment:
    GITHUB_TOKEN  optional; raises API rate limits (the workflow provides it)
"""
import base64
import json
import os
import re
import sys
import urllib.request
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML is required: pip install pyyaml")

ROOT = Path(__file__).resolve().parent.parent
POSTS_DIR = ROOT / "_posts"
SOURCES = ROOT / "_data" / "sources.yml"
API = "https://api.github.com"


def api(url: str) -> dict | list:
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json"})
    token = os.environ.get("GITHUB_TOKEN") or gh_token()
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req) as res:
        return json.loads(res.read())


def gh_token() -> str | None:
    """Fall back to the gh CLI token when GITHUB_TOKEN is unset."""
    if getattr(gh_token, "_cached", None):
        return gh_token._cached
    try:
        import subprocess
        tok = subprocess.run(["gh", "auth", "token"], capture_output=True,
                             text=True).stdout.strip()
        gh_token._cached = tok or None
    except FileNotFoundError:
        gh_token._cached = None
    return gh_token._cached


def canonical_url(spec: dict, filename: str) -> str:
    """Build the original post URL from the source repo's permalink style."""
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})-(.+)\.md$", filename)
    if not m:
        return f"{spec['site_base']}/"
    year, month, day, slug = m.groups()
    path = (spec.get("permalink_style", "/posts/:slug/")
            .replace(":year", year).replace(":month", month)
            .replace(":day", day).replace(":slug", slug))
    return spec["site_base"] + path


def stamp_front_matter(text: str, extra: dict) -> str:
    """Append keys to an existing front matter block, or create one."""
    if text.startswith("---\n"):
        m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
        block, rest = m.group(1), text[m.end():]
        lines = block.split("\n")
        for k, v in extra.items():
            if not re.search(rf"^{re.escape(k)}:", block, re.MULTILINE):
                lines.append(f"{k}: {v}")
        return "---\n" + "\n".join(lines) + "\n---\n" + rest
    fm = "\n".join(f"{k}: {v}" for k, v in extra.items())
    return f"---\n{fm}\n---\n\n" + text


def main() -> None:
    sources = yaml.safe_load(SOURCES.read_text())
    POSTS_DIR.mkdir(exist_ok=True)

    imported, skipped = [], []
    for spec in sources:
        repo = spec["repo"]
        posts_dir = spec.get("posts_dir", "_posts")
        try:
            entries = api(f"{API}/repos/dz3ai/{repo}/contents/{posts_dir}")
        except Exception as e:
            print(f"warn: could not list {repo}/{posts_dir}: {e}")
            continue

        for entry in entries:
            name = entry["name"]
            if not name.endswith(".md") or entry["type"] != "file":
                continue
            local = POSTS_DIR / name
            if local.exists():
                skipped.append(name)
                continue
            try:
                raw = api(entry["url"])
                text = base64.b64decode(raw["content"]).decode("utf-8")
                text = stamp_front_matter(text, {
                    "source_repo": repo,
                    "canonical_url": canonical_url(spec, name),
                })
                local.write_text(text)
                imported.append(name)
                print(f"imported: {repo}/{posts_dir}/{name}")
            except Exception as e:
                print(f"warn: failed to import {repo}/{name}: {e}")

    print(f"\ndone: {len(imported)} imported, {len(skipped)} already present")


if __name__ == "__main__":
    main()
