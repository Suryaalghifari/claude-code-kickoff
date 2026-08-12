# Mode `--sync` — Proyek yang Lahir dari Skill Versi Lama

Proyek yang sudah di-`/kickoff` memegang **salinan** dari `templates/`. Saat skill diperbaiki,
salinan itu **tidak ikut berubah** — `./install.sh` hanya memperbarui skill di `~/.claude/skills/`.
Akibatnya proyek tetap membaca aturan yang sudah dicabut, tiap sesi, tanpa ada yang menyadarinya.

Ini pola aturan #9 satu tingkat di atas: di sana `references/` diperbaiki tapi `templates/`
tertinggal; di sini **skill** diperbaiki tapi **proyek yang terlanjur lahir** tertinggal.

| Mode | Masukan | Yang dihasilkan |
|---|---|---|
| `--audit` | **kode proyek** — belum ada sistem konteks | sistem konteks baru dari yang terbaca |
| `--sync` | **artefak hasil generate** vs `templates/` sekarang | usulan suntingan pada berkas yang sudah basi |

> **Aturan mutlak, sama dengan `--audit`: JANGAN timpa apa pun.** Tunjukkan tiap perubahan, satu per
> satu, dan kerjakan hanya yang disetujui.

---

## S1 — Pastikan mode ini yang tepat

`--sync` hanya untuk proyek yang **sudah punya** sistem konteks hasil `/kickoff`. Tanda:

```bash
ls CLAUDE.md docs/SYSTEMMAP.md .claude/commands/ 2>/dev/null
```

Tak ada? Itu `--audit`, bukan `--sync`. Ada tapi jelas ditulis tangan tanpa skill ini → tanyakan;
jangan paksakan bentuk templat ke sistem yang sudah bekerja dengan bentuk lain.

## S2 — Cari penanda aturan yang sudah dicabut

Inti mode ini. Tiap kali sebuah aturan dicabut dari skill, penandanya dicatat di tabel bawah —
sehingga `--sync` cukup mencari penanda itu di proyek, bukan mendiff seluruh berkas.

```bash
grep -rn '<penanda>' CLAUDE.md docs/ .claude/
```

### Tabel penanda — aturan yang sudah mati

Cari penanda kiri; kalau ketemu, berkas itu basi dan usulkan penggantinya.

| Penanda di proyek | Sudah diganti oleh | Berkas yang disunting |
|---|---|---|
| `Delapan pertanyaan` (tabel komentar) | uji tunggal "apakah orang akan merapikan lalu merusak" | `docs/<NN>-conventions.md` |
| `hanya "WHY"` · `Minimal "WHY"` · `non-obvious` | komentar **default NOL** | `docs/<NN>-conventions.md`, `CLAUDE.md` aturan #2 |
| tak ada bagian docblock di dokumen konvensi | docblock tunduk uji yang sama | `docs/<NN>-conventions.md` |
| baris routing `§x.y` / "arti rujukan di komentar kode" | komentar kode dilarang merujuk ke mana pun → **hapus barisnya** | `CLAUDE.md` tabel routing |
| langkah 4 tanpa "2 tetangga" | prosedur cari-dua-tetangga | `.claude/commands/work.md`, `CLAUDE.md` §Alur |
| lapis 3 tanpa pemeriksaan jumlah query | gerbang query untuk alur yang menyentuh DB | `.claude/commands/verify.md` |
| tak ada `0X-deployment.md` padahal deploy sudah jalan | realitas deploy dibaca dari CI/Dockerfile | usulkan dokumen baru — lihat `audit.md` §A2 |
| **tak ada `.claude/hooks/destructive-guard.py`** | pagar perintah perusak data | salin hook + daftarkan `PreToolUse`/`Bash` + isi `deny` sesuai stack (`interview.md`) |

> Baris terakhir **prioritas tertinggi** apa pun urutan lainnya: proyek tanpa pagar ini bisa
> kehilangan seluruh basis datanya dalam satu perintah, dan itu satu-satunya kerusakan di daftar ini
> yang tak bisa dibatalkan.

> **Menambah baris ke tabel ini adalah bagian dari mencabut aturan.** Aturan yang dicabut tanpa
> penandanya dicatat di sini membuat `--sync` buta terhadapnya — dan proyek lama akan memegangnya
> selamanya. Ini disiplin yang menjaga mode ini tetap berguna.

## S3 — Batas yang harus dihormati

Yang boleh disentuh **hanya artefak yang dulu disalin dari `templates/`**:

```
CLAUDE.md · docs/README.md · docs/<NN>-conventions.md · docs/<NN>-git-workflow.md
docs/SYSTEMMAP.md (kerangka) · .claude/commands/*.md · .claude/hooks/*.py · .claude/settings.json
```

Yang **tidak pernah** disentuh:

- **Kode.** Sama sekali. Aturan komentar yang berubah **tidak** berarti membersihkan komentar lama
  secara massal — itu diff besar tanpa perubahan perilaku. Aturan baru berlaku untuk yang ditulis
  **sesudahnya**; yang lama dibersihkan hanya saat barisnya memang sedang disentuh.
- **Dokumen isi proyek** — data-model, design-system, security, architecture. Itu tulisan pemiliknya,
  bukan templat.
- **`docs/decisions/` dan `SYSTEMMAP-LOG.md`.** Riwayat tak pernah disunting surut.
- **Bagian spesifik-stack** di dokumen konvensi. Ia memang dihasilkan per proyek — ganti hanya
  kerangka Lapis 0–2 di sekitarnya, jangan sentuh aturan stack-nya.
- **Aturan bernomor #9+** di `CLAUDE.md` proyek. Itu lahir dari kegagalan proyek itu sendiri dan
  tidak ada hubungannya dengan versi skill.

## S4 — Laporkan, lalu kerjakan yang disetujui

Sajikan sebagai tabel, dan **tunjukkan diff tiap berkas sebelum menulisnya**:

| Berkas | Yang basi | Usulan | Dampak |
|---|---|---|---|
| `docs/<NN>-conventions.md` | tabel 8 pertanyaan (baris 77) | ganti dengan uji tunggal + bagian docblock | tinggi — ini yang dibaca tiap ngoding |
| `CLAUDE.md` | baris routing `§x.y` | hapus barisnya | tinggi — ia melembagakan praktik yang dilarang |
| `.claude/commands/work.md` | langkah 4 tanpa prosedur | tambahkan cari-dua-tetangga | sedang |

Urutkan **berdasarkan seberapa sering berkasnya dibaca**, bukan panjang diff-nya. `CLAUDE.md` dan
dokumen konvensi dimuat tiap sesi; sisanya hanya saat dipanggil.

Setelah selesai, tulis **satu entri** `SYSTEMMAP-LOG.md` bertanda `#SYNC`: versi apa yang disamakan,
berkas apa yang berubah, dan apa yang sengaja dilewati. Tanpa entri ini, sinkronisasi berikutnya
tak punya titik awal.

## Kapan menjalankannya

Setelah `./install.sh` yang membawa perubahan aturan — bukan tiap kali. Perubahan yang hanya
menyentuh `references/` (cara Claude bekerja saat kickoff) tak pernah sampai ke proyek lama, jadi
tak ada yang perlu disinkronkan.

Aturannya sederhana: **ada baris baru di tabel S2 → proyek lama perlu `--sync`.** Tidak ada → tidak.
