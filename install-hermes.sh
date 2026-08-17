#!/usr/bin/env bash
# Pasang bundle kickoff Hermes yang self-contained.
# Pakai: ./install-hermes.sh
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HERMES_SOURCE="${REPO_ROOT}/hermes"
CANONICAL_REFERENCES="${REPO_ROOT}/skill/references"
GENERIC_TEMPLATES="${REPO_ROOT}/skill/templates"
SKILLS_ROOT="${KICKOFF_HERMES_SKILLS_ROOT:-${HOME}/.hermes/skills}"
DEST="${SKILLS_ROOT}/software-development/kickoff"
BACKUP_ROOT="${KICKOFF_HERMES_BACKUP_ROOT:-${HOME}/.hermes/kickoff-backups}"
STAGE_ROOT="$(mktemp -d)"
STAGE="${STAGE_ROOT}/kickoff"

cleanup() {
  rm -rf "$STAGE_ROOT"
}
trap cleanup EXIT

mkdir -p "$STAGE/references" "$STAGE/templates"
cp "$HERMES_SOURCE/SKILL.md" "$STAGE/SKILL.md"
cp "$CANONICAL_REFERENCES"/*.md "$STAGE/references/"
mv "$STAGE/references/sync.md" "$STAGE/references/sync-canonical.md"
cp "$HERMES_SOURCE/references/sync.md" "$STAGE/references/sync.md"
cp "$HERMES_SOURCE/templates/AGENTS.md.tmpl" "$STAGE/templates/AGENTS.md.tmpl"
cp "$GENERIC_TEMPLATES/SYSTEMMAP-LOG.md.tmpl" "$STAGE/templates/SYSTEMMAP-LOG.md.tmpl"
cp "$GENERIC_TEMPLATES/decisions-README.md.tmpl" "$STAGE/templates/decisions-README.md.tmpl"

if [[ -e "$DEST" ]]; then
  mkdir -p "$BACKUP_ROOT"
  BACKUP="${BACKUP_ROOT}/kickoff.$(date +%Y%m%d-%H%M%S)"
  mv "$DEST" "$BACKUP"
  echo "• versi lama dicadangkan → $BACKUP"
fi

mkdir -p "$(dirname "$DEST")"
mv "$STAGE" "$DEST"

echo "✓ terpasang: $DEST"
echo "  Pakai: /kickoff"
