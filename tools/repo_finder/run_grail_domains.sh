#!/bin/bash
# run_grail_domains.sh — find GRAIL external-target candidates OUTSIDE geospatial.
#
# GRAIL already covers geospatial (RDPro/beast, Sedona); the generalization
# repos must come from OTHER domains. Runs the finder once per domain query,
# with rubric R1–R7 filters (paper/repo_selection.md) and a geospatial-exclusion
# regex applied to name/description/topics.
#
# Usage:
#   export GITHUB_TOKEN=ghp_xxx        # never hardcode tokens in this file
#   ./run_grail_domains.sh             # Scala + Python + Java, all domains
#   LANGS="Scala" ./run_grail_domains.sh
#   DOMAINS_ONLY="audio processing;3d mesh" ./run_grail_domains.sh   # subset
#
# Depth is language-dependent (set below): Scala totals are tiny (1 page is
# plenty); Python/Java are dense, so they sweep more pages to reach the tail.

set -u
: "${GITHUB_TOKEN:?export GITHUB_TOKEN first (do NOT hardcode it here)}"

SCRIPT="$(dirname "$0")/sedona_shape_repo_finder.py"
OUT="$(dirname "$0")/results_grail"
mkdir -p "$OUT"

# languages ordered by harness cost: Scala (adapter exists) > Python (2 signal
# fixes pending) > Java (visibility model exists, execution adapter new)
LANGS="${LANGS:-Scala Python Java}"

# Domains: scientific/domain fields + hot-topic fields. Every one has (a) rich
# TYPED data models — where LLMs actually fail — and (b) publicly obtainable
# fixtures so Stage-C feasibility passes. Fixture note in parentheses.
DOMAINS=(
  # --- classic scientific (typed numeric/record data) ---
  "bioinformatics"                 # FASTA/BAM/VCF fixtures public
  "genomics"                       # VCF/BAM public
  "proteomics mass spectrometry"   # mzML spectra fixtures public
  "cheminformatics"                # SMILES/SDF molecules
  "molecular dynamics"             # PDB/trajectory fixtures
  "materials science"              # CIF crystal structures
  "quantum computing"              # circuits / state vectors
  "neuroimaging"                   # NIfTI fixtures public
  "medical imaging"                # DICOM (anonymized public sets)
  "time-domain astronomy"          # FITS light curves public
  # --- signal / media (waveform/spectral/tensor data) ---
  "audio processing"              # any WAV/FLAC fixture
  "speech recognition"            # public speech clips
  "digital audio synthesis"       # generated buffers
  "computer vision"               # any image fixture
  "image processing"              # PNG/JPEG fixtures
  "3d mesh geometry"              # OBJ/PLY/STL fixtures public
  "point cloud processing"        # PLY/LAS-lite fixtures
  # --- systems / applied (typed binary / structured) ---
  "biometric fingerprint"         # sample templates/images
  "network packet parsing"        # pcap fixtures public
  "signal processing"             # generated signals
  "time series"                   # CSV series
  "constraint solver optimization" # model files
)

# Optional subset: DOMAINS_ONLY="audio processing;3d mesh geometry"
if [ -n "${DOMAINS_ONLY:-}" ]; then
  IFS=';' read -r -a DOMAINS <<< "$DOMAINS_ONLY"
fi

# Exclude ONLY genuinely-geospatial repos (RDPro/Sedona already cover geo).
# TIGHT list on purpose: bare 'geo' would nuke geoMETRY (3d mesh), 'raster' and
# 'map' would nuke image/vision and read-MAPPING, 'spatial' would nuke spatial
# audio / spatial transcriptomics. Only unambiguously-geospatial terms here.
EXCLUDE='geospatial|geographic|\bgis\b|cartograph|openstreetmap|\bosm\b|remote sensing|shapefile|geojson|postgis|\bgdal\b'

for LANG in $LANGS; do
  # language-dependent depth
  case "$LANG" in
    Scala) PAGES=1; PER=20 ;;   # totals are tiny (bioinfo=4); 1 page covers it
    *)     PAGES=3; PER=30 ;;   # Python/Java dense (bioinfo total 154): reach the tail
  esac
  for D in "${DOMAINS[@]}"; do
    TAG="$(echo "${LANG}_${D}" | tr ' /' '--')"
    echo "=== $LANG / $D  (pages=$PAGES × $PER) ==="
    python3 "$SCRIPT" \
      --language "$LANG" \
      --query-extra "$D" \
      --min-stars 100 --max-stars 5000 --min-forks 10 \
      --pushed-after 2025-01-01 --src-months 12 \
      --min-api 50 --top 10 --pages "$PAGES" --per-page "$PER" \
      --exclude-regex "$EXCLUDE" \
      --csv "$OUT/${TAG}.csv" --json "$OUT/${TAG}.json"
    sleep 20   # be kind to the search rate limit
  done
done

echo "done — merge/rank across all domains × languages:"
echo "python3 tools/repo_finder/rank_candidates.py"
