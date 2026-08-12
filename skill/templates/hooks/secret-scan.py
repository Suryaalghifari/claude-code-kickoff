#!/usr/bin/env python3
"""PreToolUse hook (Write|Edit) — menolak menulis rahasia ke berkas.

Kenapa di sini: git dijalankan user, jadi risikonya bukan pada commit — melainkan pada berkas yang
ditulis agen. Ini satu-satunya jalur di mana rahasia bisa masuk repo tanpa disadari.

Keluar 2 = panggilan tool DIBLOKIR, pesan di stderr dikembalikan ke Claude.
Keluar 0 = lolos. Semua kegagalan tak terduga sengaja lolos — hook yang macet lebih merusak
daripada hook yang melewatkan satu kasus.

Pasang di .claude/settings.json:
  "hooks": { "PreToolUse": [ { "matcher": "Write|Edit",
    "hooks": [ { "type": "command", "command": ".claude/hooks/secret-scan.py" } ] } ] }

CATATAN: berbasis regex, jadi tidak sempurna. Ia menangkap kecelakaan, bukan penyerang.
"""

import json
import re
import sys

PATTERNS = [
    (r"-----BEGIN [A-Z ]*PRIVATE KEY-----", "private key"),
    (r"\bAKIA[0-9A-Z]{16}\b", "AWS access key id"),
    (r"\bghp_[A-Za-z0-9]{36}\b", "GitHub token"),
    (r"\bsk-[A-Za-z0-9]{32,}\b", "API secret key"),
    (r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b", "Slack token"),
    (
        r"(?i)\b(password|passwd|secret|api_?key|token)\s*[:=]\s*"
        r"['\"][^'\"$\{<\s]{8,}['\"]",
        "kredensial literal",
    ),
    (
        r"(?i)\b(postgres|postgresql|mysql|mongodb)(\+srv)?://[^:\s]+:[^@\s]{6,}@",
        "connection string berisi password",
    ),
]

# Nilai contoh yang jelas bukan rahasia sungguhan
PLACEHOLDER = re.compile(
    r"(?i)(your[-_ ]|example|placeholder|changeme|dummy|xxx+|\.\.\.|<[^>]+>|\$\{|\{\{)"
)

# Berkas yang memang tempatnya contoh kredensial
EXEMPT_PATH = re.compile(
    r"(\.example$|\.sample$|\.tmpl$|\.dist$|/(tests?|fixtures?|__mocks__|__tests__)/)"
)


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0

    tool_input = payload.get("tool_input") or {}
    path = str(tool_input.get("file_path", ""))

    if EXEMPT_PATH.search(path):
        return 0

    # Write pakai `content`; Edit pakai `new_string`
    body = "\n".join(
        str(tool_input.get(key, ""))
        for key in ("content", "new_string", "new_str")
    )
    if not body.strip():
        return 0

    hits = []
    for line in body.splitlines():
        if PLACEHOLDER.search(line):
            continue
        for regex, label in PATTERNS:
            if re.search(regex, line):
                hits.append(f"  {label}: {line.strip()[:80]}")
                break

    if not hits:
        return 0

    target = f" ke {path}" if path else ""
    print(
        f"DIBLOKIR — sepertinya ada rahasia di isi yang akan ditulis{target}:\n"
        + "\n".join(hits[:5])
        + "\n\nPakai variabel environment, dan taruh contohnya di .env.example."
        "\nKalau ini positif palsu, beri tahu user — jangan akali polanya.",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    sys.exit(main())
