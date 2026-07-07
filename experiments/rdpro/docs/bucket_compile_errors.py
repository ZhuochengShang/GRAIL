#!/usr/bin/env python3
"""
bucket_compile_errors.py — turn the truncated [compile] failures into a real
frequency count of scalac error types, and specifically tally the RECEIVER type
in "value X is not a member of <TYPE>" so the "wrong receiver" mechanism claim
can be verified instead of inferred.

Two sources of compiler text, in priority order per run dir:
  1. a persisted stderr/compile-output file if the harness left one
  2. --recompile : re-run `scalac` on run_<api>/ApiTest.scala and capture stderr
     (compile only — no jar/spark-submit, so it's fast and needs no network)

Usage:
  # fast path — only parses whatever error text is already on disk
  python bucket_compile_errors.py

  # authoritative — recompile each ApiTest.scala to get fresh, full errors
  python bucket_compile_errors.py --recompile

  # point at non-default locations
  python bucket_compile_errors.py --exec-root ../.aideal_exec \
      --beast-lib beast/target/beast-0.10.1-bin/beast-0.10.1/lib \
      --uber beast/target/beast-uber-0.10.1.jar --recompile
"""
import argparse, glob, os, re, subprocess, sys, tempfile
from collections import Counter, defaultdict

DEF_EXEC   = os.path.expanduser("~/Documents/phd_projects/code/geoAI/GRAIL/experiments/rdpro/.aideal_exec")
DEF_ROOT   = os.path.expanduser("~/Documents/phd_projects/code/geoAI/GRAIL/experiments/rdpro")
DEF_LIB    = os.path.join(DEF_ROOT, "beast/target/beast-0.10.1-bin/beast-0.10.1/lib")
DEF_UBER   = os.path.join(DEF_ROOT, "beast/target/beast-uber-0.10.1.jar")
# scalac ships with pyspark; reuse its scala-compiler jar's classpath dir
PYSPARK_JARS_GLOB = os.path.expanduser("~/miniconda3/envs/*/lib/python*/site-packages/pyspark/jars/*.jar")

ERR_FILE_CANDIDATES = ("compile.err", "stderr.txt", "scalac.err", "scalac.out", "error.txt", "compile.log")

# ---- error taxonomy -------------------------------------------------------
def classify(line):
    if "is not a member of package" in line:            return "hallucinated package / wrong import path"
    m = re.search(r"error:\s+(?:value\s+)?(\S+)\s+is not a member of\s+(.+)", line)
    if m:                                               return ("not a member", m.group(2).strip())
    if "not found: value" in line:                      return "not found: value (bare name / undefined)"
    if "not found: type" in line:                       return "not found: type"
    if "type mismatch" in line:                         return "type mismatch (found/required)"
    if "overloaded method" in line:                     return "overload resolution failed"
    if "not enough arguments for constructor" in line:  return "wrong constructor arity"
    if "not enough arguments for method" in line:       return "wrong method arity"
    if "cannot be accessed" in line:                    return "private / inaccessible member"
    if "reference to" in line and "is ambiguous" in line: return "ambiguous reference"
    return "other error:"

def receiver_bucket(recv):
    r = recv
    if "SparkContext" in r:                                       return "SparkContext (sc.<op>)"
    if "RasterRDD" in r or re.search(r"RDD\[.*ITile", r):         return "RasterRDD / RDD[ITile]"
    if "RasterMetadata" in r:                                     return "RasterMetadata"
    if "ITile" in r:                                              return "ITile"
    if "JavaSpatialRDD" in r or "SpatialRDD" in r:               return "SpatialRDD / JavaSpatialRDD"
    if re.search(r"RDD\[.*IFeature", r) or "IFeature" in r:      return "RDD[IFeature] / IFeature"
    if re.search(r"\bRDD\b", r):                                  return "generic RDD"
    return "other: " + r[:60]

# ---- classpath for --recompile -------------------------------------------
def build_classpath(lib, uber):
    jars = sorted(glob.glob(os.path.join(lib, "*.jar")))
    jars += sorted(glob.glob(PYSPARK_JARS_GLOB))
    if os.path.exists(uber):
        jars.append(uber)
    return ":".join(jars), len(jars)

def recompile_errors(scala_file, classpath):
    with tempfile.TemporaryDirectory() as td:
        try:
            p = subprocess.run(["scalac", "-classpath", classpath, "-d", td, scala_file],
                               capture_output=True, text=True, timeout=180)
            return (p.stdout or "") + (p.stderr or "")
        except subprocess.TimeoutExpired:
            return "[scalac timeout]"
        except FileNotFoundError:
            sys.exit("scalac not on PATH — activate the geo_llm_spark env first.")

def persisted_errors(run_dir):
    for name in ERR_FILE_CANDIDATES:
        fp = os.path.join(run_dir, name)
        if os.path.exists(fp):
            return open(fp, encoding="utf-8", errors="replace").read()
    return ""

# ---- main -----------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--exec-root", default=DEF_EXEC)
    ap.add_argument("--beast-lib", default=DEF_LIB)
    ap.add_argument("--uber", default=DEF_UBER)
    ap.add_argument("--recompile", action="store_true")
    a = ap.parse_args()

    run_dirs = sorted(glob.glob(os.path.join(a.exec_root, "run_*")))
    if not run_dirs:
        sys.exit(f"no run_* dirs under {a.exec_root}")

    classpath = ""
    if a.recompile:
        classpath, n = build_classpath(a.beast_lib, a.uber)
        print(f"[recompile] classpath assembled from {n} jars\n", file=sys.stderr)

    cats = Counter()                       # error category -> count (per API, first error)
    receivers = Counter()                  # "not a member" receiver-type -> count
    examples = defaultdict(list)           # category -> [apis]
    recv_examples = defaultdict(list)      # receiver bucket -> [(api, member, recv)]
    scanned = 0; had_text = 0

    for rd in run_dirs:
        api = os.path.basename(rd).replace("run_", "")
        scala = os.path.join(rd, "ApiTest.scala")
        text = persisted_errors(rd)
        if not text and a.recompile and os.path.exists(scala):
            text = recompile_errors(scala, classpath)
        scanned += 1
        err_lines = [l for l in text.splitlines() if "error:" in l]
        if not err_lines:
            continue
        had_text += 1
        first = err_lines[0]
        c = classify(first)
        if isinstance(c, tuple):           # ("not a member", receiver)
            cats["value/member not on that type"] += 1
            examples["value/member not on that type"].append(api)
            rb = receiver_bucket(c[1])
            receivers[rb] += 1
            mm = re.search(r"(\S+)\s+is not a member", first)
            recv_examples[rb].append((api, mm.group(1) if mm else "?", c[1][:50]))
        else:
            cats[c] += 1
            examples[c].append(api)

    print(f"# scanned {scanned} run dirs; {had_text} had compiler error text "
          f"({'recompiled' if a.recompile else 'persisted-only — use --recompile for full coverage'})\n")
    print("## compile-error categories (one vote per API, first error)")
    for c, n in cats.most_common():
        print(f"{n:4d}  {c}")
        print(f"        e.g. {', '.join(examples[c][:8])}")
    if receivers:
        print("\n## 'not a member of <TYPE>' — receiver-type breakdown  (the mechanism claim)")
        for r, n in receivers.most_common():
            print(f"{n:4d}  {r}")
            for api, mem, recv in recv_examples[r][:4]:
                print(f"        {api}: '{mem}' not a member of {recv}")

if __name__ == "__main__":
    main()
