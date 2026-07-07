"""
GitHub Repo Analyzer — Local Web GUI (Fixed)
=============================================
Run:   pip install flask requests
       python github_gui.py
Opens: http://localhost:5000

Paste your GitHub token in the token field (masked, never stored).
"""

import os, re, time, base64, threading, json, uuid
from datetime import datetime, timezone
from flask import Flask, render_template_string, request, jsonify
import requests as req

app = Flask(__name__)

BASE = "https://api.github.com"

# Per-job state: { job_id: { "items": [...], "done": bool, "error": str } }
JOBS: dict = {}
JOBS_LOCK = threading.Lock()

# ── GitHub helpers ─────────────────────────────────────────────────────────────

def gh_get(url, params=None, token="", retries=3):
    """GET with retry on rate-limit. Returns parsed JSON or None."""
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    for attempt in range(retries):
        try:
            r = req.get(url, headers=headers, params=params, timeout=15)
        except Exception as e:
            return None
        if r.status_code == 200:
            return r.json()
        if r.status_code in (403, 429):
            # Respect Retry-After header, or back off exponentially
            wait = int(r.headers.get("Retry-After", 10 * (attempt + 1)))
            time.sleep(min(wait, 60))
        elif r.status_code == 404:
            return None
        else:
            time.sleep(2)
    return None

def days_ago(iso: str) -> int:
    dt = datetime.fromisoformat(iso.rstrip("Z")).replace(tzinfo=timezone.utc)
    return (datetime.now(timezone.utc) - dt).days

def freshness(d: int):
    if d < 30:  return "fresh",  "#22c55e"
    if d < 90:  return "recent", "#eab308"
    if d < 365: return "aging",  "#f97316"
    return              "stale",  "#ef4444"

# ── Testability ────────────────────────────────────────────────────────────────

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

def testability_score(repo: dict, sample: str = "") -> dict:
    score, good, bad = 60, [], []
    text = " ".join([
        repo.get("description") or "",
        repo.get("full_name",""),
        " ".join(repo.get("topics") or []),
    ]).lower()

    hw = [w for w in HW_KEYWORDS if w in text]
    if hw:
        score -= 15 * min(len(hw), 3)
        bad.append(f"hardware keywords: {', '.join(hw[:3])}")

    if sample and HW_IMPORT_RE.search(sample):
        hits = len(HW_IMPORT_RE.findall(sample))
        score -= 40
        bad.append(f"hardware imports detected ({hits})")

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
        "Very testable"           if score >= 75 else
        "Mostly testable"         if score >= 55 else
        "Tricky (external deps)"  if score >= 35 else
        "Hardware/infra dependent"
    )
    color = (
        "#22c55e" if score >= 75 else
        "#eab308" if score >= 55 else
        "#f97316" if score >= 35 else
        "#ef4444"
    )
    return {"score": score, "verdict": verdict, "color": color,
            "good": good, "bad": bad}

# ── File tree ──────────────────────────────────────────────────────────────────

def check_tree(name: str, branch: str, token: str) -> dict:
    data = gh_get(f"{BASE}/repos/{name}/git/trees/{branch}",
                  params={"recursive": "1"}, token=token)
    if not data or "tree" not in data:
        if branch == "main":
            return check_tree(name, "master", token)
        return {"has_tests": False, "has_ci": False,
                "test_files": [], "source_paths": []}

    paths = [n["path"] for n in data["tree"] if n["type"] == "blob"]

    test_files = [
        p for p in paths
        if re.search(r"(^|/)tests?/|test_\w+\.py$|_test\.py$", p, re.I)
    ]
    has_ci = any(
        ".github/workflows" in p or ".travis" in p
        or "tox.ini" == p or "Jenkinsfile" in p
        for p in paths
    )
    source_paths = [
        p for p in paths
        if p.endswith(".py")
        and not any(s in p for s in ["test","vendor","migrations","__pycache__"])
        and not p.startswith(".")
    ]
    return {
        "has_tests":    bool(test_files),
        "has_ci":       has_ci,
        "test_files":   test_files[:5],
        "source_paths": source_paths,
    }

# ── Sample source for hardware-import detection ────────────────────────────────

def sample_source(name: str, paths: list, token: str, n: int = 6) -> str:
    chunks = []
    for p in paths[:n]:
        d = gh_get(f"{BASE}/repos/{name}/contents/{p}", token=token)
        time.sleep(0.12)
        if d and d.get("encoding") == "base64":
            try:
                chunks.append(
                    base64.b64decode(d["content"]).decode("utf-8", "ignore")
                )
            except Exception:
                pass
    return "\n".join(chunks)

# ── Function counting ──────────────────────────────────────────────────────────

FUNC_RE = {
    "python":     re.compile(r"^\s*(?:async\s+)?def\s+\w+\s*\(", re.M),
    "javascript": re.compile(r"(?:function\s+\w+\s*\(|(?:const|let|var)\s+\w+\s*=\s*(?:async\s*)?\(.*?\)\s*=>)", re.M),
    "typescript": re.compile(r"(?:function\s+\w+\s*[\(<]|(?:const|let|var)\s+\w+\s*=\s*(?:async\s*)?\(.*?\)\s*=>)", re.M),
    "go":         re.compile(r"^func\s+(?:\(\w+\s+\*?\w+\)\s+)?\w+\s*\(", re.M),
    "rust":       re.compile(r"^\s*(?:pub\s+)?(?:async\s+)?fn\s+\w+\s*[<(]", re.M),
}
EXTS = {
    "python": [".py"], "javascript": [".js",".jsx"],
    "typescript": [".ts",".tsx"], "go": [".go"], "rust": [".rs"],
}

def count_funcs(name: str, lang: str, paths: list, token: str,
                max_files: int = 30) -> dict:
    pat  = FUNC_RE.get(lang.lower())
    exts = EXTS.get(lang.lower(), [f".{lang}"])
    if not pat:
        return {"total": None, "files": 0, "top": []}

    eligible = [
        p for p in paths
        if any(p.endswith(e) for e in exts)
        and not any(s in p for s in ["test","vendor","node_modules",".min."])
    ][:max_files]

    total, rows = 0, []
    for p in eligible:
        d = gh_get(f"{BASE}/repos/{name}/contents/{p}", token=token)
        time.sleep(0.12)
        if not d or d.get("encoding") != "base64":
            continue
        try:
            code = base64.b64decode(d["content"]).decode("utf-8", "ignore")
        except Exception:
            continue
        n = len(pat.findall(code))
        if n:
            rows.append({"path": p, "count": n})
        total += n

    rows.sort(key=lambda x: x["count"], reverse=True)
    return {
        "total":     total,
        "files":     len(eligible),
        "top":       rows[:4],
        "truncated": len(paths) > max_files,
    }

# ── Last commit ────────────────────────────────────────────────────────────────

def last_commit(name: str, token: str) -> dict:
    data = gh_get(f"{BASE}/repos/{name}/commits",
                  params={"per_page": 1}, token=token)
    if not data or not isinstance(data, list) or not data:
        return {}
    c  = data[0]
    ds = c["commit"]["author"]["date"]
    return {
        "sha":  c["sha"][:7],
        "msg":  c["commit"]["message"].split("\n")[0][:72],
        "date": ds[:10],
        "days": days_ago(ds),
    }

# ── Background analysis worker ─────────────────────────────────────────────────

def push(job_id: str, kind: str, payload: dict):
    with JOBS_LOCK:
        JOBS[job_id]["items"].append({"kind": kind, **payload})

def run_job(job_id: str, token: str, language: str,
            min_stars: int, max_stars: int, min_forks: int,
            pushed_after: str, top: int,
            skip_hw: bool, skip_funcs: bool):
    try:
        push(job_id, "status", {"msg": f"🔍 Searching GitHub for {language} repos…"})

        q = (f"stars:{min_stars}..{max_stars} forks:>{min_forks} "
             f"pushed:>{pushed_after} language:{language}")
        data = gh_get(f"{BASE}/search/repositories",
                      params={"q": q, "sort": "forks",
                              "order": "desc", "per_page": top * 2},
                      token=token)
        time.sleep(1.5)  # respect search rate limit

        if not data:
            push(job_id, "error", {"msg": "GitHub API returned nothing — check your token."})
            return
        if "message" in data:
            push(job_id, "error", {"msg": f"GitHub API error: {data['message']}"})
            return
        if not data.get("items"):
            push(job_id, "error", {"msg": "No repos found for those filters."})
            return

        repos = data["items"]
        for r in repos:
            r["_fork_ratio"] = r["forks_count"] / max(r["stargazers_count"], 1)
        repos.sort(key=lambda r: r["_fork_ratio"], reverse=True)

        push(job_id, "status", {
            "msg": f"✅ Found {len(repos)} candidates — analyzing top {top}…"
        })

        count = 0
        for repo in repos:
            if count >= top:
                break
            name = repo["full_name"]
            push(job_id, "status", {"msg": f"📦 [{count+1}/{top}] Analyzing {name}…"})

            # Full metadata (for size, license, etc.)
            meta = gh_get(f"{BASE}/repos/{name}", token=token) or {}
            time.sleep(0.15)
            branch = meta.get("default_branch", "main")
            for k in ["size","open_issues_count","license","homepage",
                      "description","topics"]:
                repo[k] = meta.get(k, repo.get(k))

            # Tree: test files + CI + source paths
            tree = check_tree(name, branch, token)
            time.sleep(0.15)
            repo["_has_tests"] = tree["has_tests"]
            repo["_has_ci"]    = tree["has_ci"]

            # Sample source for hardware-import detection
            sample = sample_source(name, tree["source_paths"], token, n=5)

            # Testability
            ts = testability_score(repo, sample)
            if skip_hw and ts["score"] < 50:
                push(job_id, "status", {
                    "msg": f"  ⏭ Skipped {name} — {ts['verdict']} ({ts['score']}%)"
                })
                continue

            # Last commit
            lc = last_commit(name, token)
            time.sleep(0.15)

            # Function count
            fc = {}
            if not skip_funcs and tree["source_paths"]:
                push(job_id, "status", {"msg": f"  🔧 Counting functions in {name}…"})
                fc = count_funcs(name, language, tree["source_paths"], token)

            # LLM gaps
            gaps = []
            if not repo.get("description") or len(repo.get("description","")) < 20:
                gaps.append("no/short description")
            if not repo.get("license"):
                gaps.append("no license")
            if not repo.get("homepage"):
                gaps.append("no docs site")

            fl, fc_color = freshness(lc.get("days", 9999)) if lc else ("?", "#888")

            push(job_id, "result", {
                "rank":        count + 1,
                "repo":        name,
                "url":         repo["html_url"],
                "stars":       repo["stargazers_count"],
                "forks":       repo["forks_count"],
                "ratio":       round(repo["_fork_ratio"], 3),
                "desc":        (repo.get("description") or "")[:100],
                "lc_date":     lc.get("date", "?"),
                "lc_days":     lc.get("days", "?"),
                "lc_msg":      lc.get("msg", ""),
                "lc_sha":      lc.get("sha", ""),
                "fresh_label": fl,
                "fresh_color": fc_color,
                "ts_score":    ts["score"],
                "ts_verdict":  ts["verdict"],
                "ts_color":    ts["color"],
                "ts_good":     ts["good"],
                "ts_bad":      ts["bad"],
                "test_files":  tree["test_files"],
                "has_ci":      tree["has_ci"],
                "fn_total":    fc.get("total"),
                "fn_files":    fc.get("files"),
                "fn_top":      fc.get("top", []),
                "fn_trunc":    fc.get("truncated", False),
                "llm_gaps":    gaps,
            })
            count += 1

        push(job_id, "done", {"msg": f"✅ Done — {count} repos analyzed."})

    except Exception as e:
        push(job_id, "error", {"msg": f"Unexpected error: {str(e)}"})
    finally:
        with JOBS_LOCK:
            if job_id in JOBS:
                JOBS[job_id]["done"] = True

# ── API endpoints ──────────────────────────────────────────────────────────────

@app.route("/start", methods=["POST"])
def start():
    body = request.json or {}
    job_id = str(uuid.uuid4())
    with JOBS_LOCK:
        JOBS[job_id] = {"items": [], "done": False, "cursor": 0}

    t = threading.Thread(
        target=run_job,
        args=(
            job_id,
            body.get("token",""),
            body.get("language","python"),
            int(body.get("min_stars", 200)),
            int(body.get("max_stars", 2000)),
            int(body.get("min_forks", 20)),
            body.get("pushed_after","2024-06-01"),
            int(body.get("top", 10)),
            body.get("skip_hw", False),
            body.get("skip_funcs", False),
        ),
        daemon=True,
    )
    t.start()
    return jsonify({"job_id": job_id})


@app.route("/poll/<job_id>")
def poll(job_id: str):
    with JOBS_LOCK:
        job = JOBS.get(job_id)
        if not job:
            return jsonify({"error": "unknown job"}), 404
        cursor = job["cursor"]
        new_items = job["items"][cursor:]
        job["cursor"] = len(job["items"])
        done = job["done"]
    return jsonify({"items": new_items, "done": done})


# ── Frontend ───────────────────────────────────────────────────────────────────

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>GitHub Repo Analyzer</title>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
     background:#0d1117;color:#e6edf3;min-height:100vh}

header{background:#161b22;border-bottom:1px solid #30363d;
       padding:12px 24px;display:flex;align-items:center;gap:12px}
header h1{font-size:16px;font-weight:600}
header .sub{font-size:11px;color:#8b949e;background:#21262d;
            padding:2px 8px;border-radius:12px}

.layout{display:flex;height:calc(100vh - 49px)}

aside{width:270px;flex-shrink:0;background:#161b22;
      border-right:1px solid #30363d;padding:18px 14px;
      overflow-y:auto;display:flex;flex-direction:column;gap:12px}

.field label{display:block;font-size:11px;color:#8b949e;
             margin-bottom:4px;font-weight:500;letter-spacing:.02em}
.field input,.field select{
  width:100%;background:#0d1117;border:1px solid #30363d;
  color:#e6edf3;border-radius:6px;padding:6px 10px;
  font-size:13px;outline:none;transition:border .15s}
.field input:focus,.field select:focus{border-color:#58a6ff}
.field input[type=password]{letter-spacing:2px;font-family:monospace}
.field input[type=date]{color-scheme:dark}
.row2{display:grid;grid-template-columns:1fr 1fr;gap:8px}

.toggle{display:flex;align-items:center;gap:7px;cursor:pointer}
.toggle input[type=checkbox]{width:14px;height:14px;accent-color:#58a6ff;cursor:pointer}
.toggle label{font-size:12px;color:#8b949e;cursor:pointer;line-height:1.3}

#run{width:100%;padding:8px;border-radius:6px;background:#238636;
     border:1px solid #2ea043;color:#fff;font-size:13px;font-weight:600;
     cursor:pointer;margin-top:2px;transition:background .15s}
#run:hover{background:#2ea043}
#run:disabled{background:#1c2128;color:#8b949e;border-color:#30363d;cursor:not-allowed}

#stop{width:100%;padding:8px;border-radius:6px;background:#21262d;
      border:1px solid #f85149;color:#f85149;font-size:13px;font-weight:600;
      cursor:pointer;display:none}
#stop:hover{background:#3b1b1b}

main{flex:1;overflow-y:auto;padding:18px 22px}

#statusbar{font-size:12px;color:#8b949e;margin-bottom:12px;
           min-height:20px;display:flex;align-items:center;gap:7px}
.spinner{width:13px;height:13px;border:2px solid #21262d;
         border-top-color:#58a6ff;border-radius:50%;
         animation:spin .7s linear infinite;flex-shrink:0}
@keyframes spin{to{transform:rotate(360deg)}}

#results{display:flex;flex-direction:column;gap:12px}

.card{background:#161b22;border:1px solid #30363d;border-radius:10px;
      padding:16px 18px;animation:fadeIn .2s ease}
@keyframes fadeIn{from{opacity:0;transform:translateY(5px)}to{opacity:1;transform:none}}

.c-head{display:flex;justify-content:space-between;
        align-items:flex-start;gap:8px;margin-bottom:5px}
.c-title{display:flex;align-items:center;gap:8px}
.rank{font-size:10px;color:#8b949e;background:#21262d;
      padding:1px 7px;border-radius:10px;flex-shrink:0}
.rlink{font-size:15px;font-weight:600;color:#58a6ff;text-decoration:none}
.rlink:hover{text-decoration:underline}
.desc{font-size:12px;color:#8b949e;margin-bottom:9px;line-height:1.5}

.metrics{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:10px}
.badge{font-size:11px;padding:3px 9px;border-radius:20px;
       display:flex;align-items:center;gap:4px}
.b-stars,.b-forks{background:#21262d;color:#e6edf3}
.b-ratio{background:#1f2d3d;color:#58a6ff;font-weight:600}

hr.div{border:none;border-top:1px solid #21262d;margin:9px 0}

.srow{display:flex;align-items:flex-start;gap:8px;
      font-size:12px;margin-bottom:6px}
.slabel{color:#8b949e;white-space:nowrap;min-width:90px;
        padding-top:1px;font-size:11px}
.sval{color:#e6edf3;line-height:1.5;flex:1}

.commit-msg{font-family:monospace;font-size:11px;color:#8b949e;
            margin-top:2px;word-break:break-all}
.sha{background:#21262d;padding:1px 5px;border-radius:4px;
     font-size:10px;font-family:monospace;color:#8b949e}

.bar-wrap{display:flex;align-items:center;gap:8px}
.bar-bg{height:6px;width:90px;background:#21262d;
        border-radius:3px;overflow:hidden;flex-shrink:0}
.bar-fill{height:100%;border-radius:3px}

.tags{display:flex;flex-wrap:wrap;gap:4px;margin-top:5px}
.tag{font-size:10px;padding:2px 7px;border-radius:20px;line-height:1.4}
.tg{background:#1b3a27;color:#3fb950}
.tb{background:#3b1b1b;color:#f85149}
.tf{background:#21262d;color:#8b949e}
.tc{background:#1f2d3d;color:#58a6ff}

.fn-row{display:flex;justify-content:space-between;
        font-size:11px;color:#8b949e;padding:1px 0}
.fn-row b{color:#e6edf3;font-weight:500}

.gap-row{display:flex;flex-wrap:wrap;gap:4px;margin-top:2px}
.gaptag{font-size:10px;padding:2px 7px;border-radius:20px;
        background:#3b2a00;color:#e3b341}

.empty{text-align:center;padding:60px 20px;color:#8b949e;font-size:14px}
.empty .icon{font-size:40px;margin-bottom:12px}

.err-banner{background:#3b1b1b;border:1px solid #f85149;
            border-radius:8px;padding:12px 16px;color:#f85149;font-size:13px}
</style>
</head>
<body>

<header>
  <h1>⭐ GitHub Repo Analyzer</h1>
  <span class="sub">hidden gems · testability · LLM-readiness</span>
</header>

<div class="layout">
  <aside>
    <div class="field">
      <label>🔑 GitHub Token</label>
      <input type="password" id="token" placeholder="ghp_…"
             autocomplete="off" spellcheck="false">
    </div>
    <div class="field">
      <label>Language</label>
      <select id="language">
        <option value="python" selected>Python</option>
        <option value="typescript">TypeScript</option>
        <option value="javascript">JavaScript</option>
        <option value="go">Go</option>
        <option value="rust">Rust</option>
        <option value="java">Java</option>
      </select>
    </div>
    <div class="field row2">
      <div>
        <label>Min stars</label>
        <input type="number" id="min_stars" value="200" min="1">
      </div>
      <div>
        <label>Max stars</label>
        <input type="number" id="max_stars" value="2000" min="1">
      </div>
    </div>
    <div class="field">
      <label>Min forks</label>
      <input type="number" id="min_forks" value="20" min="1">
    </div>
    <div class="field">
      <label>Pushed after</label>
      <input type="date" id="pushed_after" value="2024-06-01">
    </div>
    <div class="field">
      <label>Top N results</label>
      <input type="number" id="top" value="10" min="1" max="30">
    </div>
    <label class="toggle">
      <input type="checkbox" id="skip_hw">
      <label for="skip_hw">Skip hardware / infra repos</label>
    </label>
    <label class="toggle">
      <input type="checkbox" id="skip_funcs">
      <label for="skip_funcs">Skip function counting (faster)</label>
    </label>
    <button id="run" onclick="startAnalysis()">▶ Run Analysis</button>
    <button id="stop" onclick="stopAnalysis()">■ Stop</button>
  </aside>

  <main>
    <div id="statusbar"></div>
    <div id="results">
      <div class="empty">
        <div class="icon">🔭</div>
        Configure filters and click <strong>Run Analysis</strong>
      </div>
    </div>
  </main>
</div>

<script>
let pollTimer = null;
let jobId = null;

function setStatus(msg, loading) {
  document.getElementById('statusbar').innerHTML =
    (loading ? '<div class="spinner"></div>' : '') +
    `<span>${msg}</span>`;
}

function startAnalysis() {
  if (pollTimer) { clearInterval(pollTimer); pollTimer = null; }

  const token = document.getElementById('token').value.trim();
  if (!token) {
    setStatus('❌ Please enter a GitHub token first.', false);
    return;
  }

  document.getElementById('run').disabled = true;
  document.getElementById('stop').style.display = 'block';
  document.getElementById('results').innerHTML = '';
  setStatus('Starting…', true);

  const body = {
    token,
    language:     document.getElementById('language').value,
    min_stars:    +document.getElementById('min_stars').value,
    max_stars:    +document.getElementById('max_stars').value,
    min_forks:    +document.getElementById('min_forks').value,
    pushed_after: document.getElementById('pushed_after').value,
    top:          +document.getElementById('top').value,
    skip_hw:      document.getElementById('skip_hw').checked,
    skip_funcs:   document.getElementById('skip_funcs').checked,
  };

  fetch('/start', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(body),
  })
  .then(r => r.json())
  .then(data => {
    jobId = data.job_id;
    pollTimer = setInterval(pollResults, 800);
  })
  .catch(e => {
    setStatus('❌ Failed to start: ' + e.message, false);
    document.getElementById('run').disabled = false;
    document.getElementById('stop').style.display = 'none';
  });
}

function stopAnalysis() {
  if (pollTimer) { clearInterval(pollTimer); pollTimer = null; }
  jobId = null;
  setStatus('Stopped.', false);
  document.getElementById('run').disabled = false;
  document.getElementById('stop').style.display = 'none';
}

function pollResults() {
  if (!jobId) return;
  fetch('/poll/' + jobId)
    .then(r => r.json())
    .then(data => {
      for (const item of data.items) {
        if (item.kind === 'status') {
          setStatus(item.msg, true);
        } else if (item.kind === 'result') {
          appendCard(item);
        } else if (item.kind === 'error') {
          document.getElementById('results').innerHTML +=
            `<div class="err-banner">❌ ${item.msg}</div>`;
          finish();
        } else if (item.kind === 'done') {
          setStatus(item.msg, false);
          finish();
        }
      }
      if (data.done) finish();
    })
    .catch(() => {});
}

function finish() {
  if (pollTimer) { clearInterval(pollTimer); pollTimer = null; }
  document.getElementById('run').disabled = false;
  document.getElementById('stop').style.display = 'none';
}

function appendCard(r) {
  const goodTags = (r.ts_good||[]).map(g=>`<span class="tag tg">✓ ${g}</span>`).join('');
  const badTags  = (r.ts_bad ||[]).map(b=>`<span class="tag tb">✗ ${b}</span>`).join('');
  const tfTags   = (r.test_files||[]).slice(0,3).map(f=>`<span class="tag tf">📁 ${f.split('/').slice(-2).join('/')}</span>`).join('');
  const ciTag    = r.has_ci ? `<span class="tag tc">⚙ CI</span>` : '';

  const fnBlock = r.fn_total != null ? `
    <div class="srow">
      <span class="slabel">🔧 Functions</span>
      <span class="sval">
        <strong>${r.fn_total}</strong> across <strong>${r.fn_files}</strong> files
        ${r.fn_trunc ? '<span style="color:#8b949e;font-size:10px"> (first 30 files)</span>' : ''}
        <div style="margin-top:3px">
          ${(r.fn_top||[]).map(f=>`
            <div class="fn-row">
              <span>${f.path.split('/').slice(-2).join('/')}</span>
              <b>${f.count} fn</b>
            </div>`).join('')}
        </div>
      </span>
    </div>` : '';

  const gapBlock = (r.llm_gaps||[]).length ? `
    <div class="srow">
      <span class="slabel">⚠ LLM gaps</span>
      <span class="sval">
        <div class="gap-row">
          ${r.llm_gaps.map(g=>`<span class="gaptag">${g}</span>`).join('')}
        </div>
      </span>
    </div>` : '';

  const el = document.createElement('div');
  el.className = 'card';
  el.innerHTML = `
    <div class="c-head">
      <div class="c-title">
        <span class="rank">#${r.rank}</span>
        <a class="rlink" href="${r.url}" target="_blank">${r.repo}</a>
      </div>
    </div>
    <div class="desc">${r.desc || '—'}</div>
    <div class="metrics">
      <span class="badge b-stars">⭐ ${r.stars.toLocaleString()}</span>
      <span class="badge b-forks">🍴 ${r.forks.toLocaleString()}</span>
      <span class="badge b-ratio">fork ratio ${r.ratio}</span>
    </div>
    <hr class="div">
    <div class="srow">
      <span class="slabel">🕐 Last commit</span>
      <span class="sval">
        <span style="color:${r.fresh_color};font-weight:500">${r.fresh_label}</span>
        &nbsp;${r.lc_date}&nbsp;
        <span style="color:#8b949e">(${r.lc_days}d ago)</span>
        &nbsp;<span class="sha">${r.lc_sha}</span>
        <div class="commit-msg">${r.lc_msg}</div>
      </span>
    </div>
    <div class="srow">
      <span class="slabel">🧪 Testability</span>
      <span class="sval">
        <div class="bar-wrap">
          <div class="bar-bg">
            <div class="bar-fill" style="width:${r.ts_score}%;background:${r.ts_color}"></div>
          </div>
          <span style="color:${r.ts_color};font-weight:600">${r.ts_score}%</span>
          <span style="color:#8b949e;font-size:11px">${r.ts_verdict}</span>
        </div>
        <div class="tags">${goodTags}${badTags}${tfTags}${ciTag}</div>
      </span>
    </div>
    ${fnBlock}
    ${gapBlock}`;
  document.getElementById('results').appendChild(el);
}
</script>
</body>
</html>"""

@app.route("/")
def index():
    return render_template_string(HTML)

if __name__ == "__main__":
    import webbrowser
    port = int(os.getenv("PORT", 5000))
    print(f"\n🚀  GitHub Analyzer → http://localhost:{port}\n")
    threading.Timer(1.2, lambda: webbrowser.open(f"http://localhost:{port}")).start()
    app.run(debug=False, port=port, threaded=True)
