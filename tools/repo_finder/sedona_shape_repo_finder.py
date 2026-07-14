#!/usr/bin/env python3
"""
sedona_shape_repo_finder.py

Find "Apache Sedona-shaped" open-source libraries:
  - real library / SDK / toolkit, not app/template/tutorial
  - active source commits recently
  - enough API surface for multi-function tests
  - evidence of usage: stars/forks + optional PyPI downloads
  - domain/API complexity where LLMs can improve understanding

Requires:
  pip install requests

Recommended:
  export GITHUB_TOKEN=ghp_xxx
  python sedona_shape_repo_finder.py --language Python --top 30 --csv results.csv --json results.json

Examples:
  python sedona_shape_repo_finder.py --language Python --query-extra "optimization"
  python sedona_shape_repo_finder.py --language Python --min-stars 200 --max-stars 5000 --src-months 6
  python sedona_shape_repo_finder.py --language JavaScript --query-extra "parser"
"""

from __future__ import annotations

import argparse
import base64
import csv
import json
import os
import re
import sys
import time
from collections import Counter
from dataclasses import dataclass, asdict
from datetime import datetime, timezone, timedelta
from pathlib import PurePosixPath
from typing import Any, Optional

import requests


GITHUB_API = "https://api.github.com"
PYPI_API = "https://pypi.org/pypi"
PEPY_API = "https://api.pepy.tech/api/v2/projects"

SOURCE_EXTS = {
    ".py", ".js", ".jsx", ".ts", ".tsx",
    ".java", ".scala", ".cpp", ".cc", ".cxx", ".hpp", ".h",
    ".go", ".rs",
}

LANG_EXTS = {
    "Python": {".py"},
    "JavaScript": {".js", ".jsx"},
    "TypeScript": {".ts", ".tsx"},
    "Java": {".java"},
    "Go": {".go"},
    "Rust": {".rs"},
    "Scala": {".scala"},
    "C++": {".cpp", ".cc", ".cxx", ".hpp", ".h"},
}

PUBLIC_API_PATTERNS = {
    ".py": re.compile(r"^\s*(?:async\s+)?def\s+(?!_)\w+\s*\(|^\s*class\s+(?!_)\w+\s*[\(:]", re.M),
    ".js": re.compile(r"^\s*export\s+(?:async\s+)?function\s+\w+\s*\(|^\s*export\s+class\s+\w+|^\s*export\s+const\s+\w+", re.M),
    ".jsx": re.compile(r"^\s*export\s+(?:async\s+)?function\s+\w+\s*\(|^\s*export\s+class\s+\w+|^\s*export\s+const\s+\w+", re.M),
    ".ts": re.compile(r"^\s*export\s+(?:async\s+)?function\s+\w+|^\s*export\s+(?:abstract\s+)?class\s+\w+|^\s*export\s+interface\s+\w+|^\s*export\s+type\s+\w+|^\s*export\s+const\s+\w+", re.M),
    ".tsx": re.compile(r"^\s*export\s+(?:async\s+)?function\s+\w+|^\s*export\s+(?:abstract\s+)?class\s+\w+|^\s*export\s+interface\s+\w+|^\s*export\s+type\s+\w+|^\s*export\s+const\s+\w+", re.M),
    ".java": re.compile(r"^\s*public\s+(?:abstract\s+|final\s+)?(?:class|interface|enum)\s+\w+|^\s*public\s+(?:static\s+)?[\w<>\[\], ?]+\s+\w+\s*\(", re.M),
    ".go": re.compile(r"^func\s+(?:\(\w+\s+\*?\w+\)\s+)?[A-Z]\w*\s*\(|^type\s+[A-Z]\w*\s+(?:struct|interface)", re.M),
    ".rs": re.compile(r"^\s*pub\s+(?:async\s+)?fn\s+\w+\s*[<(]|^\s*pub\s+(?:struct|enum|trait)\s+\w+", re.M),
    ".scala": re.compile(r"^\s*(?:class|trait|object)\s+[A-Z]\w+|^\s*def\s+\w+", re.M),
    ".cpp": re.compile(r"^\s*(?:class|struct)\s+\w+|^[\w:~<>&*\s]+\s+\w+\s*\([^)]*\)\s*(?:const\s*)?[;{]", re.M),
    ".cc": re.compile(r"^\s*(?:class|struct)\s+\w+|^[\w:~<>&*\s]+\s+\w+\s*\([^)]*\)\s*(?:const\s*)?[;{]", re.M),
    ".cxx": re.compile(r"^\s*(?:class|struct)\s+\w+|^[\w:~<>&*\s]+\s+\w+\s*\([^)]*\)\s*(?:const\s*)?[;{]", re.M),
    ".hpp": re.compile(r"^\s*(?:class|struct)\s+\w+|^[\w:~<>&*\s]+\s+\w+\s*\([^)]*\)\s*(?:const\s*)?[;{]", re.M),
    ".h": re.compile(r"^\s*(?:class|struct)\s+\w+|^[\w:~<>&*\s]+\s+\w+\s*\([^)]*\)\s*(?:const\s*)?[;{]", re.M),
}

EXCLUDE_SIGNALS = [
    "awesome", "template", "boilerplate", "starter", "example", "examples",
    "demo", "course", "tutorial", "leetcode", "interview",
    "dotfiles", "dataset", "datasets", "paper-list", "curriculum",
    "scaffold", "sample",
]

APP_SIGNALS = [
    "web app", "dashboard", "cms", "blog", "website", "ui", "server",
    "self-hosted", "clone", "chatbot",
]

LIBRARY_SIGNALS = [
    "library", "sdk", "toolkit", "framework", "client", "parser",
    "engine", "api", "package", "module", "bindings", "connector",
    "driver", "compiler", "serializer", "validator", "optimization",
    "analytics", "processing", "pipeline", "simulation", "modeling",
    "graph", "query", "index", "protocol", "format",
]

DOMAIN_SIGNALS = [
    "spatial", "geospatial", "geometry", "raster", "vector",
    "optimization", "solver", "portfolio", "probabilistic",
    "scientific", "chemistry", "bioinformatics", "genomics",
    "phylogenetic", "spectrometry", "astronomy", "physics",
    "materials", "graph", "knowledge graph", "parser", "protocol",
    "calendar", "email", "url", "finance", "timeseries",
    "dataframe", "distributed", "streaming", "analytics",
]

HARDWARE_SIGNALS = [
    "arduino", "raspberry", "gpio", "firmware", "embedded", "mcu",
    "esp32", "stm32", "sensor", "lidar", "robot", "drone", "fpga",
    "bluetooth", "zigbee", "modbus",
]

TRIVIAL_COMMIT_RE = re.compile(
    r"^(docs?:|ci:|style:|chore:|bump|release|update readme|fix typo|"
    r"update docs|update changelog|update workflow|dependabot)",
    re.I,
)


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def parse_iso(iso: str) -> datetime:
    return datetime.fromisoformat(iso.replace("Z", "+00:00"))


def days_ago(iso: str) -> int:
    return (now_utc() - parse_iso(iso)).days


def clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))


class GitHub:
    def __init__(self, token: str = ""):
        self.token = token or os.getenv("GITHUB_TOKEN", "")
        self.calls = 0
        self.search_delay = 3.5 if self.token else 8.0  # 30/min limit; 3.5s = ~17/min (safe)
        self.core_delay = 0.15 if self.token else 0.8

    def headers(self) -> dict[str, str]:
        h = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "sedona-shape-repo-finder",
        }
        if self.token:
            h["Authorization"] = f"Bearer {self.token}"
        return h

    def get(self, url: str, params: Optional[dict[str, Any]] = None, retries: int = 3) -> Any:
        self.calls += 1
        for attempt in range(retries):
            r = requests.get(url, headers=self.headers(), params=params, timeout=25)
            if r.status_code == 200:
                return r.json()
            if r.status_code in (403, 429):
                wait = int(r.headers.get("Retry-After", 10 + attempt * 10))
                print(f"  rate limited; waiting {wait}s", file=sys.stderr)
                time.sleep(wait)
                continue
            if r.status_code == 404:
                return None
            time.sleep(2 + attempt)
        return None

    def search_repos(self, query: str, per_page: int = 30, page: int = 1) -> dict[str, Any]:
        data = self.get(f"{GITHUB_API}/search/repositories", {
            "q": query,
            "sort": "updated",
            "order": "desc",
            "per_page": per_page,
            "page": page,
        }) or {}
        time.sleep(self.search_delay)
        return data

    def core(self, path_or_url: str, params: Optional[dict[str, Any]] = None) -> Any:
        url = path_or_url if path_or_url.startswith("http") else f"{GITHUB_API}{path_or_url}"
        data = self.get(url, params=params)
        time.sleep(self.core_delay)
        return data


def repo_text(repo: dict[str, Any]) -> str:
    parts = [
        repo.get("full_name", ""),
        repo.get("name", ""),
        repo.get("description") or "",
        " ".join(repo.get("topics") or []),
    ]
    return " ".join(parts).lower()


def looks_excluded(repo: dict[str, Any]) -> tuple[bool, str]:
    text = repo_text(repo)
    for s in EXCLUDE_SIGNALS:
        if s in text:
            return True, f"exclude signal: {s}"
    for h in HARDWARE_SIGNALS:
        if h in text:
            return True, f"hardware signal: {h}"
    return False, ""


def library_likeness(repo: dict[str, Any], paths: list[str]) -> tuple[int, list[str]]:
    text = repo_text(repo)
    score = 0
    reasons = []

    hits = [w for w in LIBRARY_SIGNALS if w in text]
    if hits:
        score += min(30, len(hits) * 8)
        reasons.append("library terms: " + ", ".join(hits[:3]))

    domain_hits = [w for w in DOMAIN_SIGNALS if w in text]
    if domain_hits:
        score += min(30, len(domain_hits) * 8)
        reasons.append("domain terms: " + ", ".join(domain_hits[:3]))

    app_hits = [w for w in APP_SIGNALS if w in text]
    if app_hits:
        score -= min(30, len(app_hits) * 10)
        reasons.append("app-ish terms: " + ", ".join(app_hits[:2]))

    if any(PurePosixPath(p).name in ("pyproject.toml", "setup.py", "setup.cfg", "package.json", "Cargo.toml", "go.mod", "pom.xml", "build.gradle") for p in paths):
        score += 20
        reasons.append("package manifest")

    if any("/tests/" in f"/{p}" or p.startswith("tests/") for p in paths):
        score += 10
        reasons.append("tests present")

    return int(clamp(score, 0, 100)), reasons


def get_tree(gh: GitHub, full_name: str, branch: str) -> list[str]:
    data = gh.core(f"/repos/{full_name}/git/trees/{branch}", {"recursive": "1"})
    if not data or "tree" not in data:
        return []
    return [n["path"] for n in data["tree"] if n.get("type") == "blob"]


def source_paths(paths: list[str], language: str | None = None) -> list[str]:
    allowed = LANG_EXTS.get(language or "", SOURCE_EXTS)
    bad_parts = ("vendor", "node_modules", "dist", "build", ".min.", "migrations", "__pycache__", "third_party", "external")
    out = []
    for p in paths:
        ext = PurePosixPath(p).suffix.lower()
        if ext not in allowed:
            continue
        low = p.lower()
        if any(b in low for b in bad_parts):
            continue
        if re.search(r"(^|/)(test|tests|spec|examples?)/", low):
            continue
        if re.search(r"(test_|_test\.|\.spec\.|\.test\.)", low):
            continue
        out.append(p)
    return out


def main_source_dir(src_paths: list[str]) -> str:
    if not src_paths:
        return "."
    dirs = []
    for p in src_paths:
        parts = p.split("/")
        dirs.append(parts[0] if len(parts) > 1 else ".")
    return Counter(dirs).most_common(1)[0][0]


def recent_source_activity(gh: GitHub, full_name: str, src_paths: list[str], months: int) -> dict[str, Any]:
    src_dir = main_source_dir(src_paths)
    since = (now_utc() - timedelta(days=30 * months)).isoformat()
    params = {"since": since, "per_page": 5}
    if src_dir != ".":
        params["path"] = src_dir
    commits = gh.core(f"/repos/{full_name}/commits", params)

    if not isinstance(commits, list) or not commits:
        return {"active": False, "src_dir": src_dir, "reason": f"no commits to {src_dir}/ in {months} months"}

    for c in commits:
        msg = c["commit"]["message"].splitlines()[0]
        date = c["commit"]["author"]["date"]
        if not TRIVIAL_COMMIT_RE.search(msg):
            return {
                "active": True,
                "src_dir": src_dir,
                "date": date[:10],
                "days": days_ago(date),
                "sha": c["sha"][:7],
                "message": msg[:100],
            }

    # If messages look trivial, fetch one commit detail to verify actual changed source files.
    detail = gh.core(f"/repos/{full_name}/commits/{commits[0]['sha']}")
    changed = []
    if detail:
        for f in detail.get("files", []):
            fn = f.get("filename", "")
            if PurePosixPath(fn).suffix.lower() in SOURCE_EXTS:
                changed.append(fn)
    if changed:
        c = commits[0]
        date = c["commit"]["author"]["date"]
        return {
            "active": True,
            "src_dir": src_dir,
            "date": date[:10],
            "days": days_ago(date),
            "sha": c["sha"][:7],
            "message": c["commit"]["message"].splitlines()[0][:100],
            "changed_source_files": changed[:5],
        }
    return {"active": False, "src_dir": src_dir, "reason": "recent commits looked docs/CI/trivial only"}


def fetch_file_text(gh: GitHub, full_name: str, path: str, max_chars: int = 500_000) -> str:
    data = gh.core(f"/repos/{full_name}/contents/{path}")
    if not data or data.get("encoding") != "base64":
        return ""
    try:
        raw = base64.b64decode(data.get("content", "")).decode("utf-8", "ignore")
        return raw[:max_chars]
    except Exception:
        return ""


def count_public_api(gh: GitHub, full_name: str, src_paths: list[str], max_files: int = 40) -> dict[str, Any]:
    total = 0
    files_counted = 0
    top = []
    for p in src_paths[:max_files]:
        ext = PurePosixPath(p).suffix.lower()
        pat = PUBLIC_API_PATTERNS.get(ext)
        if not pat:
            continue
        text = fetch_file_text(gh, full_name, p)
        if not text:
            continue
        n = len(pat.findall(text))
        files_counted += 1
        if n:
            top.append({"path": p, "count": n})
        total += n
    top.sort(key=lambda x: x["count"], reverse=True)
    return {
        "public_api_count": total,
        "files_counted": files_counted,
        "top_api_files": top[:8],
        "truncated": len(src_paths) > max_files,
    }


def detect_docs_tests(paths: list[str]) -> dict[str, Any]:
    low = [p.lower() for p in paths]
    return {
        "has_tests": any(re.search(r"(^|/)tests?/|_test\.|test_|\.spec\.|\.test\.", p) for p in low),
        "has_examples": any(re.search(r"(^|/)examples?/", p) for p in low),
        "has_docs": any(p.startswith("docs/") or "/docs/" in p or p.endswith("readme.md") for p in low),
        "has_ci": any(".github/workflows/" in p or p in (".travis.yml", "tox.ini") for p in low),
        "has_agents": any(p.endswith("agents.md") or "copilot-instructions" in p for p in low),
        "has_contributing": any("contributing" in p for p in low),
        "has_changelog": any("changelog" in p or "changes.md" in p for p in low),
    }


def pypi_name_guess(repo: dict[str, Any], paths: list[str]) -> Optional[str]:
    # Quick heuristic: repo name is often package name. For exact extraction, parse pyproject.
    if (repo.get("language") or "") != "Python":
        return None
    name = repo.get("name", "")
    if not name:
        return None
    return name.replace("_", "-")


def pypi_downloads(package: str) -> dict[str, Any]:
    # Public endpoint can fail or be rate-limited. Treat as optional.
    out = {"pypi_package": package, "pypi_found": False, "downloads_30d": None}
    try:
        r = requests.get(f"{PEPY_API}/{package}", timeout=15)
        if r.status_code == 200:
            data = r.json()
            out["pypi_found"] = True
            # pepy currently exposes total_downloads. It may not expose 30d without auth.
            out["downloads_total"] = data.get("total_downloads")
            return out
    except Exception:
        pass

    try:
        r = requests.get(f"{PYPI_API}/{package}/json", timeout=15)
        if r.status_code == 200:
            out["pypi_found"] = True
            data = r.json()
            out["pypi_summary"] = (data.get("info") or {}).get("summary")
    except Exception:
        pass
    return out


def issue_confusion_signal(gh: GitHub, full_name: str) -> dict[str, Any]:
    # NOTE: this uses the search API (rate-limited to 30/min with token).
    # Only call this when --issues flag is set. Adds ~3.5s delay per repo.
    q = f'repo:{full_name} ("how do I" OR "documentation" OR "example" OR "usage" OR "confusing")'
    data = gh.get(f"{GITHUB_API}/search/issues", {
        "q": q,
        "sort": "updated",
        "order": "desc",
        "per_page": 1,
    }) or {}
    time.sleep(gh.search_delay * 1.5)  # extra buffer — issues search counts against same limit
    return {"usage_issue_hits": data.get("total_count", 0)}


def score_candidate(
    repo: dict[str, Any],
    paths: list[str],
    src: list[str],
    api_info: dict[str, Any],
    activity: dict[str, Any],
    structure: dict[str, Any],
    lib_score: int,
    pypi: dict[str, Any],
    issue_info: dict[str, Any],
) -> tuple[int, list[str]]:
    stars = repo.get("stargazers_count", 0)
    forks = repo.get("forks_count", 0)
    api_count = api_info.get("public_api_count", 0)
    issue_hits = issue_info.get("usage_issue_hits", 0) or 0

    score = 0
    reasons = []

    adoption = clamp((stars / 2000) * 20, 0, 20) + clamp((forks / 300) * 15, 0, 15)
    score += adoption
    reasons.append(f"adoption {adoption:.1f}")

    if pypi.get("pypi_found"):
        score += 8
        reasons.append("package registry found")
    if pypi.get("downloads_total"):
        dl = pypi["downloads_total"]
        extra = clamp((dl / 1_000_000) * 10, 0, 10)
        score += extra
        reasons.append(f"downloads bonus {extra:.1f}")

    score += clamp(api_count / 80 * 20, 0, 20)
    reasons.append(f"API surface {api_count}")

    if activity.get("active"):
        days = activity.get("days", 999)
        activity_score = 15 if days <= 30 else 10 if days <= 90 else 6
        score += activity_score
        reasons.append(f"source active {days}d")

    score += lib_score * 0.15
    reasons.append(f"library score {lib_score}")

    if structure["has_tests"]:
        score += 8
        reasons.append("tests")
    if structure["has_examples"]:
        score += 4
        reasons.append("examples")
    if structure["has_docs"]:
        score += 4
        reasons.append("docs")

    # Good LLM target: some usage confusion but not only support burden.
    score += clamp(issue_hits / 50 * 8, 0, 8)
    if issue_hits:
        reasons.append(f"usage/doc issue hits {issue_hits}")

    # Penalty if too massive/popular for easy experimentation.
    if stars > 5000:
        score -= 8
        reasons.append("too popular penalty")
    if len(paths) > 5000:
        score -= 5
        reasons.append("very large repo penalty")
    if not structure["has_tests"]:
        score -= 8
        reasons.append("no tests penalty")
    if api_count < 30:
        score -= 15
        reasons.append("small API penalty")

    return int(clamp(score, 0, 100)), reasons


@dataclass
class Candidate:
    repo: str
    url: str
    description: str
    language: str
    stars: int
    forks: int
    pushed_at: str
    source_files: int
    public_api_count: int
    enough_for_5_combo_tests: bool
    source_active: bool
    last_source_commit_date: str
    library_score: int
    final_score: int
    has_tests: bool
    has_examples: bool
    has_docs: bool
    has_agents: bool
    usage_issue_hits: int
    pypi_found: bool
    llm_gaps: str
    reasons: str


def analyze_repo(
    gh: GitHub,
    repo: dict[str, Any],
    src_months: int,
    min_api: int,
    count_api: bool,
    check_issues: bool,
    check_pypi: bool,
) -> Optional[Candidate]:
    full_name = repo["full_name"]

    excluded, reason = looks_excluded(repo)
    if excluded:
        print(f"  skip {full_name}: {reason}")
        return None

    meta = gh.core(f"/repos/{full_name}") or repo
    repo.update(meta)

    branch = repo.get("default_branch") or "main"
    paths = get_tree(gh, full_name, branch)
    if not paths:
        print(f"  skip {full_name}: no tree")
        return None

    src = source_paths(paths, repo.get("language"))
    if len(src) < 8:
        print(f"  skip {full_name}: too few source files ({len(src)})")
        return None

    lib_score, lib_reasons = library_likeness(repo, paths)
    if lib_score < 35:
        print(f"  skip {full_name}: low library score ({lib_score})")
        return None

    activity = recent_source_activity(gh, full_name, src, src_months)
    if not activity.get("active"):
        print(f"  skip {full_name}: {activity.get('reason')}")
        return None

    structure = detect_docs_tests(paths)

    api_info = {"public_api_count": None, "top_api_files": []}
    if count_api:
        api_info = count_public_api(gh, full_name, src)
        if api_info["public_api_count"] < min_api:
            print(f"  skip {full_name}: API too small ({api_info['public_api_count']})")
            return None

    pypi = {"pypi_found": False}
    if check_pypi:
        guess = pypi_name_guess(repo, paths)
        if guess:
            pypi = pypi_downloads(guess)

    issue_info = {"usage_issue_hits": 0}
    if check_issues:
        issue_info = issue_confusion_signal(gh, full_name)

    final_score, score_reasons = score_candidate(
        repo, paths, src, api_info, activity, structure, lib_score, pypi, issue_info
    )

    gaps = []
    if not structure["has_agents"]:
        gaps.append("no AGENTS.md")
    if not structure["has_examples"]:
        gaps.append("few/no examples")
    if not structure["has_contributing"]:
        gaps.append("no CONTRIBUTING detected")
    if not structure["has_changelog"]:
        gaps.append("no CHANGELOG detected")
    if issue_info.get("usage_issue_hits", 0) > 20:
        gaps.append("many usage/docs issues")
    if api_info.get("public_api_count", 0) >= 50:
        gaps.append("large composable API surface")

    enough_5 = bool((api_info.get("public_api_count") or 0) >= min_api and structure["has_tests"])

    return Candidate(
        repo=full_name,
        url=repo.get("html_url", f"https://github.com/{full_name}"),
        description=(repo.get("description") or "").replace("\n", " ")[:220],
        language=repo.get("language") or "",
        stars=repo.get("stargazers_count", 0),
        forks=repo.get("forks_count", 0),
        pushed_at=repo.get("pushed_at", ""),
        source_files=len(src),
        public_api_count=api_info.get("public_api_count") or 0,
        enough_for_5_combo_tests=enough_5,
        source_active=bool(activity.get("active")),
        last_source_commit_date=activity.get("date", ""),
        library_score=lib_score,
        final_score=final_score,
        has_tests=structure["has_tests"],
        has_examples=structure["has_examples"],
        has_docs=structure["has_docs"],
        has_agents=structure["has_agents"],
        usage_issue_hits=issue_info.get("usage_issue_hits", 0) or 0,
        pypi_found=bool(pypi.get("pypi_found")),
        llm_gaps=", ".join(gaps),
        reasons=" | ".join(lib_reasons + score_reasons),
    )


TARGET_LANGUAGES = [
    "Python", "JavaScript", "TypeScript", "Java", "C++", "Go", "Rust", "Scala"
]


def build_queries(args: argparse.Namespace) -> list[str]:
    base_filters = [
        f"stars:{args.min_stars}..{args.max_stars}",
        f"forks:>{args.min_forks}",
        f"pushed:>{args.pushed_after}",
        "archived:false",
    ]

    # Use focused search terms because broad GitHub search is noisy.
    extras = [args.query_extra] if args.query_extra else [
        "library",
        "sdk",
        "parser",
        "optimization",
        "data processing",
        "graph",
        "protocol",
        "analytics",
        "scientific",
    ]

    queries = []
    if args.language:
        # Single language — one query per extra term
        for e in extras:
            queries.append(" ".join(base_filters + [f"language:{args.language}", e]))
    else:
        # All languages — GitHub doesn't support language:A OR language:B,
        # so we emit one query per language per extra term.
        # To avoid exploding the call count, only use the first 3 extras.
        for lang in TARGET_LANGUAGES:
            for e in extras[:3]:
                queries.append(" ".join(base_filters + [f"language:{lang}", e]))

    return queries


def write_csv(path: str, rows: list[Candidate]) -> None:
    if not rows:
        return
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(asdict(rows[0]).keys()))
        w.writeheader()
        for r in rows:
            w.writerow(asdict(r))


def write_json(path: str, rows: list[Candidate]) -> None:
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump([asdict(r) for r in rows], f, indent=2)


def main() -> int:
    ap = argparse.ArgumentParser(description="Find Sedona-shaped GitHub libraries for LLM-readiness experiments.")
    ap.add_argument("--token", default=os.getenv("GITHUB_TOKEN", ""))
    ap.add_argument("--language", default="Python", help=f"One of: {', '.join(TARGET_LANGUAGES)} — or empty/all for all languages (slower, more API calls)")
    ap.add_argument("--query-extra", default="", help="Extra GitHub search term, e.g. optimization, parser, graph")
    ap.add_argument("--min-stars", type=int, default=200)
    ap.add_argument("--max-stars", type=int, default=5000)
    ap.add_argument("--min-forks", type=int, default=20)
    ap.add_argument("--pushed-after", default="2025-01-01")
    ap.add_argument("--src-months", type=int, default=6)
    ap.add_argument("--top", type=int, default=25)
    ap.add_argument("--pages", type=int, default=2)
    ap.add_argument("--per-page", type=int, default=20)
    ap.add_argument("--min-api", type=int, default=30, help="Minimum estimated public functions/classes for 5-combo testing")
    ap.add_argument("--no-api-count", action="store_true", help="Skip source file downloads/API counting")
    ap.add_argument("--issues", action="store_true", help="Search issues for usage/docs confusion signals")
    ap.add_argument("--pypi", action="store_true", help="Check PyPI/pepy for Python package usage signal")
    ap.add_argument("--csv", default="")
    ap.add_argument("--json", default="")
    ap.add_argument("--exclude-regex", default="",
                    help="drop repos whose name/description/topics match this regex "
                         "(case-insensitive), e.g. 'geo|spatial|gis|raster|map' to find "
                         "candidates OUTSIDE the geospatial domain GRAIL already covers")
    args = ap.parse_args()

    if args.language.lower() in ("", "all", "none"):
        args.language = ""

    gh = GitHub(args.token)
    print(f"Token: {'set' if gh.token else 'not set'}")
    print(f"Language: {args.language or 'all'}")
    print(f"Filters: stars {args.min_stars}-{args.max_stars}, forks>{args.min_forks}, pushed>{args.pushed_after}")
    print(f"API count: {'off' if args.no_api_count else 'on'}; issues: {args.issues}; pypi: {args.pypi}")

    queries = build_queries(args)
    print(f"Queries: {len(queries)} search queries × {args.pages} pages = up to {len(queries) * args.pages * args.per_page} repos to analyze")
    print(f"Tip: use --query-extra 'library' to run just 1 query instead of {len(queries)}")
    print()

    seen = set()
    candidates: list[Candidate] = []

    for q in queries:
        print(f"\nSEARCH: {q}")
        for page in range(1, args.pages + 1):
            data = gh.search_repos(q, per_page=args.per_page, page=page)
            items = data.get("items") or []
            print(f"  page {page}: {len(items)} items / total {data.get('total_count', '?')}")
            for repo in items:
                if repo["full_name"] in seen:
                    continue
                seen.add(repo["full_name"])
                if args.exclude_regex:
                    hay = " ".join([repo.get("full_name") or "",
                                    repo.get("description") or "",
                                    " ".join(repo.get("topics") or [])])
                    if re.search(args.exclude_regex, hay, re.I):
                        print(f" skip (excluded domain) {repo['full_name']}")
                        continue
                print(f" analyze {repo['full_name']}")
                try:
                    c = analyze_repo(
                        gh,
                        repo,
                        src_months=args.src_months,
                        min_api=args.min_api,
                        count_api=not args.no_api_count,
                        check_issues=args.issues,
                        check_pypi=args.pypi,
                    )
                    if c:
                        candidates.append(c)
                except KeyboardInterrupt:
                    raise
                except Exception as e:
                    print(f"  error {repo['full_name']}: {e}", file=sys.stderr)

    candidates.sort(key=lambda c: c.final_score, reverse=True)
    candidates = candidates[:args.top]

    print("\n" + "=" * 100)
    print(f"RESULTS: {len(candidates)} candidates, GitHub calls: {gh.calls}")
    print("=" * 100)

    for i, c in enumerate(candidates, 1):
        print(f"\n#{i:02d} {c.repo} [{c.language}] score={c.final_score}")
        print(f"    {c.url}")
        print(f"    ⭐ {c.stars:,}  🍴 {c.forks:,}  src={c.source_files}  api≈{c.public_api_count}")
        print(f"    active source: {c.source_active} last={c.last_source_commit_date}")
        print(f"    5-combo testable: {c.enough_for_5_combo_tests} | tests={c.has_tests} examples={c.has_examples} docs={c.has_docs}")
        print(f"    LLM gaps: {c.llm_gaps}")
        print(f"    {c.description}")

    if args.csv:
        write_csv(args.csv, candidates)
        print(f"\nCSV written: {args.csv}")
    if args.json:
        write_json(args.json, candidates)
        print(f"JSON written: {args.json}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
