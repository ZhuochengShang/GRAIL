import re
from functools import lru_cache
from pathlib import Path

API_PATTERN = re.compile(
    r"\.\s*(geoTiff|shapefile|mapPixels|filterPixels|overlay|raptorJoin|mask|saveAsGeoTiff|reshapeNN|reproject)\b"
)

API_DOC_FILES = {
    "geoTiff": "geoTiff.md",
    "mapPixels": "mapPixels.md",
    "overlay": "overlay.md",
    "raptorJoin": "raptorjoin.md",
    "saveAsGeoTiff": "saveAsGeoTiff.md",
    "reshapeNN": "reshape.md",
    "reproject": "reshape.md",
}

FALLBACK_GUIDES = {
    "shapefile": {
        "failure_cases": [
            "Optional vector path passed directly into shapefile instead of unwrapping to a concrete String path.",
            "Vector load typed as Option[RDD[IFeature]] instead of RDD[IFeature].",
            "Using `count()` only to validate the vector load instead of a cheap probe like `take(1)`.",
        ],
        "fix_snippet": (
            "val vector: RDD[IFeature] = sc.shapefile(primaryVectorPath)\n"
            "if (vector.take(1).isEmpty) {\n"
            "  throw new IllegalArgumentException(\"No valid geometries found in shapefile\")\n"
            "}"
        ),
    },
    "filterPixels": {
        "failure_cases": [
            "Predicate lambda returns a non-Boolean value or the lambda parameter type is inferred incorrectly.",
            "filterPixels is chained directly into another raster op, hiding the failing call site from the compile loop.",
        ],
        "fix_snippet": "val out: RasterRDD[Float] = in.filterPixels((v: Float) => v != -9999.0f)",
    },
    "raptorJoin": {
        "failure_cases": [
            "Vector-driven mask or clip logic was implemented with value filtering instead of raster-vector pairing.",
            "Joined raster/vector output is treated like a tuple instead of using the documented named fields.",
        ],
        "fix_snippet": (
            "val vector: RDD[IFeature] = sc.shapefile(primaryVectorPath)\n"
            "val joined: RDD[RaptorJoinFeature[Int]] = raster.raptorJoin(vector)"
        ),
    },
    "geoTiff": {
        "failure_cases": [
            "Comparing pixelType to string literals such as \"int32\" or \"float32\" instead of Spark SQL type objects.",
            "Using a typed raster read assumption that does not match the runtime pixelType.",
            "Calling `count()` on RasterRDD only for logging or validation, forcing a full raster scan.",
        ],
        "fix_snippet": (
            "val firstRaster = raster.take(1).headOption.getOrElse(\n"
            "  throw new IllegalArgumentException(\"Raster is empty\"))\n"
            "if (firstRaster.pixelType != IntegerType) {\n"
            "  throw new RuntimeException(s\"Expected IntegerType but got ${firstRaster.pixelType}\")\n"
            "}"
        ),
    },
}


def _doc_root() -> Path:
    return Path(__file__).resolve().parents[2] / "Doc"


def extract_called_apis(scala_text: str) -> list[str]:
    apis: list[str] = []
    for match in API_PATTERN.finditer(scala_text or ""):
        api = match.group(1)
        if api == "mask":
            api = "raptorJoin"
        if api not in apis:
            apis.append(api)
    return apis


def _extract_heading_section(text: str, heading: str) -> str:
    match = re.search(
        rf"(?ms)^### {re.escape(heading)}\s*$\n(.*?)(?=^### |\Z)",
        text or "",
    )
    return match.group(1).strip() if match else ""


def _extract_code_block(text: str) -> str:
    match = re.search(r"(?ms)^```(?:scala)?\n(.*?)^```$", text or "")
    return match.group(1).strip() if match else ""


def _extract_bullets(text: str) -> list[str]:
    return [m.group(1).strip() for m in re.finditer(r"(?m)^-\s+(.*)$", text or "")]


@lru_cache(maxsize=None)
def load_api_fix_guide(api: str) -> dict:
    fallback = FALLBACK_GUIDES.get(api, {})
    doc_name = API_DOC_FILES.get(api)
    if not doc_name:
        return {
            "api": api,
            "source": "",
            "failure_cases": list(fallback.get("failure_cases", [])),
            "fix_snippet": str(fallback.get("fix_snippet", "") or "").strip(),
        }

    doc_path = _doc_root() / doc_name
    if not doc_path.exists():
        return {
            "api": api,
            "source": "",
            "failure_cases": list(fallback.get("failure_cases", [])),
            "fix_snippet": str(fallback.get("fix_snippet", "") or "").strip(),
        }

    text = doc_path.read_text(encoding="utf-8", errors="ignore")
    failure_cases = _extract_bullets(_extract_heading_section(text, "Failure case to include"))
    fix_snippet = _extract_code_block(_extract_heading_section(text, "Fix snippet"))

    if not failure_cases:
        failure_cases = list(fallback.get("failure_cases", []))
    if not fix_snippet:
        fix_snippet = str(fallback.get("fix_snippet", "") or "").strip()

    return {
        "api": api,
        "source": str(doc_path),
        "failure_cases": failure_cases,
        "fix_snippet": fix_snippet,
    }


def render_api_fix_guides(apis: list[str]) -> str:
    if not apis:
        return ""

    lines = ["API_FIX_GUIDES:"]
    for api in apis:
        guide = load_api_fix_guide(api)
        if not guide.get("failure_cases") and not guide.get("fix_snippet"):
            continue
        lines.append(f"- API: {api}")
        if guide.get("source"):
            lines.append(f"  source: {guide['source']}")
        if guide.get("failure_cases"):
            lines.append("  failure_cases:")
            for item in guide["failure_cases"]:
                lines.append(f"    - {item}")
        if guide.get("fix_snippet"):
            lines.append("  fix_snippet:")
            lines.append("```scala")
            lines.append(guide["fix_snippet"])
            lines.append("```")
    return "\n".join(lines)
