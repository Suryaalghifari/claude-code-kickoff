#!/usr/bin/env python3
"""SessionStart hook — menyuntikkan fokus & utang terbuka ke konteks awal sesi.

Kenapa hook, bukan baris di CLAUDE.md: baris router bisa dilewat kalau tugasnya terasa jelas.
Ini tidak. Dua hal inilah yang menentukan "kerjakan apa" dan "apa yang tertinggal".

Sengaja pelit: keluaran ini masuk ke SETIAP sesi, jadi tiap baris dibayar berulang kali.
Batasnya di MAX_ROWS/MAX_WIDTH — naikkan hanya kalau benar-benar kurang.

Pasang di .claude/settings.json:
  "hooks": { "SessionStart": [ { "hooks": [
      { "type": "command", "command": ".claude/hooks/session-start.py" } ] } ] }
"""

import re
import sys
from pathlib import Path

MAP = Path("docs/SYSTEMMAP.md")
MAX_ROWS = 5
MAX_WIDTH = 140


def clip(text: str) -> str:
    text = text.strip()
    return text if len(text) <= MAX_WIDTH else text[: MAX_WIDTH - 1] + "…"


def is_data_row(line: str) -> bool:
    """Baris tabel berisi — bukan pemisah |---|, bukan header."""
    stripped = line.strip()
    if not stripped.startswith("|"):
        return False
    return not re.fullmatch(r"\|[\s:|-]*\|?", stripped)


def section(lines: list[str], pattern: str) -> list[str]:
    """Baris di bawah heading yang cocok, sampai heading berikutnya."""
    out: list[str] = []
    inside = False
    for line in lines:
        if line.startswith("#"):
            if inside:
                break
            inside = bool(re.search(pattern, line, re.I))
            continue
        if inside:
            out.append(line)
    return out


def main() -> int:
    if not MAP.exists():
        return 0

    lines = MAP.read_text(encoding="utf-8").splitlines()
    parts: list[str] = []

    # Fokus — satu baris, sesuai protokol
    focus = next((l for l in lines if l.startswith("## 🎯")), None)
    parts.append(clip(focus.lstrip("# ")) if focus else "🎯 Fokus belum diisi")

    # Utang terbuka — heading bebas asal memuat kata "utang"
    debts = [clip(l) for l in section(lines, r"utang") if is_data_row(l)]
    # buang baris header tabel
    debts = [d for d in debts if not re.search(r"\|\s*(sejak|kapan)\s*\|", d, re.I)]
    if debts:
        parts.append("\n### Utang terbuka\n" + "\n".join(debts[:MAX_ROWS]))

    # Sedang dikerjakan — hanya baris tabel, bukan legenda/kutipan
    wip = [
        clip(l)
        for l in lines
        if "🟨" in l and is_data_row(l) and "legenda" not in l.lower()
    ]
    if wip:
        parts.append("\n### Sedang dikerjakan (🟨)\n" + "\n".join(wip[:MAX_ROWS]))

    print(f"## Status proyek (dari {MAP})\n")
    print("\n".join(parts))
    print("\n> Belum diverifikasi end-to-end = 🟨, bukan ✅.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
