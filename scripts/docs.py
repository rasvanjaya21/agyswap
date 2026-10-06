"""Mirror the official docs of every stack dependency into docs/, pinned to the exact version agyswap locks.

Versions come from uv.lock. Run with `uv run python scripts/docs.py` after a version bump.
"""

from __future__ import annotations

import re
import shutil
import subprocess
import tempfile
import tomllib
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs"
TODAY = date.today().isoformat()

# Release notes, project governance and generated plugin lists: large and not about the API we use.
PYTEST_SKIP = re.compile(
    r"^(changelog|announce/.*|historical-notes|history|talks|sponsor|tidelift|license|contact|"
    r"contributing|backwards-compatibility|development_guide|reference/plugin_list)$"
)


# Autodoc-only API pages render to nothing without Sphinx.
RICH_SKIP = re.compile(r"^reference(/.*)?$")


def lock_version(name: str) -> str:
    lock = tomllib.loads((ROOT / "uv.lock").read_text())
    return next(p["version"] for p in lock["package"] if p["name"] == name)


def run(args: list[str], cwd: Path | None = None) -> str:
    return subprocess.run(args, cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()


def checkout(repo: str, tag: str, sparse: list[str]) -> tuple[Path, str]:
    d = Path(tempfile.mkdtemp(prefix="agyswap-docs-"))
    run(
        [
            "git",
            "clone",
            "--quiet",
            "--depth",
            "1",
            "--branch",
            tag,
            "--filter=blob:none",
            "--sparse",
            f"https://github.com/{repo}",
            str(d),
        ]
    )
    run(["git", "sparse-checkout", "set", "--no-cone", *sparse], d)
    return d, run(["git", "rev-parse", "--short", "HEAD"], d)


def md_page(path: str, url: str, body: str) -> tuple[str, str, str]:
    """Pages starting with their own H1 keep it as title; otherwise the path is the title."""
    body = re.sub(r"\A---\n.*?\n---\n", "", body, flags=re.S).strip()
    if body.startswith("# "):
        first, _, rest = body.partition("\n")
        return first[2:], url, rest.strip()
    return path, url, body


def rst_title(body: str, fallback: str) -> str:
    lines = body.splitlines()
    for i in range(len(lines) - 1):
        under = lines[i + 1].strip()
        if lines[i].strip() and len(under) >= 3 and len(set(under)) == 1 and under[0] in "=-~*#^\"'`":
            return lines[i].strip()
    return fallback


def toctree(root: Path, start: str, skip: re.Pattern | None = None) -> list[str]:
    """Docnames in Sphinx toctree order, depth first from `start`."""
    order: list[str] = []

    def walk(name: str) -> None:
        if name in order or (skip and skip.match(name)) or not (root / f"{name}.rst").exists():
            return
        order.append(name)
        text = (root / f"{name}.rst").read_text()
        base = name.rpartition("/")[0]
        for block in re.finditer(r"^\.\. toctree::\n((?:[ \t]+.*\n|[ \t]*\n)*)", text, re.M):
            for line in block.group(1).splitlines():
                entry = line.strip()
                if not entry or entry.startswith(":"):
                    continue
                entry = re.sub(r"^.*<(.+)>$", r"\1", entry)  # "Title <target>"
                if "://" in entry:
                    continue
                entry = entry.removesuffix(".rst")
                walk(entry.lstrip("/") if entry.startswith("/") else f"{base}/{entry}".lstrip("/"))

    walk(start)
    return order


def textual_pages(d: Path) -> list[tuple[str, str, str]]:
    nav = (d / "mkdocs-nav.yml").read_text()
    paths = dict.fromkeys(re.findall(r'"([^"]+\.md)"', nav))  # ordered, unique
    snippet = re.compile(r'^([ \t]*)--8<--\s*"([^"]+)"\s*$', re.M)

    def expand(body: str) -> str:
        def sub(m: re.Match) -> str:
            # mkdocs resolves snippet paths against the repo root and docs/.
            f = next((b / m.group(2) for b in (d, d / "docs") if (b / m.group(2)).is_file()), None)
            if not f or f.suffix == ".svg":  # inline screenshots are noise in text
                return m.group(0)
            return m.group(1) + expand(f.read_text()).replace("\n", "\n" + m.group(1))  # snippets nest

        return snippet.sub(sub, body)

    pages = []
    for p in paths:
        f = d / "docs" / p
        if p.startswith(("api/", "blog/")) or not f.exists():
            continue
        url = "https://textual.textualize.io/" + re.sub(r"(^|/)index\.md$", r"\1", p).removesuffix(".md")
        pages.append(md_page(p, url, expand(f.read_text())))
    return pages


def rst_pages(root: Path, start: str, url: str, skip: re.Pattern | None = None) -> list[tuple[str, str, str]]:
    pages = []
    for name in toctree(root, start, skip):
        body = (root / f"{name}.rst").read_text().strip()
        if body:
            pages.append((rst_title(body, name), f"{url}{name}.html", body))
    return pages


def write(file: str, title: str, version: str, source: str, note: str, pages: list[tuple[str, str, str]]) -> None:
    header = "\n".join(
        [
            f"# {title}",
            "",
            f"- Version: **{version}**",
            f"- Source: {source}",
            f"- Mirrored: {TODAY}",
            "",
            note,
            "",
            "Complete official documentation for this exact version, mirrored for offline use. "
            "Not written by hand; regenerate it with `uv run python scripts/docs.py` instead of editing it.",
            "",
            "---",
            "",
        ]
    )
    body = "\n".join(f"# {t}\nSource: {u}\n\n{b}\n" for t, u, b in pages)
    (OUT / file).write_text(f"{header}\n{body}")
    print(f"{file}: {len(pages)} pages ({version})")


DOCS = [
    {
        "file": "textual.md",
        "title": "Textual documentation",
        "pkg": "textual",
        "repo": "Textualize/textual",
        "tag": "v{v}",
        "sparse": ["/docs/", "/examples/", "/mkdocs-nav.yml"],
        "note": "Pages follow the navigation order of `mkdocs-nav.yml`; `--8<--` snippets are inlined. "
        "`api/` (only mkdocstrings `:::` directives) and `blog/` are left out.",
        "pages": textual_pages,
    },
    {
        "file": "rich.md",
        "title": "Rich documentation",
        "pkg": "rich",
        "repo": "Textualize/rich",
        "tag": "v{v}",
        "sparse": ["/docs/"],
        "note": "Pages follow the Sphinx toctree from `docs/source/index.rst`, kept as reStructuredText. "
        "`reference/` is left out: its pages are only autodoc directives.",
        "pages": lambda d: rst_pages(d / "docs/source", "index", "https://rich.readthedocs.io/en/stable/", RICH_SKIP),
    },
    {
        "file": "pytest.md",
        "title": "pytest documentation",
        "pkg": "pytest",
        "repo": "pytest-dev/pytest",
        "tag": "{v}",
        "sparse": ["/doc/en/"],
        "note": "Pages follow the Sphinx toctree from `doc/en/index.rst`, kept as reStructuredText. "
        "Changelog, announcements, project/governance pages and the generated plugin list are left out.",
        "pages": lambda d: rst_pages(d / "doc/en", "index", "https://docs.pytest.org/en/stable/", PYTEST_SKIP),
    },
]

if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for doc in DOCS:
        version = lock_version(doc["pkg"])
        tag = doc["tag"].format(v=version)
        d, commit = checkout(doc["repo"], tag, doc["sparse"])
        try:
            paths = ", ".join(s.strip("/") for s in doc["sparse"])
            source = f"https://github.com/{doc['repo']}/tree/{tag} ({paths}; commit `{commit}`)"
            write(doc["file"], doc["title"], version, source, doc["note"], doc["pages"](d))
        finally:
            shutil.rmtree(d, ignore_errors=True)
