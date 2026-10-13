"""Conservative, dependency-free audit for a curated Portal Air publication tree.

The tool intentionally treats suspicious material as a finding rather than trying
to redact it. It is safe to run on the internal repository or a candidate tree:
it reads files only and prints paths, rule names, and line numbers -- never the
matched value.
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import re
from collections import Counter
from pathlib import Path
from typing import Iterable


TEXT_LIMIT_BYTES = 2_000_000
SKIP_DIRS = {".git", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", ".venv", "venv", "node_modules"}

# These patterns identify likely credential material or exact geographic values.
# A match is a review finding, not proof that a secret is present.
CONTENT_RULES: tuple[tuple[str, str, re.Pattern[str]], ...] = (
    ("P0", "private-key", re.compile(r"-----BEGIN(?: [A-Z0-9]+)? PRIVATE KEY-----", re.I)),
    ("P0", "authorization-header", re.compile(r"\bAuthorization\s*:\s*(?:Basic|Bearer)\s+[^\s<>{}]+", re.I)),
    (
        "P1",
        "credential-assignment",
        re.compile(
            r"\b(?:[A-Za-z][A-Za-z0-9]*[_-])*"
            r"(?:password|passwd|api[_-]?key|access[_-]?token|secret(?:[_-]?key)?|client[_-]?secret)"
            r"(?:[_-][A-Za-z0-9]+)*['\"]?\s*[:=]\s*['\"]?[^\s'\"<>{}]{8,}",
            re.I,
        ),
    ),
    ("P1", "credential-url", re.compile(r"https?://[^\s/@:]+:[^\s/@]+@", re.I)),
    ("P1", "exact-coordinate-assignment", re.compile(r"\b(?:latitude|longitude|lat|lon)\s*[:=]\s*-?\d{1,3}\.\d{4,}\b", re.I)),
    ("P1", "protected-runtime-path", re.compile(r"/(?:var/(?:lib|backups)|home/[^/]+|etc/(?:haproxy|letsencrypt|ssl))/(?!(?:example|placeholder))", re.I)),
)

PATH_RULES: tuple[tuple[str, str, str], ...] = (
    ("P0", "private-key-file", "*.pem"),
    ("P0", "private-key-file", "*.key"),
    ("P0", "private-key-file", "*.p12"),
    ("P0", "private-key-file", "*.pfx"),
    ("P0", "private-key-file", "*.ppk"),
    ("P0", "private-key-file", "id_rsa"),
    ("P0", "private-key-file", "id_ed25519"),
    ("P1", "environment-file", ".env"),
    ("P1", "environment-file", ".env.*"),
    ("P1", "credential-file", "credentials.json"),
    ("P1", "credential-file", "secrets.json"),
    ("P1", "credential-file", "auth.json"),
    ("P1", "private-evidence", "*evidence*"),
    ("P1", "private-evidence", "*rollback*"),
    ("P1", "browser-profile", "*profile*"),
    ("P1", "opencode-runtime", ".opencode-*"),
)

# An empty, reviewed template is useful in a reproducible clean tree.  It is
# intentionally handled as an exception to the broad ``.env.*`` filename rule;
# a non-empty example is still content-scanned like every other text file.
SAFE_TEMPLATE_NAMES = frozenset({".env.example", ".env.template", ".env.sample"})
SAFE_TEMPLATE_PATHS = frozenset({
    ".env.example",
    "portal_air_v1/config.example.json",
})


def iter_files(root: Path) -> Iterable[Path]:
    for path in sorted(root.rglob("*")):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.is_file():
            yield path


def is_binary(path: Path) -> bool:
    try:
        return b"\0" in path.read_bytes()[:8192]
    except OSError:
        return True


def audit(root: Path, *, allow_safe_templates: bool = False) -> list[dict[str, object]]:
    findings: list[dict[str, object]] = []
    for path in iter_files(root):
        relative = path.relative_to(root).as_posix()
        name = path.name.lower()
        for severity, rule, pattern in PATH_RULES:
            if rule == "environment-file" and name in SAFE_TEMPLATE_NAMES:
                continue
            if fnmatch.fnmatch(name, pattern.lower()) or fnmatch.fnmatch(relative.lower(), pattern.lower()):
                findings.append({"severity": severity, "rule": rule, "path": relative, "line": None})
        try:
            size = path.stat().st_size
        except OSError:
            findings.append({"severity": "P1", "rule": "unreadable-file", "path": relative, "line": None})
            continue
        if size > TEXT_LIMIT_BYTES or is_binary(path):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            findings.append({"severity": "P1", "rule": "non-utf8-text", "path": relative, "line": None})
            continue
        for number, line in enumerate(text.splitlines(), start=1):
            for severity, rule, expression in CONTENT_RULES:
                if (
                    allow_safe_templates
                    and relative in SAFE_TEMPLATE_PATHS
                    and rule == "protected-runtime-path"
                ):
                    continue
                if expression.search(line):
                    findings.append({"severity": severity, "rule": rule, "path": relative, "line": number})
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path, help="candidate publication-tree root")
    parser.add_argument("--json-out", type=Path, help="write the sanitized finding summary as JSON")
    parser.add_argument("--fail-on", choices=("P0", "P1", "none"), default="P1")
    parser.add_argument(
        "--allow-safe-templates",
        action="store_true",
        help=("allow documented non-secret protected runtime paths in the reviewed "
              "template allowlist; this does not disable any credential or coordinate rule"),
    )
    args = parser.parse_args(argv)
    root = args.root.resolve()
    if not root.is_dir():
        parser.error(f"not a directory: {root}")
    findings = audit(root, allow_safe_templates=args.allow_safe_templates)
    summary = Counter(str(item["severity"]) for item in findings)
    payload = {
        "schema_version": 1,
        "root": ".",
        "findings": findings,
        "summary": {"P0": summary["P0"], "P1": summary["P1"]},
    }
    if args.json_out:
        args.json_out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for item in findings:
        line = "" if item["line"] is None else f":{item['line']}"
        print(f"{item['severity']} {item['rule']} {item['path']}{line}")
    print(f"PUBLICATION_AUDIT P0={summary['P0']} P1={summary['P1']} FILES_ROOT={root}")
    if args.fail_on == "P0" and summary["P0"]:
        return 1
    if args.fail_on == "P1" and (summary["P0"] or summary["P1"]):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
