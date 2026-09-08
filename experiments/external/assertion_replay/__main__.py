"""Resumable local replay observer. Never starts or changes measured experiments."""
import argparse
from datetime import datetime
import fcntl
import json
import os
from pathlib import Path
import time
import uuid

from .evidence import collect, digest, retained_source
from .execute import java_command, policy, replay, run
from .report import atomic, publish


def preflight(work, java_home):
    folder = work / ("preflight-" + uuid.uuid4().hex[:12])
    root = folder / "allowed"
    (root / "tmp").mkdir(parents=True)
    classes = folder / "classes"
    classes.mkdir()
    source = folder / "GuardTest.java"
    source.write_text('''import java.io.*; import java.net.*;
public class GuardTest {
 public static void main(String[] args) throws Exception {
  new FileOutputStream(System.getProperty("aideal.replay.root")+"/allowed.txt").close();
  int denied=0;
  try { new FileOutputStream(System.getProperty("aideal.replay.root")+"/../denied.txt").close(); }
  catch (SecurityException e) { denied++; }
  try { new Socket("127.0.0.1", 9).close(); } catch (SecurityException e) { denied++; }
  try { Runtime.getRuntime().exec("/usr/bin/true"); } catch (SecurityException e) { denied++; }
  if (denied != 3) throw new IllegalStateException("isolation sentinel failed: "+denied);
  System.out.println("denied="+denied+" assertions="+GuardTest.class.desiredAssertionStatus());
  System.out.println("__CHECK__ sentinel __DONE__");
  assert false : "sentinel must fail with assertions enabled";
 }
}''')
    compiled = run([str(java_home / "bin/javac"), "-d", str(classes), str(source)], folder, 60)
    if compiled["exit_code"]:
        raise RuntimeError(compiled)
    permission = folder / "replay.policy"
    permission.write_text(policy(root))
    events = {}
    for name, enabled in [("off", False), ("on", True)]:
        command = java_command(java_home / "bin/java", classes, classes, root, permission, enabled, "GuardTest")
        events[name] = run(command, root, 30)
    assert events["off"]["exit_code"] == 0 and "denied=3 assertions=false" in events["off"]["stdout"], events
    assert events["on"]["exit_code"] != 0 and "AssertionError" in events["on"]["stderr"] and "denied=3 assertions=true" in events["on"]["stdout"], events
    return {"checked_at": datetime.now().astimezone().isoformat(), "compile": compiled, "events": events,
            "java_version": run([str(java_home / "bin/java"), "-version"], folder, 30),
            "checks": ["writes inside root allowed", "writes outside root denied", "network denied", "child execution denied", "assertion false fails despite printed success markers"]}


def once(args, protocol):
    cells = {}
    for cell in ("A2", "A1", "B1", "B2"):
        project = args.workspace_parent / f"GRAIL_thumbnailator_{cell}/experiments/external/thumbnailator"
        snapshot = collect(project, cell) if project.exists() else None
        if snapshot is None:
            continue
        current = {k: v for k, v in snapshot.items() if k not in ("rows", "components")}
        records = []
        current["records"] = records
        cells[cell] = current
        execute = snapshot["components"]["execute_config"]
        fixture_hashes = {name: digest((project / path).read_bytes()) for name, path in execute["sample_data"].items()}
        jar_hash = digest((project / execute.get("build_cwd", "source") / execute["uberjar"]).read_bytes())
        for name, row in snapshot["rows"].items():
            item = retained_source(project, cell, row)
            if item.get("binding") == "retained_unbound_legacy" and sum(n.casefold() == name.casefold() for n in snapshot["rows"]) > 1:
                item = {"available": False, "reason": "case-colliding retained path without native code binding"}
            record = {"api": name, "cell": cell, "native": row, **item}
            records.append(record)
            if not item["available"]:
                continue
            key = digest({"protocol": protocol, "cell": cell, "api": name, "source": item["source"],
                          "native": row, "jar": jar_hash, "fixtures": fixture_hashes})
            evidence_file = args.out / "cases" / (key + ".json")
            if evidence_file.exists():
                record.update(json.loads(evidence_file.read_text()))
            else:
                directory = args.work / cell / (key[:20] + "-" + uuid.uuid4().hex[:8])
                record["replay"] = replay(item, snapshot, directory, args.java_home)
                record["protocol"] = protocol
                record["captured_native_source"] = {"path": snapshot["source_path"], "sha256": snapshot["source_sha256"]}
                record["evidence_file"] = str(evidence_file.relative_to(args.out))
                atomic(evidence_file, json.dumps(record, indent=2) + "\n")
                print(cell, name, record["replay"]["variants"]["assertions_on"]["outcome"], flush=True)
            if len(records) % 10 == 0:
                atomic(args.out / "heartbeat.json", json.dumps({"pid": os.getpid(), "at": time.time(), "cell": cell, "processed": len(records)}))
        publish(args.out, cells)
    publish(args.out, cells)
    return len(cells) == 4 and all(c["complete"] for c in cells.values())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace-parent", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--work", type=Path, required=True)
    parser.add_argument("--java-home", type=Path, required=True)
    parser.add_argument("--watch", action="store_true")
    parser.add_argument("--interval", type=int, default=120)
    args = parser.parse_args()
    for name in ("workspace_parent", "out", "work", "java_home"):
        setattr(args, name, getattr(args, name).resolve())
    (args.out / "cases").mkdir(parents=True, exist_ok=True)
    args.work.mkdir(parents=True, exist_ok=True)
    with (args.out / "observer.lock").open("a+") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        lock.seek(0)
        lock.truncate()
        lock.write(str(os.getpid()))
        lock.flush()
        checked = preflight(args.work, args.java_home)
        atomic(args.out / "preflight.json", json.dumps(checked, indent=2) + "\n")
        protocol = {"version": "thumbnailator-assertion-replay-v1", "java_version": checked["java_version"]["stderr"],
                    "engine": {p.name: digest(p.read_bytes()) for p in Path(__file__).parent.glob("*.py") if p.name != "report.py" and not p.name.startswith("test_")},
                    "llm_calls": 0, "code_fix_rounds": 0}
        while True:
            complete = once(args, protocol)
            atomic(args.out / "heartbeat.json", json.dumps({"pid": os.getpid(), "at": time.time(), "all_native_cells_complete": complete, "watch": args.watch}))
            if complete or not args.watch:
                return
            time.sleep(max(10, args.interval))


if __name__ == "__main__":
    main()
