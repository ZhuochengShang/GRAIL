"""Bounded, local Java 8 replay with separate writable roots and no network."""
import json
import os
from pathlib import Path
import signal
import subprocess
import time

from .evidence import digest, relocate


def run(command, cwd, timeout):
    env = {k: v for k, v in os.environ.items() if k not in ("JAVA_TOOL_OPTIONS", "_JAVA_OPTIONS", "JDK_JAVA_OPTIONS")}
    started = time.monotonic()
    proc = subprocess.Popen(command, cwd=cwd, env=env, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, text=True, start_new_session=True)
    try:
        stdout, stderr = proc.communicate(timeout=timeout)
        rc = proc.returncode
    except subprocess.TimeoutExpired:
        os.killpg(proc.pid, signal.SIGKILL)  # Only this replay child and its descendants.
        stdout, stderr = proc.communicate()
        rc = 124
    return {"command": command, "exit_code": rc, "stdout": stdout[-20000:],
            "stderr": stderr[-20000:], "wall_s": round(time.monotonic() - started, 3)}


def policy(root):
    # Exclusive policy: reads are allowed, writes only under this variant's root.
    return '''grant {
      permission java.io.FilePermission "<<ALL FILES>>", "read";
      permission java.io.FilePermission %s, "read,write,delete";
      permission java.util.PropertyPermission "*", "read,write";
      permission java.lang.RuntimePermission "*";
      permission java.lang.reflect.ReflectPermission "suppressAccessChecks";
      permission java.awt.AWTPermission "*";
    };\n''' % json.dumps(str(root / "-"))


def java_command(java, classes, jar, root, policy_path, enabled, main="ApiTest"):
    return [str(java), "-ea" if enabled else "-da", "-Xmx256m", "-Djava.awt.headless=true",
            "-Djava.security.manager", "-Djava.security.policy==" + str(policy_path),
            "-Djava.io.tmpdir=" + str(root / "tmp"), "-Duser.home=" + str(root),
            "-Daideal.replay.root=" + str(root), "-cp", str(classes) + os.pathsep + str(jar), main]


def outcome(result, execute):
    text = result["stdout"] + "\n" + result["stderr"]
    if result["exit_code"] == 124:
        return "timeout"
    if "AccessControlException" in text:
        return "isolation_denied"
    if "AssertionError" in text:
        return "assertion_failure"
    if result["exit_code"]:
        return "runtime_failure"
    if execute.get("success_marker", "__DONE__") not in text or execute.get("error_marker", "__RUN_ERR__") in text:
        return "marker_failure"
    if execute.get("require_correctness", True) and execute.get("check_marker", "__CHECK__") not in text:
        return "missing_check_marker"
    return "pass"


def replay(item, snapshot, directory, java_home):
    project = Path(snapshot["project"])
    execute = snapshot["components"]["execute_config"]
    fixtures = execute["sample_data"]
    source, replacements = relocate(item["source"], project, fixtures)
    directory.mkdir(parents=True, exist_ok=False)
    classes = directory / "classes"
    classes.mkdir()
    source_file = directory / "ApiTest.java"
    source_file.write_text(source)
    jar_source = project / execute.get("build_cwd", "source") / execute["uberjar"]
    jar = directory / "library.jar"
    jar.write_bytes(jar_source.read_bytes())
    provenance = {"jar_sha256": digest(jar.read_bytes()), "source_sha256": digest(source.encode()),
                  "path_replacements": replacements, "fixtures": {}}
    compiled = run([str(java_home / "bin/javac"), "-cp", str(jar), "-d", str(classes), str(source_file)], directory, 60)
    result = {"compile": compiled, "provenance": provenance, "variants": {}}
    for label, enabled in [("assertions_off", False), ("assertions_on", True)]:
        if compiled["exit_code"]:
            result["variants"][label] = {"outcome": "compile_failure", "exit_code": compiled["exit_code"]}
            continue
        root = directory / label
        (root / "fixtures").mkdir(parents=True)
        (root / "tmp").mkdir()
        for name, relative in fixtures.items():
            data = (project / relative).read_bytes()
            (root / "fixtures" / (name + Path(relative).suffix)).write_bytes(data)
            provenance["fixtures"][name] = {"source": relative, "sha256": digest(data)}
        permission_file = directory / (label + ".policy")
        permission_file.write_text(policy(root))
        command = java_command(java_home / "bin/java", classes, jar, root, permission_file, enabled)
        event = run(command, root, snapshot["components"].get("timeout_s", 600))
        event["outcome"] = outcome(event, execute)
        result["variants"][label] = event
    return result
