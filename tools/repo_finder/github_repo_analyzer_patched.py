"""
GitHub Repo Analyzer — Sedona-Profile Edition
==============================================
Finds domain libraries that match the Apache Sedona shape:
  - 200–2000 stars, high fork ratio
  - Non-trivial API surface (real codebase, not data/config)
  - Domain library used as a dependency
  - Genuinely active: source code commits in the last 3 months
    (not just .gitignore / README / CI tweaks)
  - Testable without hardware

The "active source" check works by:
  1. Finding the main source directory from the file tree (e.g. src/, lib/, mylib/)
  2. Querying commits with ?path=<src_dir>&since=<3_months_ago>&per_page=3
  3. Checking those commits changed actual source files (not just config/docs)
  This costs exactly 1–2 extra API calls per repo.

Languages: Python, JavaScript, TypeScript, Go, Rust, Java, Scala, C++
SQL excluded — GitHub SQL repos are migration files, not libraries.

Rate limits:
  No token  →  60 req/min core, 10 req/min search
  With token → 5000 req/min core, 30 req/min search
  Get a free token: github.com/settings/tokens (no scopes needed)

Usage:
  python github_repo_analyzer.py --token ghp_xxxx
  python github_repo_analyzer.py --token ghp_xxxx --funcs
  python github_repo_analyzer.py --token ghp_xxxx --language rust
  python github_repo_analyzer.py --token ghp_xxxx --testable-only
  python github_repo_analyzer.py --token ghp_xxxx --src-months 6
"""

import os, re, time, base64, argparse
from collections import Counter
from datetime import datetime, timezone, timedelta
from typing import Optional
import requests

BASE = "https://api.github.com"

TARGET_LANGUAGES = [
    "Python",       # #1 fastest growing — SO 2025
    "JavaScript",   # #1 most used (66%) — SO 2025
    "TypeScript",   # #1 on GitHub by PRs — Octoverse 2025
    "Java",         # enterprise backbone — TIOBE top 3
    "C++",          # systems / performance — TIOBE top 5
    "Go",           # cloud-native, microservices — SO desired
    "Rust",         # most loved 2 years running — SO 2025
    "Scala",        # data engineering (Spark)
]

SEARCH_BUCKETS = [
    "Python OR JavaScript OR TypeScript",
    "Java OR Go OR Rust",
    "Scala OR C++",
]

# ── Sedona-profile filters ────────────────────────────────────────────────────

DATA_REPO_SIGNALS = [
    "staged-recipes", "awesome-", "boilerplate", "template", "example",
    "hello-world", "starter", "cookiecutter", "scaffold", "demo",
    "cheatsheet", "curriculum", "exercises", "practice", "course",
    "tutorial", "learning", "interview", "leetcode", "algorithm-",
    "todo-", "sample-", "-example", "-examples", "dotfiles",
]

OVEREXPOSED_REPOS = {
    "django", "fastapi", "flask", "react", "vue", "angular", "nextjs",
    "express", "spring", "hibernate", "rails", "laravel", "symfony",
    "numpy", "pandas", "scikit-learn", "tensorflow", "pytorch", "keras",
    "tokio", "axum", "actix", "gin", "echo", "fiber",
}

DOMAIN_LIBRARY_SIGNALS = [
    "library", "sdk", "engine", "toolkit", "client",
    "processing", "analysis", "analytics", "pipeline", "computation",
    "distributed", "parallel", "streaming", "indexing", "query",
    "parser", "serializer", "protocol", "codec", "format",
    "inference", "optimization", "simulation", "modelling", "modeling",
    "genomics", "bioinformatics", "chemistry", "physics", "astronomy",
    "financial", "trading", "signal", "image", "graph", "network",
    "spatial", "temporal", "metrics", "statistics", "probabilistic",
]

# Commit message patterns that almost certainly mean no source was changed
TRIVIAL_COMMIT_RE = re.compile(
    r"^(bump version|update (readme|docs?|changelog|ci|workflow|"
    r"\.gitignore|dependabot|github actions|lock|lockfile|"
    r"dependencies|dependency|deps)|"
    r"(fix|add|remove|update) (typo|comment|whitespace|formatting|"
    r"lint|badge|copyright|license)|"
    r"chore:|docs:|ci:|style:|release v?\d)",
    re.IGNORECASE,
)

# Source file extensions that count as "real code"
SOURCE_EXTS = {
    ".py", ".js", ".jsx", ".ts", ".tsx",
    ".java", ".scala", ".cpp", ".cc", ".cxx", ".hpp", ".h",
    ".go", ".rs",
}

FUNC_PATTERNS = {
    ".py":   re.compile(r"^\s*(?:async\s+)?def\s+\w+\s*\(", re.M),
    ".js":   re.compile(r"(?:function\s+\w+\s*\(|(?:const|let|var)\s+\w+\s*=\s*(?:async\s*)?\(.*?\)\s*=>)", re.M),
    ".jsx":  re.compile(r"(?:function\s+\w+\s*\(|(?:const|let|var)\s+\w+\s*=\s*(?:async\s*)?\(.*?\)\s*=>)", re.M),
    ".ts":   re.compile(r"(?:function\s+\w+\s*[\(<]|(?:const|let|var)\s+\w+\s*=\s*(?:async\s*)?\(.*?\)\s*=>)", re.M),
    ".tsx":  re.compile(r"(?:function\s+\w+\s*[\(<]|(?:const|let|var)\s+\w+\s*=\s*(?:async\s*)?\(.*?\)\s*=>)", re.M),
    ".java": re.compile(r"(?:public|private|protected|static|\s)+[\w<>\[\]]+\s+\w+\s*\([^)]*\)\s*\{", re.M),
    ".cpp":  re.compile(r"[\w:~]+\s+[\w:~]+\s*\([^)]*\)\s*(?:const\s*)?\s*\{", re.M),
    ".cc":   re.compile(r"[\w:~]+\s+[\w:~]+\s*\([^)]*\)\s*(?:const\s*)?\s*\{", re.M),
    ".go":   re.compile(r"^func\s+(?:\(\w+\s+\*?\w+\)\s+)?\w+\s*\(", re.M),
    ".rs":   re.compile(r"^\s*(?:pub\s+)?(?:async\s+)?fn\s+\w+\s*[<(]", re.M),
    ".scala":re.compile(r"^\s*(?:def\s+\w+|override\s+def\s+\w+)", re.M),
}

HW_KEYWORDS = [
    "raspberry","arduino","gpio","i2c","spi","uart","firmware",
    "microcontroller","mcu","esp32","esp8266","stm32","embedded","rpi",
    "sensor","lidar","servo","stepper","motor","hardware","driver",
    "robot","drone","bluetooth","zigbee","modbus","plc","fpga",
]
HW_IMPORT_RE = re.compile(
    r"\bimport\s+(RPi|gpiozero|serial|smbus2?|cv2|pigpio|board|"
    r"busio|digitalio|wiringpi|pyserial|usb|hid)\b"
    r"|\bfrom\s+(RPi|gpiozero|serial|smbus|cv2|pigpio|board|"
    r"busio|digitalio|adafruit_)",
    re.IGNORECASE,
)
PURE_KEYWORDS = [
    "utility","algorithm","parser","formatter","validator","serializer",
    "converter","calculator","math","string","text","json","yaml","toml",
    "csv","cache","queue","scheduler","logger","config","cli","toolkit",
]


# ── HTTP client ───────────────────────────────────────────────────────────────

class GitHubClient:
    def __init__(self, token: str):
        self.token   = token
        self.delay   = 0.12 if token else 0.8
        self.s_delay = 2.5  if token else 7.0
        self._calls  = 0

    def _headers(self):
        h = {"Accept": "application/vnd.github+json"}
        if self.token:
            h["Authorization"] = f"Bearer {self.token}"
        return h

    def get(self, url, params=None, retries=3) -> Optional[dict]:
        self._calls += 1
        for attempt in range(retries):
            try:
                r = requests.get(url, headers=self._headers(),
                                 params=params, timeout=15)
            except Exception:
                time.sleep(5); continue
            if r.status_code == 200:
                return r.json()
            if r.status_code in (403, 429):
                remaining = r.headers.get("X-RateLimit-Remaining", "?")
                wait = int(r.headers.get("Retry-After", 15 * (attempt + 1)))
                print(f"  ⏳ Rate limited (remaining={remaining}) — waiting {wait}s ...")
                time.sleep(wait)
            elif r.status_code == 404:
                return None
            else:
                time.sleep(3)
        return None

    def search(self, params) -> Optional[dict]:
        data = self.get(f"{BASE}/search/repositories", params=params)
        time.sleep(self.s_delay)
        return data

    def core(self, url, params=None) -> Optional[dict]:
        data = self.get(url, params=params)
        time.sleep(self.delay)
        return data

    @property
    def call_count(self): return self._calls


# ── Helpers ───────────────────────────────────────────────────────────────────

def days_ago(iso: str) -> int:
    dt = datetime.fromisoformat(iso.rstrip("Z")).replace(tzinfo=timezone.utc)
    return (datetime.now(timezone.utc) - dt).days

def since_iso(months: int) -> str:
    dt = datetime.now(timezone.utc) - timedelta(days=30 * months)
    return dt.isoformat()

def freshness(d: int) -> str:
    if d <  30: return "🟢 fresh"
    if d <  90: return "🟡 recent"
    if d < 365: return "🟠 aging"
    return              "🔴 stale"


# ── Source activity check ─────────────────────────────────────────────────────

def main_source_dir(source_paths: list) -> str:
    """
    Finds the top-level directory that contains most source files.
    Returns '.' if most source files are in the root.

    Examples:
      ['src/foo.py', 'src/bar.py', 'src/utils.py'] → 'src'
      ['mylib/a.go', 'mylib/b.go', 'cmd/main.go']  → 'mylib'
      ['main.py', 'utils.py', 'cli.py']             → '.'
    """
    top_dirs = []
    for p in source_paths:
        parts = p.split("/")
        top_dirs.append(parts[0] if len(parts) > 1 else ".")
    if not top_dirs:
        return "."
    return Counter(top_dirs).most_common(1)[0][0]


def check_source_activity(gh: GitHubClient, name: str,
                           source_paths: list, months: int = 3) -> dict:
    """
    Checks whether source code (not just config/docs) was committed
    in the last `months` months. Uses 1–2 API calls.

    Strategy:
      1. Find the main source directory from the tree we already have.
      2. Query commits with ?path=<dir>&since=<N months ago>&per_page=3
      3. For each returned commit, verify it's non-trivial:
         - message doesn't match TRIVIAL_COMMIT_RE
         - OR fetch commit detail and confirm source files were changed
      If any non-trivial commit found → active. Otherwise → stale source.
    """
    src_dir = main_source_dir(source_paths)
    cutoff  = since_iso(months)

    params = {"per_page": 3, "since": cutoff}
    if src_dir != ".":
        params["path"] = src_dir

    commits = gh.core(f"{BASE}/repos/{name}/commits", params=params)

    if not commits or not isinstance(commits, list) or len(commits) == 0:
        return {
            "active": False,
            "reason": f"no commits to '{src_dir}/' in last {months} months",
            "src_dir": src_dir,
            "last_src_date": None,
            "last_src_days": None,
        }

    # Check commit messages first (cheap)
    for c in commits:
        msg = c["commit"]["message"].split("\n")[0]
        if not TRIVIAL_COMMIT_RE.match(msg):
            date_str = c["commit"]["author"]["date"]
            return {
                "active": True,
                "src_dir": src_dir,
                "last_src_date": date_str[:10],
                "last_src_days": days_ago(date_str),
                "last_src_msg": msg[:65],
                "last_src_sha": c["sha"][:7],
            }

    # All messages look trivial — fetch the most recent commit's file list
    # to confirm (1 extra call)
    sha = commits[0]["sha"]
    detail = gh.core(f"{BASE}/repos/{name}/commits/{sha}")

    if detail:
        changed_files = [f["filename"] for f in detail.get("files", [])]
        src_changed = [
            f for f in changed_files
            if os.path.splitext(f)[1].lower() in SOURCE_EXTS
        ]
        if src_changed:
            date_str = commits[0]["commit"]["author"]["date"]
            return {
                "active": True,
                "src_dir": src_dir,
                "last_src_date": date_str[:10],
                "last_src_days": days_ago(date_str),
                "last_src_msg": commits[0]["commit"]["message"].split("\n")[0][:65],
                "last_src_sha": sha[:7],
                "src_files_changed": src_changed[:3],
            }

    return {
        "active": False,
        "reason": f"recent commits to '{src_dir}/' only touched config/docs",
        "src_dir": src_dir,
        "last_src_date": None,
        "last_src_days": None,
    }


# ── Sedona-profile check ──────────────────────────────────────────────────────

def sedona_profile_check(repo: dict, source_file_count: int,
                          source_ratio: float) -> dict:
    name   = repo.get("full_name", "").lower()
    desc   = (repo.get("description") or "").lower()
    topics = [t.lower() for t in (repo.get("topics") or [])]
    text   = f"{name} {desc} {' '.join(topics)}"
    flags, reasons = [], []

    for signal in DATA_REPO_SIGNALS:
        if signal in text:
            flags.append(f"data/template signal: '{signal}'")
            break  # one is enough

    repo_base = name.split("/")[-1].replace("-","").replace("_","")
    for known in OVEREXPOSED_REPOS:
        if known in repo_base:
            flags.append(f"overexposed: '{known}'")
            break

    if source_file_count < 5:
        flags.append(f"too few source files ({source_file_count})")

    if source_ratio < 0.15:
        flags.append(f"only {source_ratio:.0%} of repo is source code")

    if len((repo.get("description") or "").strip()) < 15:
        flags.append("description too short")

    domain_hits = [w for w in DOMAIN_LIBRARY_SIGNALS if w in text]
    if domain_hits:
        reasons.append(f"domain signals: {', '.join(domain_hits[:3])}")
    if repo.get("_fork_ratio", 0) > 0.08:
        reasons.append(f"fork ratio {repo['_fork_ratio']:.2f}")
    if source_file_count >= 10:
        reasons.append(f"{source_file_count} source files")

    return {"passes": len(flags) == 0, "reasons": reasons, "flags": flags}


# ── Testability ───────────────────────────────────────────────────────────────

def testability_score(repo: dict, sample: str = "") -> dict:
    score, good, bad = 60, [], []
    text = " ".join([
        repo.get("description") or "",
        repo.get("full_name", ""),
        " ".join(repo.get("topics") or []),
    ]).lower()

    hw = [w for w in HW_KEYWORDS if w in text]
    if hw:
        score -= 15 * min(len(hw), 3)
        bad.append(f"hardware keywords: {', '.join(hw[:3])}")
    if sample and HW_IMPORT_RE.search(sample):
        score -= 40; bad.append("hardware imports in source")

    if repo.get("_has_tests"):
        score += 25; good.append("has test files")
    else:
        score -= 10; bad.append("no test files found")

    logic = [w for w in PURE_KEYWORDS if w in text]
    if logic:
        score += min(len(logic) * 10, 30)
        good.append(f"pure-logic: {', '.join(logic[:2])}")

    if repo.get("_has_ci"):
        score += 10; good.append("CI present")
    if repo.get("size", 99999) < 500:
        score += 10; good.append("small codebase")

    score = max(0, min(100, score))
    verdict = (
        "✅ Very testable"           if score >= 75 else
        "🟡 Mostly testable"         if score >= 55 else
        "🟠 Tricky (external deps)"  if score >= 35 else
        "🔴 Hardware/infra dependent"
    )
    return {"score": score, "verdict": verdict, "good": good, "bad": bad}


# ── File tree ─────────────────────────────────────────────────────────────────

def check_tree(gh: GitHubClient, name: str, branch: str) -> dict:
    data = gh.core(f"{BASE}/repos/{name}/git/trees/{branch}",
                   params={"recursive": "1"})
    if not data or "tree" not in data:
        if branch == "main":
            return check_tree(gh, name, "master")
        return {"has_tests": False, "has_ci": False,
                "test_files": [], "source_paths": [],
                "source_ratio": 0.0, "total_files": 0}

    paths = [n["path"] for n in data["tree"] if n["type"] == "blob"]

    test_files = [p for p in paths
                  if re.search(r"(^|/)tests?/|test_\w+\.\w+$|_test\.\w+$|\.spec\.\w+$", p, re.I)]
    has_ci     = any(".github/workflows" in p or ".travis" in p
                     or "tox.ini" == p or "Jenkinsfile" in p for p in paths)
    source_paths = [
        p for p in paths
        if os.path.splitext(p)[1].lower() in SOURCE_EXTS
        and not any(s in p for s in
                    ["test","vendor","migrations","__pycache__",
                     "node_modules",".min.","spec","third_party","extern"])
        and not p.startswith(".")
    ]
    total = max(len(paths), 1)
    return {
        "has_tests":    bool(test_files),
        "has_ci":       has_ci,
        "test_files":   test_files[:5],
        "source_paths": source_paths,
        "source_ratio": len(source_paths) / total,
        "total_files":  total,
    }


def sample_source(gh: GitHubClient, name: str, paths: list, n: int = 5) -> str:
    chunks = []
    for p in paths[:n]:
        d = gh.core(f"{BASE}/repos/{name}/contents/{p}")
        if d and d.get("encoding") == "base64":
            try:
                chunks.append(base64.b64decode(d["content"]).decode("utf-8","ignore"))
            except Exception:
                pass
    return "\n".join(chunks)


# ── Function counting ─────────────────────────────────────────────────────────

def count_funcs(gh: GitHubClient, name: str,
                source_paths: list, max_files: int = 15) -> dict:
    eligible = [
        p for p in source_paths
        if os.path.splitext(p)[1].lower() in FUNC_PATTERNS
        and not any(s in p for s in ["test","vendor","node_modules",".min.","spec"])
    ][:max_files]

    total, rows = 0, []
    for path in eligible:
        ext = os.path.splitext(path)[1].lower()
        pat = FUNC_PATTERNS.get(ext)
        if not pat: continue
        d = gh.core(f"{BASE}/repos/{name}/contents/{path}")
        if not d or d.get("encoding") != "base64": continue
        try:
            code = base64.b64decode(d["content"]).decode("utf-8","ignore")
        except Exception:
            continue
        n = len(pat.findall(code))
        if n: rows.append({"path": path, "count": n})
        total += n

    rows.sort(key=lambda x: x["count"], reverse=True)
    return {"total": total, "files": len(eligible),
            "top": rows[:5], "truncated": len(source_paths) > max_files}


# ── Last commit (any file) ────────────────────────────────────────────────────

def last_commit(gh: GitHubClient, name: str) -> dict:
    data = gh.core(f"{BASE}/repos/{name}/commits", params={"per_page": 1})
    if not data or not isinstance(data, list) or not data:
        return {}
    c = data[0]; ds = c["commit"]["author"]["date"]
    return {"sha": c["sha"][:7],
            "msg": c["commit"]["message"].split("\n")[0][:72],
            "date": ds[:10], "days": days_ago(ds)}


def llm_gaps(repo: dict, tree: dict) -> list:
    gaps = []
    if len((repo.get("description") or "").strip()) < 20:
        gaps.append("no/short description")
    if not repo.get("license"):  gaps.append("no license")
    if not repo.get("homepage"): gaps.append("no docs site")
    if repo.get("open_issues_count", 0) > 100:
        gaps.append(f"{repo['open_issues_count']} open issues")
    all_paths = [p.lower() for p in tree.get("source_paths", [])]
    if not any("agents.md" in p or "copilot-instructions" in p for p in all_paths):
        gaps.append("no AGENTS.md")
    if not any("contributing" in p for p in all_paths):
        gaps.append("no CONTRIBUTING.md")
    if not any("changelog" in p for p in all_paths):
        gaps.append("no CHANGELOG")
    return gaps


# ── Search ────────────────────────────────────────────────────────────────────

def search_repos(gh: GitHubClient, language: Optional[str],
                 min_stars: int, max_stars: int, min_forks: int,
                 pushed_after: str, per_page: int) -> list:
    if language:
        return _query(gh, language, min_stars, max_stars,
                      min_forks, pushed_after, per_page)

    seen, all_repos = set(), []
    for bucket in SEARCH_BUCKETS:
        batch = _query(gh, bucket, min_stars, max_stars,
                       min_forks, pushed_after, per_page=min(per_page, 20))
        for r in batch:
            if r["id"] not in seen:
                seen.add(r["id"]); all_repos.append(r)
        time.sleep(gh.s_delay)

    all_repos = [r for r in all_repos
                 if (r.get("language") or "") in TARGET_LANGUAGES]
    for r in all_repos:
        r["_fork_ratio"] = r["forks_count"] / max(r["stargazers_count"], 1)
    all_repos.sort(key=lambda r: r["_fork_ratio"], reverse=True)
    print(f"  ✅ {len(all_repos)} raw candidates across "
          f"{len(set(r.get('language') for r in all_repos))} languages")
    return all_repos


def _query(gh, lang_clause, min_stars, max_stars,
           min_forks, pushed_after, per_page) -> list:
    if " OR " in lang_clause:
        langs = lang_clause.split(" OR ")
        lang_filter = " OR ".join(f"language:{l}" for l in langs)
        q = (f"stars:{min_stars}..{max_stars} forks:>{min_forks} "
             f"pushed:>{pushed_after} ({lang_filter})")
    else:
        q = (f"stars:{min_stars}..{max_stars} forks:>{min_forks} "
             f"pushed:>{pushed_after} language:{lang_clause}")
    print(f"  🔍 [{lang_clause}]")
    data = gh.search({"q": q, "sort": "updated",
                      "order": "desc", "per_page": per_page})
    if not data: print("    ⚠️  no response"); return []
    if "message" in data: print(f"    ⚠️  {data['message']}"); return []
    items = data.get("items", [])
    print(f"    → {data.get('total_count', 0):,} total, got {len(items)}")
    for r in items:
        r["_fork_ratio"] = r["forks_count"] / max(r["stargazers_count"], 1)
    return items


# ── Main ──────────────────────────────────────────────────────────────────────

def analyze(token="", language=None, min_stars=200, max_stars=2000,
            min_forks=20, pushed_after="2024-06-01", top=10,
            do_funcs=False, max_files=15, testable_only=False,
            src_months=3):

    if not token:
        token = os.getenv("GITHUB_TOKEN", "")

    gh = GitHubClient(token)

    print(f"\n{'═'*72}")
    print(f"  GitHub Repo Analyzer — Sedona-profile edition")
    print(f"  Token     : {'✅ set' if token else '❌ not set (rate limits will be tight)'}")
    print(f"  Language  : {language or ', '.join(TARGET_LANGUAGES)}")
    print(f"  Filters   : ⭐{min_stars}–{max_stars}  forks>{min_forks}  pushed>{pushed_after}")
    print(f"  Src check : real source commits in last {src_months} months")
    print(f"              (ignores .gitignore / README / CI-only pushes)")
    if not token:
        est = top * (25 if do_funcs else 10)
        print(f"  ⚠️  No token: ~{est} API calls, limit 60/min → will be slow")
        print(f"     Free token: github.com/settings/tokens (no scopes)")
    print(f"{'═'*72}")

    candidates = search_repos(gh, language, min_stars, max_stars,
                               min_forks, pushed_after, per_page=top * 3)
    if not candidates:
        print("\nNo candidates found — try relaxing the filters.")
        return []

    results, skipped = [], 0
    skip_reasons = Counter()
    print(f"\n📦 Analyzing repos ...\n")

    for i, repo in enumerate(candidates, 1):
        if len(results) >= top:
            break
        name = repo["full_name"]
        lang = repo.get("language") or "unknown"
        print(f"  [{i:02d}] {name}  [{lang}]  (API calls: {gh.call_count})")

        # Full metadata
        meta   = gh.core(f"{BASE}/repos/{name}") or {}
        branch = meta.get("default_branch", "main")
        for k in ["size","open_issues_count","license","homepage",
                  "description","topics","language"]:
            repo[k] = meta.get(k, repo.get(k))
        repo["_fork_ratio"] = repo["forks_count"] / max(repo["stargazers_count"], 1)
        lang = repo.get("language") or "unknown"

        if not language and lang not in TARGET_LANGUAGES:
            print(f"       ⏭  language '{lang}' not in target list")
            skipped += 1; skip_reasons["wrong language"] += 1; continue

        # File tree
        tree = check_tree(gh, name, branch)
        repo["_has_tests"] = tree["has_tests"]
        repo["_has_ci"]    = tree["has_ci"]

        # Sedona-profile shape check
        profile = sedona_profile_check(
            repo, len(tree["source_paths"]), tree["source_ratio"]
        )
        if not profile["passes"]:
            flag_str = "; ".join(profile["flags"][:2])
            print(f"       ⏭  {flag_str}")
            skipped += 1; skip_reasons[profile["flags"][0]] += 1; continue

        # ── Real source activity check ────────────────────────────────────────
        print(f"       🔎 checking source activity (last {src_months} months) ...")
        activity = check_source_activity(
            gh, name, tree["source_paths"], months=src_months
        )
        if not activity["active"]:
            print(f"       ⏭  {activity['reason']}")
            skipped += 1; skip_reasons["stale source"] += 1; continue

        print(f"       ✅ src active — last commit to "
              f"'{activity['src_dir']}/' "
              f"{activity['last_src_days']}d ago")

        # Hardware import check (only if hw keywords in metadata)
        text = f"{repo.get('description','').lower()} {name.lower()}"
        hw_hit = any(w in text for w in HW_KEYWORDS)
        sample = sample_source(gh, name, tree["source_paths"]) if hw_hit else ""

        # Testability
        ts = testability_score(repo, sample)
        if testable_only and ts["score"] < 50:
            print(f"       ⏭  testability {ts['score']}% — {ts['verdict']}")
            skipped += 1; skip_reasons["low testability"] += 1; continue

        # Last overall commit
        lc = last_commit(gh, name)

        # Function count (opt-in)
        fc = {}
        if do_funcs and tree["source_paths"]:
            print(f"       🔧 counting functions ...")
            fc = count_funcs(gh, name, tree["source_paths"], max_files)

        results.append({
            "rank":        len(results) + 1,
            "repo":        name,
            "url":         repo["html_url"],
            "lang":        lang,
            "stars":       repo["stargazers_count"],
            "forks":       repo["forks_count"],
            "fork_ratio":  round(repo["_fork_ratio"], 3),
            "desc":        (repo.get("description") or "").strip(),
            "last_commit": lc,
            "activity":    activity,
            "testability": ts,
            "profile":     profile,
            "test_files":  tree["test_files"],
            "has_ci":      tree["has_ci"],
            "source_files":len(tree["source_paths"]),
            "source_ratio":tree["source_ratio"],
            "func_info":   fc,
            "llm_gaps":    llm_gaps(repo, tree),
        })

    # ── Report ────────────────────────────────────────────────────────────────
    SEP = "─" * 72
    print(f"\n\n{'═'*72}")
    print(f"  Results — {len(results)} repos matched  "
          f"({skipped} filtered, {gh.call_count} API calls)")
    if skip_reasons:
        print(f"  Filter breakdown: " +
              ", ".join(f"{v}× {k}" for k, v in skip_reasons.most_common(5)))
    print(f"{'═'*72}\n")

    for r in results:
        lc   = r["last_commit"]
        ts   = r["testability"]
        fc   = r["func_info"]
        act  = r["activity"]
        bar  = "█" * round(ts["score"]/5) + "░" * (20 - round(ts["score"]/5))

        print(f"#{r['rank']:02d}  {r['repo']}  [{r['lang']}]")
        print(f"     {r['url']}")
        print(f"     ⭐ {r['stars']:,}  🍴 {r['forks']:,}  "
              f"fork-ratio: {r['fork_ratio']:.3f}")
        print(f"     📂 {r['source_files']} source files  "
              f"({r['source_ratio']:.0%} of repo is code)")
        print(f"     📝 {r['desc'][:80] or '(no description)'}")

        # Last overall commit
        if lc:
            print(f"     🕐 Last commit   : {lc['date']}  "
                  f"{freshness(lc['days'])}  ({lc['days']}d ago)")
            print(f"                        \"{lc['msg'][:65]}\"  [{lc['sha']}]")

        # Last SOURCE commit (the key new signal)
        print(f"     📦 Last src commit: {act.get('last_src_date','?')}  "
              f"({act.get('last_src_days','?')}d ago)  "
              f"[{act.get('src_dir','?')}/]")
        if act.get("last_src_msg"):
            print(f"                        \"{act['last_src_msg']}\"  "
                  f"[{act.get('last_src_sha','')}]")
        if act.get("src_files_changed"):
            print(f"                        changed: "
                  f"{', '.join(act['src_files_changed'][:3])}")

        print(f"     🧪 Testability   : {ts['score']:3d}%  [{bar}]  {ts['verdict']}")
        if ts["good"]: print(f"        ✅ {' | '.join(ts['good'])}")
        if ts["bad"]:  print(f"        ❌ {' | '.join(ts['bad'])}")
        if r["test_files"]:
            print(f"        📁 {', '.join(r['test_files'][:3])}")
        if r["has_ci"]:
            print(f"        ⚙️  CI detected")

        if r["profile"]["reasons"]:
            print(f"     🎯 Sedona match  : {' | '.join(r['profile']['reasons'])}")

        if fc.get("total") is not None:
            trunc = "  (truncated)" if fc.get("truncated") else ""
            print(f"     🔧 Functions     : {fc['total']} "
                  f"across {fc['files']} files{trunc}")
            for tf in fc.get("top", [])[:3]:
                print(f"          {tf['count']:4d}  {tf['path']}")

        if r["llm_gaps"]:
            print(f"     ⚠️  LLM gaps      : {', '.join(r['llm_gaps'])}")

        print(SEP)

    print(f"\n✅  Done — {len(results)} repos, "
          f"{skipped} filtered out, {gh.call_count} total API calls.\n")
    if not token:
        print("💡 Set --token or GITHUB_TOKEN for 5× rate limits\n")
    return results


# ── CLI ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="GitHub hidden-gem repo analyzer — Sedona-profile + source activity check",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
target languages: {', '.join(TARGET_LANGUAGES)}

source activity check (the key new filter):
  GitHub's 'pushed' date updates on ANY push — including .gitignore edits,
  README typo fixes, CI tweaks. This script verifies that actual source files
  (.py / .go / .rs / .java / etc.) in the main source directory were committed
  within --src-months months. Costs 1-2 extra API calls per repo.

examples:
  python github_repo_analyzer.py --token ghp_xxxx
  python github_repo_analyzer.py --token ghp_xxxx --funcs
  python github_repo_analyzer.py --token ghp_xxxx --language rust
  python github_repo_analyzer.py --token ghp_xxxx --src-months 6
  python github_repo_analyzer.py --token ghp_xxxx --testable-only --top 5
        """,
    )
    ap.add_argument("--token",         default="",
                    help="GitHub token (or set GITHUB_TOKEN env var)")
    ap.add_argument("--language",      default=None,
                    help=f"One of: {', '.join(TARGET_LANGUAGES)} (default: all)")
    ap.add_argument("--min-stars",     type=int, default=200)
    ap.add_argument("--max-stars",     type=int, default=2000)
    ap.add_argument("--min-forks",     type=int, default=20)
    ap.add_argument("--pushed-after",  default="2024-06-01",
                    help="Pre-filter: any push after this date (default 2024-06-01)")
    ap.add_argument("--src-months",    type=int, default=3,
                    help="Source activity window in months (default 3)")
    ap.add_argument("--top",           type=int, default=10)
    ap.add_argument("--funcs",         action="store_true",
                    help="Count functions per repo (needs token to avoid rate limits)")
    ap.add_argument("--max-files",     type=int, default=15)
    ap.add_argument("--testable-only", action="store_true",
                    help="Skip repos with testability < 50%%")
    args = ap.parse_args()

    if args.language and args.language not in TARGET_LANGUAGES:
        print(f"⚠️  '{args.language}' not in target list.")
        print(f"   Valid: {', '.join(TARGET_LANGUAGES)}")
        exit(1)

    analyze(
        token         = args.token,
        language      = args.language,
        min_stars     = args.min_stars,
        max_stars     = args.max_stars,
        min_forks     = args.min_forks,
        pushed_after  = args.pushed_after,
        top           = args.top,
        do_funcs      = args.funcs,
        max_files     = args.max_files,
        testable_only = args.testable_only,
        src_months    = args.src_months,
    )
