from pathlib import Path

import yaml

from aideal.config import load_config
from aideal.doc_checks import _classify_error, _fill_scaffold
from aideal.readme_agent import api_test_examples, public_api_details


def test_java_adapter_mines_public_javadoc_and_junit(tmp_path: Path):
    src = tmp_path / "source" / "src" / "main" / "java" / "org" / "example"
    tests = tmp_path / "source" / "src" / "test" / "java" / "org" / "example"
    src.mkdir(parents=True)
    tests.mkdir(parents=True)
    (src / "Molecule.java").write_text(
        "public class Molecule {\n"
        "  public Molecule(int atoms, String label[]) {}\n"
        "  /** Return the atom count. */\n"
        "  public int atomCount() { return 0; }\n"
        "  public void exercise() {\n"
        "    atomCount();\n"
        "    if (atomCount() > 0) {}\n"
        "  }\n"
        "  protected int internalCount() { return 0; }\n"
        "  private int secretCount() { return 0; }\n"
        "}\n",
        encoding="utf-8",
    )
    (tests / "MoleculeTest.java").write_text(
        "import org.junit.jupiter.api.Test;\n"
        "class MoleculeTest {\n"
        "  @Test void countsAtoms() {\n"
        "    new Molecule().atomCount();\n"
        "  }\n"
        "}\n",
        encoding="utf-8",
    )
    (tmp_path / "configs").mkdir()
    (tmp_path / "configs" / "aideal.yaml").write_text(
        yaml.safe_dump({
            "extends": ["java"],
            "project": {"name": "molecule", "language": "Java"},
            "codebase": {
                "source_globs": ["source/src/main/java/**/*.java"],
                "test_globs": ["source/src/test/java/**/*.java"],
            },
        }),
        encoding="utf-8",
    )

    cfg = load_config(tmp_path / "configs" / "aideal.yaml")
    all_details = public_api_details(cfg)
    details = {d["name"]: d for d in all_details}
    assert sum(d["name"] == "atomCount" for d in all_details) == 1
    assert "if" not in details
    assert details["Molecule"]["signature"] == "public Molecule(int atoms, String label[])"
    assert details["Molecule"]["params"] == [
        {"name": "atoms", "type": "int", "default": ""},
        {"name": "label", "type": "String[]", "default": ""},
    ]
    assert details["Molecule"]["returns"] == ""
    assert details["atomCount"]["visibility"] == "public"
    assert details["atomCount"]["signature"] == "public int atomCount()"
    assert details["atomCount"]["returns"] == "int"
    assert details["atomCount"]["description"] == "Return the atom count."
    assert details["internalCount"]["visibility"] == "non-public"
    assert details["secretCount"]["visibility"] == "non-public"

    examples = api_test_examples(cfg)
    assert "atomCount" in examples
    assert "countsAtoms" in examples["atomCount"][0]["test"]


def test_java_scaffold_and_error_classification():
    scaffold = (
        "public class ApiTest {\n"
        "  public static void main(String[] args) {\n"
        "    // TODO API_TEST_START\n"
        "    // TODO API_TEST_END\n"
        "  }\n"
        "}\n"
    )
    filled = _fill_scaffold(
        scaffold, "System.out.println(1);",
        ["// TODO API_TEST_START", "// TODO API_TEST_END"], {})
    assert "    System.out.println(1);" in filled

    category, message, locus = _classify_error(
        "ApiTest.java:7: error: cannot find symbol\n", 1, "__RUN_ERR__", "Java")
    assert category == "compile"
    assert "cannot find symbol" in message
    assert locus == "ApiTest.java:7"

    category, message, _ = _classify_error(
        "__RUN_ERR__ IllegalArgumentException: bad molecule\n"
        "at ApiTest.main(ApiTest.java:12)\n", 1, "__RUN_ERR__", "Java")
    assert category == "runtime"
    assert "IllegalArgumentException" in message

    category, _, _ = _classify_error(
        "java.lang.NoClassDefFoundError: org/openscience/cdk/Atom\n",
        1, "__RUN_ERR__", "Java")
    assert category == "infra"
