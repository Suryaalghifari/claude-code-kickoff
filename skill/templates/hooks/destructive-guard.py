#!/usr/bin/env python3
"""PreToolUse hook (Bash) — menolak perintah yang menghancurkan data.

Kenapa hook, bukan aturan di CLAUDE.md: aturan di prompt itu himbauan yang dipatuhi saat model
ingat. Kerusakan di sini **tidak bisa dibatalkan** — tak ada `git revert` untuk basis data yang
sudah dikosongkan, dan `migrate:fresh` di lingkungan yang salah menghapus data produksi dalam satu
detik tanpa konfirmasi.

Kenapa tidak cukup `permissions.deny`: deny mencocokkan bentuk perintah. Perintah yang sama bisa
lewat sebagai `a && b`, di dalam `bash -c`, sebagai target `make`, atau dengan urutan flag berbeda.
Hook membaca seluruh string perintahnya.

Kebijakannya sama dengan aturan git: **Claude tidak menjalankannya, user yang menjalankannya.**
Ini bukan larangan terhadap perintahnya — `migrate:fresh` di basis data lokal itu wajar dan berguna.
Yang dilarang adalah *agen* yang memutuskan sendiri kapan menjalankannya.

Keluar 2 = panggilan tool DIBLOKIR, pesan di stderr dikembalikan ke Claude.
Keluar 0 = lolos. Semua kegagalan tak terduga sengaja lolos — hook yang macet lebih merusak
daripada hook yang melewatkan satu kasus.

Pasang di .claude/settings.json:
  "hooks": { "PreToolUse": [ { "matcher": "Bash",
    "hooks": [ { "type": "command", "command": ".claude/hooks/destructive-guard.py" } ] } ] }

CATATAN: berbasis regex. Ia menangkap kecelakaan, bukan penyerang. Tambahkan pola sesuai stack
proyek — daftar di bawah sengaja pendek supaya tiap barisnya benar-benar dibaca.
"""

import json
import re
import sys

# (regex, label, kenapa fatal). Urut dari yang paling sering terjadi.
PATTERNS = [
    # ── Basis data: mengosongkan / menjatuhkan ────────────────────────────────
    (r"(?i)\bmigrate:(fresh|refresh|reset)\b", "migrate:fresh/refresh/reset",
     "menjatuhkan SEMUA tabel lalu memigrasi ulang — seluruh isi basis data hilang"),
    (r"(?i)\bdb:wipe\b", "db:wipe", "mengosongkan seluruh basis data"),
    (r"(?i)\bprisma\s+migrate\s+reset\b", "prisma migrate reset",
     "menjatuhkan basis data lalu memigrasi ulang dari nol"),
    (r"(?i)--force-reset\b", "--force-reset", "menjatuhkan basis data sebelum push skema"),
    (r"(?i)\b(rails|rake)\s+db:(drop|reset)\b", "rails db:drop/reset", "menjatuhkan basis data"),
    (r"(?i)\bmanage\.py\s+(flush|sqlflush)\b", "manage.py flush",
     "menghapus seluruh baris dari semua tabel"),
    (r"(?i)\bsequelize\s+db:drop\b", "sequelize db:drop", "menjatuhkan basis data"),
    (r"(?i)\bdrop\s+(database|schema)\b", "DROP DATABASE/SCHEMA", "menghapus basis data permanen"),
    (r"(?i)\bdrop\s+table\b", "DROP TABLE", "menghapus tabel beserta isinya"),
    (r"(?i)\btruncate\s+(table\s+)?\w", "TRUNCATE", "mengosongkan tabel, tidak bisa di-rollback"),
    (r"(?i)\bdropDatabase\s*\(", "dropDatabase()", "menghapus basis data MongoDB"),
    # DELETE tanpa WHERE — menghapus seluruh isi tabel
    (r"(?is)\bdelete\s+from\s+\w+\s*(;|$)(?!.*\bwhere\b)", "DELETE FROM tanpa WHERE",
     "menghapus SEMUA baris di tabel itu"),

    # ── Volume & kontainer: data yang dikira aman ─────────────────────────────
    (r"(?i)\bdocker\s+(compose\s+)?down\b[^|;&]*\s-[a-z]*v", "docker compose down -v",
     "menghapus volume — basis data di dalam kontainer ikut hilang"),
    (r"(?i)\bdocker\s+volume\s+rm\b", "docker volume rm", "menghapus volume beserta datanya"),
    (r"(?i)\bdocker\s+system\s+prune\b[^|;&]*--volumes", "docker system prune --volumes",
     "menghapus semua volume yang tak terpakai — termasuk yang kamu kira terpakai"),

    # ── Berkas: hanya yang jelas bencana (rm -rf node_modules/ dll TIDAK diblokir) ──
    (r"\brm\s+-[a-zA-Z]*[rR][a-zA-Z]*f[a-zA-Z]*\s+(/|~|\$HOME|\.)\s*(\*|/)?\s*($|[;&|])",
     "rm -rf pada root/home/direktori-kerja", "menghapus jauh lebih banyak dari yang dimaksud"),

    # ── Git: menghancurkan pekerjaan yang belum ter-commit ────────────────────
    (r"(?i)\bgit\s+reset\s+--hard\b", "git reset --hard",
     "membuang perubahan yang belum di-commit — tak ada di reflog"),
    (r"(?i)\bgit\s+clean\s+-[a-z]*[fd]", "git clean -fd",
     "menghapus berkas tak ter-track, termasuk .env yang tak pernah di-commit"),
    # --force-with-lease sengaja TIDAK diblokir: ia justru bentuk amannya, gagal kalau remote maju
    (r"(?i)\bgit\s+push\b[^|;&]*(--force(?![-\w])|(?<![-\w])-f\b)",
     "git push --force", "menimpa riwayat remote — pekerjaan orang lain bisa hilang"),
]


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0

    tool_input = payload.get("tool_input") or {}
    command = str(tool_input.get("command", ""))
    if not command.strip():
        return 0

    for regex, label, why in PATTERNS:
        if re.search(regex, command):
            print(
                f"DIBLOKIR — perintah ini menghancurkan data dan tidak bisa dibatalkan:\n"
                f"  {label} — {why}\n\n"
                f"  {command.strip()[:160]}\n\n"
                "Kebijakannya sama dengan git: **user yang menjalankannya, bukan Claude.**\n"
                "Kalau ini memang yang diinginkan, sampaikan perintahnya ke user beserta\n"
                "lingkungan yang dituju — biar ia yang mengeksekusi setelah memastikan\n"
                "itu bukan basis data produksi.\n"
                "Kalau ini positif palsu, beri tahu user — jangan akali polanya.",
                file=sys.stderr,
            )
            return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
