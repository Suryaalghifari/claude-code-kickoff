#!/usr/bin/env bash
# Pasang skill kickoff ke ~/.claude/skills/kickoff/
# Pakai: ./install.sh [--uninstall]
set -euo pipefail

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/skill"
DEST="${HOME}/.claude/skills/kickoff"
# Cadangan WAJIB di luar skills/ — apa pun di dalamnya terbaca sebagai skill terpisah,
# sehingga cadangan basi muncul di daftar dengan trigger yang sama.
BACKUP_DIR="${HOME}/.claude/kickoff-backups"

if [[ "${1:-}" == "--uninstall" ]]; then
  rm -rf "$DEST"
  echo "✓ dilepas: $DEST"
  exit 0
fi

# Backup dulu kalau sudah ada — jangan pernah menimpa diam-diam
if [[ -d "$DEST" ]]; then
  mkdir -p "$BACKUP_DIR"
  BACKUP="${BACKUP_DIR}/kickoff.$(date +%Y%m%d-%H%M%S)"
  mv "$DEST" "$BACKUP"
  echo "• versi lama dicadangkan → $BACKUP"
fi

mkdir -p "$DEST"
cp -a "$SRC"/. "$DEST"/          # -a: pertahankan bit executable hook
chmod +x "$DEST"/templates/hooks/* 2>/dev/null || true

echo "✓ terpasang: $DEST"
echo
echo "  Cek:  ls $DEST"
echo "  Pakai: buka folder proyek baru, lalu ketik  /kickoff"
