# Binding sync Hermes

File ini hanya menerjemahkan artefak Hermes. Algoritme, batas perubahan, klasifikasi aturan lokal,
urutan pelaporan, dan kewajiban berhenti tetap kanonis di `references/sync-canonical.md`.

## Cara menjalankan

1. Baca `references/sync-canonical.md` saat `--sync` dipanggil.
2. Jalankan alur S1–S5 di sana, tetapi ganti inventaris dan nama artefaknya dengan tabel di bawah.
3. Abaikan tindakan yang hanya mengelola `.claude/`, hooks, settings, atau slash command Claude.
4. Laporkan diff dan berhenti. Terapkan hanya perubahan yang kemudian disetujui user.

## Binding artefak

| Kanonis Claude | Hermes |
|---|---|
| `CLAUDE.md` | `AGENTS.md` |
| `.claude/commands/{work,revise,fix,verify,pause}.md` | mode `/kickoff {work,revise,fix,verify,pause}`; tidak ada file proyek |
| `.claude/commands/verify.md` sebagai sumber DoD | dokumen DoD yang ditautkan oleh aturan #8 `AGENTS.md` |
| `.claude/settings.json`, `.claude/hooks/*` | di luar scope versi minimum Hermes |
| template skill Claude | bundle Hermes yang sedang terpasang |

Artefak proyek yang diperiksa: `AGENTS.md`, `docs/README.md`, doc set yang dirutekan,
`docs/SYSTEMMAP.md`, `docs/SYSTEMMAP-LOG.md`, `docs/decisions/README.md`, dokumen conventions/DoD,
dokumen Git bila dipilih, dan `.gitignore`.

Bandingkan hanya artefak yang memang dimiliki proyek. Pertahankan keputusan proyek, aturan 9+,
isi decisions, status/utang, LOG, dan penyesuaian lokal seperti yang diwajibkan algoritme kanonis.
