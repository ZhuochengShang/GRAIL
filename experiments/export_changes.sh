#!/usr/bin/env bash
# Export every aideal/* branch of a study's clone as a patch into the study's
# changes/ folder (which IS committed to the GRAIL repo, unlike the clone).
#
# Usage:  ./export_changes.sh rdpro/beast
#         ./export_changes.sh sedona/sedona
#
# Reproducing a condition later:
#   git clone <upstream> && cd <clone>
#   git checkout -b aideal/stage2-aliases && git apply ../changes/aideal-stage2-aliases.patch

set -euo pipefail
CLONE="${1:?usage: ./export_changes.sh <study>/<clone-dir>, e.g. rdpro/beast}"
HERE="$(cd "$(dirname "$0")" && pwd)"
CLONE_DIR="$HERE/$CLONE"
STUDY_DIR="$(dirname "$CLONE_DIR")"
OUT="$STUDY_DIR/changes"
mkdir -p "$OUT"

cd "$CLONE_DIR"
BASE="$(git symbolic-ref --short refs/remotes/origin/HEAD 2>/dev/null | sed 's|origin/||' || echo master)"

echo "clone: $CLONE_DIR   base: $BASE"
{
  echo "# Applied changes — exported $(date -u +%Y-%m-%dT%H:%MZ)"
  echo "# upstream: $(git remote get-url origin 2>/dev/null || echo unknown)"
  echo "# base: $BASE @ $(git rev-parse --short "$BASE")"
  echo
} > "$OUT/MANIFEST.md"

for BR in $(git for-each-ref --format='%(refname:short)' refs/heads/aideal/); do
  SAFE="$(echo "$BR" | tr '/' '-')"
  git diff "$BASE".."$BR" > "$OUT/$SAFE.patch"
  STAT="$(git diff --shortstat "$BASE".."$BR")"
  echo "- \`$BR\`:$STAT → $SAFE.patch" >> "$OUT/MANIFEST.md"
  echo "  exported $BR ($STAT)"
done

echo "wrote $OUT/MANIFEST.md"
