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
| tak ada `.claude/commands/{revise,fix,pause}.md` | tiga mode kerja + checkpoint | salin templatnya; `work.md` jadi pemegang alur, sisanya delta |
| `SYSTEMMAP.md` tanpa `§Sedang Berjalan` | checkpoint pekerjaan terputus | sisipkan section di bawah §Fokus + perbarui `session-start.py` |
| `session-start.py` **tanpa pembuangan komentar HTML** (`<!--`) atau filter `"- "` | alarm palsu permanen | perbaiki filternya — **uji dulu**: §Sedang Berjalan kosong harus menghasilkan **nol** peringatan |
| protokol SYSTEMMAP masih "4 langkah" | jadi 5 — langkah 4 mengosongkan §Sedang Berjalan | `SYSTEMMAP.md` §Protokol Update |

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
- **Divergensi yang disengaja.** Proyek boleh menyimpang dari templat — kadang justru karena
  templatnya yang salah dan proyek menemukannya lebih dulu. Komentar di kode atau entri LOG bisa
  menunjukkan **di mana harus melihat**, tapi tak pernah jadi kesimpulan (lihat di bawah).

> **Bandingkan berkasnya, jangan menyimpulkan dari LOG.** Entri LOG mencatat apa yang benar **saat
> ia ditulis**; berkasnya bisa sudah berubah sejak itu — termasuk oleh `--sync` sebelumnya. Selalu
> `diff` isi nyatanya dulu:
>
> ```bash
> diff .claude/hooks/<nama>.py ~/.claude/skills/kickoff/templates/hooks/<nama>.py
> ```
>
> Identik → **jangan usulkan apa pun**, dan jangan sebut ada divergensi. Kasus nyata: entri LOG
> mencatat divergensi yang sudah lama disamakan, dan `--sync` mengusulkan "adopsi versi templat"
> untuk berkas yang **byte-nya sudah sama persis**. Usulan nol-perubahan bukan sekadar mubazir —
> ia membuat user menyetujui hal yang tak ia butuhkan, dan setelah beberapa kali, membaca laporan
> `--sync` terasa seperti formalitas.

> **Periksa arah perbaikannya sebelum menyamakan.** Kalau proyek sudah memperbaiki hal yang
> templatnya masih bawa, yang basi adalah **templatnya** — laporkan ke user supaya diperbaiki di
> hulu, dan **jangan** timpa versi proyek dengan versi templat yang lebih buruk. `--sync` menyamakan
> ke versi yang benar, bukan ke versi yang lebih baru.

## S4 — Laporkan, lalu BERHENTI

**Sampai titik ini kamu belum boleh menulis apa pun.** S1–S3 seluruhnya membaca. Menulis terjadi di
S5, dan hanya setelah user menjawab.

Sajikan sebagai tabel, dan **tunjukkan diff tiap berkas**:

| Berkas | Yang basi | Usulan | Dampak |
|---|---|---|---|
| `docs/<NN>-conventions.md` | tabel 8 pertanyaan (baris 77) | ganti dengan uji tunggal + bagian docblock | tinggi — ini yang dibaca tiap ngoding |
| `CLAUDE.md` | baris routing `§x.y` | hapus barisnya | tinggi — ia melembagakan praktik yang dilarang |
| `.claude/commands/work.md` | langkah 4 tanpa prosedur | tambahkan cari-dua-tetangga | sedang |

Urutkan **berdasarkan seberapa sering berkasnya dibaca**, bukan panjang diff-nya. `CLAUDE.md` dan
dokumen konvensi dimuat tiap sesi; sisanya hanya saat dipanggil.

**Tiap baris usulan wajib punya perubahan nyata.** Sebelum memasukkannya ke tabel, buktikan
berkasnya memang berbeda — `diff` yang kosong berarti barisnya tidak ada, bukan barisnya "aman".
Tak ada satu pun yang berbeda → laporkan **"tak ada yang perlu disamakan"** dan selesai. Laporan
kosong itu hasil yang sah, dan jauh lebih berguna daripada usulan yang tak mengubah apa pun.

> **Lalu berhenti dan tanyakan mau dikerjakan yang mana.** Jangan borong, dan jangan menulis
> "sambil melapor" — menyajikan tabel **bukan** izin untuk mulai. Sekali satu berkas ditulis
> sebelum dijawab, seluruh laporan kehilangan artinya: user tak lagi bisa membedakan mana yang ia
> setujui dari mana yang sudah terlanjur.
>
> Kasus nyata: `--sync` menulis `session-start.py` lebih dulu, lalu menyajikannya sebagai
> "usulan". Isinya kebetulan benar — tapi user menyetujui sesuatu yang sudah terjadi, dan baru
> ketahuan lewat `git diff`. **Yang menyelamatkannya bukan skill ini, melainkan git.**

## S5 — Kerjakan yang disetujui

Hanya yang dijawab **ya**, satu per satu. Berkas yang jalan **tiap sesi** (`CLAUDE.md`, hooks,
dokumen konvensi) dikonfirmasi sendiri-sendiri — bukan sebagai satu paket.

Setelah selesai, tulis **satu entri** `SYSTEMMAP-LOG.md` bertanda `#SYNC`: apa yang disamakan, apa
yang **sengaja dilewati**, dan apa yang ditolak user. Tanpa entri ini, sinkronisasi berikutnya tak
punya titik awal.

Entri itu mencatat apa yang **benar-benar terjadi**. Kalau sebuah berkas ternyata sudah identik,
tulis "diperiksa, sudah sama" — **jangan** tulis "diadopsi". Entri yang mengklaim perubahan yang
tak pernah terjadi adalah riwayat palsu, dan riwayat palsu lebih buruk daripada tak ada entri.

## Kapan menjalankannya

Setelah `./install.sh` yang membawa perubahan aturan — bukan tiap kali. Perubahan yang hanya
menyentuh `references/` (cara Claude bekerja saat kickoff) tak pernah sampai ke proyek lama, jadi
tak ada yang perlu disinkronkan.

Aturannya sederhana: **ada baris baru di tabel S2 → proyek lama perlu `--sync`.** Tidak ada → tidak.
