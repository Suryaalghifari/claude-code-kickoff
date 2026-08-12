# Mode `--audit` — Proyek yang Sudah Jalan

Di proyek baru arah **ditemukan lewat wawancara**. Di proyek existing arah **sudah tertulis di
kode** — tugasmu membacanya, mengonfirmasi, lalu menambal yang kurang.

> **Aturan mutlak: JANGAN timpa apa pun.** Berkas yang sudah ada hanya boleh diubah setelah
> perubahannya ditunjukkan dan disetujui, satu per satu. Repo ini punya riwayat yang tak kamu
> saksikan; asumsi bahwa sesuatu "salah" hampir selalu salah.

---

## A1 — Inventaris (baca, jangan tulis)

Kumpulkan dulu, jangan menyimpulkan:

```bash
ls -la                                  # CLAUDE.md? docs/? .claude/?
find docs -name '*.md' | head -30
wc -l CLAUDE.md docs/*.md 2>/dev/null
git log --oneline | wc -l               # umur & intensitas
git log --format=%s | sed -E 's/^([a-z]+).*/\1/' | sort | uniq -c | sort -rn
```

Yang dicari: apa yang **sudah ada dan bekerja** — bukan apa yang kurang. Yang kurang datang nanti.

### Peta kode graphify — periksa sehat atau tercampur

Kalau `graphify-out/` ada, jangan langsung dipercaya. Periksa komposisinya:

```bash
python3 -c "
import json,collections
n=json.load(open('graphify-out/graph.json'))['nodes']
c=collections.Counter(x.get('file_type','?') for x in n)
print(dict(c))
print('TERCAMPUR → rebuild --code-only' if c.get('document') else 'code-only → cukup update')
"
du -sh graphify-out/*/ 2>/dev/null   # snapshot bertanggal = duplikat, aman dibuang
```

**Kenapa ini penting.** Graf yang ikut mengindeks dokumen terlihat lebih kaya, padahal tidak.
Diukur pada satu proyek nyata: dari 8.185 edge, hanya **3** yang menyeberang dari node dokumen ke
node kode. Sisi dokumen jadi **pulau terpisah** — ratusan node yang mengencerkan hasil query tanpa
pernah menghubungkanmu ke satu baris kode pun. Lebih buruk lagi, node dokumen bisa terpilih jadi
**titik awal penelusuran**, sehingga query berangkat dari wilayah yang salah sejak langkah pertama.

Navigasi dokumen sudah ditangani tabel routing `CLAUDE.md` — index buatan manusia yang lebih akurat
daripada community detection.

**Kalau tercampur, usulkan (jangan langsung jalankan):**

```bash
printf 'docs/\n*.md\nTemplate/\nvendor/\nnode_modules/\n' >> .graphifyignore
rm -rf graphify-out/            # buang graf lama + snapshot bertanggal sekaligus
graphify . --code-only          # bangun ulang bersih
```

> **`graphify update` TIDAK cukup di sini.** Ia hanya me-re-extract berkas kode; node dokumen yang
> terlanjur masuk tetap tinggal. Membersihkannya menuntut **rebuild**.

Pastikan `graphify-out/` masuk `.gitignore` — ia di-generate lokal, bukan kode proyek.

---

## A2 — Turunkan keputusan dari kode

Keputusan terkunci di proyek existing sudah ada, cuma tak tertulis. Baca dari:

| Sumber | Yang terbaca |
|---|---|
| Manifest dependensi (`package.json`, `composer.json`, `go.mod`, …) | framework, runtime, pustaka besar |
| Konfigurasi DB / migrasi | penyimpanan data & bentuknya |
| Berkas auth / middleware | mekanisme autentikasi |
| CI workflow | perintah lint/test/build **nyata** — langsung jadi DoD |
| `.env.example` | layanan eksternal yang dipakai, dan apa yang harus hidup agar ia jalan |

Lalu **konfirmasi, jangan menyimpulkan sendiri**:

> *"Saya lihat proyek ini pakai X untuk Y. Saya catat sebagai keputusan terkunci — alasannya apa,
> dan masih berlaku? Kalau sebenarnya sudah mau diganti, jangan dikunci."*

Yang tak bisa dipastikan → tandai `[BELUM]`. **Jangan menebak alasan.** Alasan karangan lebih
berbahaya daripada kolom kosong, karena ia akan dipercaya enam bulan lagi.

> **Kalau repo pernah punya dokumen yang kini terhapus** (`git log --diff-filter=D -- '*.md'`):
> jangan diam-diam memulihkan isinya. Penghapusan bisa disengaja — dokumen usang yang menyesatkan,
> atau memang dibuang. **Tanyakan dulu**: mau dipakai sebagai bahan, atau diabaikan?

### Realitas deploy — di sini dibaca, bukan ditunda

`doc-rubric.md` melarang menulis dokumen deployment **di depan**, dan itu benar untuk `/kickoff`:
di hari pertama cara deploy masih tebakan. **Larangan itu soal meramal, bukan soal membaca.** Di
proyek yang sudah jalan, cara deploy sudah tertulis — sekelas dengan manifest dan migrasi di tabel
atas. Jangan bawa larangan "tunda" ke mode di mana pembenarannya tidak berlaku.

```bash
ls .github/workflows/ .gitlab-ci.yml Dockerfile* docker-compose* Procfile fly.toml 2>/dev/null
ls deploy* scripts/deploy* Makefile 2>/dev/null
```

| Sumber | Yang terbaca |
|---|---|
| Job **deploy** di CI (berkas yang sama dengan DoD) | ke mana ia naik, dipicu apa, environment apa saja |
| `Dockerfile` / `compose` / `Procfile` | bagaimana ia dijalankan, proses apa saja yang harus hidup |
| Skrip deploy / `Makefile` | langkah rilis nyata, termasuk migrasi |
| Konfigurasi webserver / reverse proxy | pintu masuk trafik, berkas statis, TLS |
| Nama secret di CI (**namanya saja**) | ketergantungan eksternal yang tak terlihat di kode |

> Berkas CI **sudah kamu buka** untuk memanen perintah lint/test/build. Job deploy ada di berkas
> itu juga — memanen separuh lalu membuang sisanya adalah kehilangan yang tak perlu.

Lima pertanyaan yang harus terjawab, dan **berhenti di situ**: di mana ia jalan · bagaimana ia
sampai ke sana · environment apa saja & bedanya · apa yang pertama rusak · bagaimana kembali ke
versi sebelumnya. Ukurannya ikut pola `0X-security.md` — **peta jalan ke produksi, bukan manual
ops.** Yang tumbuh belakangan dari kejadian nyata, bukan ditulis lengkap sekarang.

**Aturan yang mengikat bagian ini:**

- **Turunkan lalu konfirmasi.** Yang tak bisa dipastikan → `[BELUM]`. Berlaku ekstra di sini:
  langkah manual yang hidup di kepala orang **tak akan pernah** muncul di CI, dan justru itu yang
  paling sering jadi penyebab rilis gagal.
- **Isi yang tak terverifikasi lebih buruk daripada tak ada dokumen** — alasannya sama persis
  dengan peta kode basi di §A1: ia terlihat berwibawa. Tandai apa adanya mana yang dibaca dari
  berkas dan mana yang dikonfirmasi user.
- **Jangan menyentuh CI, secret, atau konfigurasi deploy.** Ini membaca, bukan merapikan (lihat
  §Batas yang harus dihormati).

---

## A3 — Gali kandidat aturan dari riwayat git

**Ini keuntungan yang tak dimiliki proyek baru.** Proyek baru harus menunggu gagal dua kali untuk
mendapat aturan #9; proyek existing sudah menyimpan kegagalannya di `git log`.

```bash
# klaster perbaikan per skop — puncaknya = mode kegagalan berulang
git log --format=%s | grep -E '^fix' | sed -E 's/^fix\(([^)]*)\).*/\1/' | sort | uniq -c | sort -rn

# baca isi klaster teratas
git log --format='%s' --grep='^fix(<skop>)'

# berkas yang paling sering diperbaiki = titik rapuh
git log --format= --name-only --diff-filter=M -- '*.php' '*.ts' '*.vue' | sort | uniq -c | sort -rn | head -20
```

**Teknik ini tervalidasi.** Pada proyek rujukan, tiga klaster fix teratas — `admin` (8), `media`
(7), `security` (6) — persis sama dengan tiga aturan yang ditulis tangan oleh pemiliknya setelah
berbulan-bulan. Riwayat sudah memuat aturannya sebelum siapa pun menuliskannya.

**Cara menyodorkan:**

> *"Dari 52 commit fix, tiga tema berulang: media (7×), admin (8×), keamanan (6×). Membaca isinya,
> pola yang terulang tampaknya `<pola konkret>`. Layak jadi aturan #9? Kalimatnya saya usulkan:
> `<usulan yang bisa diperiksa>`."*

**User yang memutuskan.** Klaster bukan bukti — bisa saja itu satu fitur besar yang wajar butuh
banyak perbaikan. Tugasmu menyodorkan pola, bukan memvonis.

---

## A4 — Backfill SYSTEMMAP

Isi status dari keadaan **sekarang**, bukan dari riwayat lengkap:

- Modul/fitur yang sudah jalan → ✅, kolom tanggal `(pra-audit)`, ref boleh kosong
- Yang setengah jadi → 🟨
- Yang direncanakan tapi belum → ⬜

**`SYSTEMMAP-LOG.md` dimulai kosong**, dengan satu entri pertama: `#AUDIT` yang mencatat kondisi
awal. Jangan merekonstruksi 200 commit jadi entri log — itu fiksi, dan tak ada yang membacanya.
Log mulai jujur dari hari ini.

Utang terbuka: gali dari `TODO`/`FIXME` di kode dan issue yang menganggur.

```bash
grep -rn "TODO\|FIXME" --include='*.php' --include='*.ts' --include='*.vue' . | head -30
```

---

## A5 — Laporkan celah, kerjakan yang disetujui

Sajikan sebagai tabel, terurut dampak:

| Aspek | Kondisi | Usulan |
|---|---|---|
| `CLAUDE.md` | tak ada / 340 baris | buat / rampingkan ke ≤200 |
| Status pekerjaan | tersebar di issue | buat `SYSTEMMAP.md` |
| Keputusan besar | tak terekam | buat `docs/decisions/` |
| Aturan dari kegagalan | 3 klaster fix belum jadi aturan | usulkan #9–#11 |
| DoD | ada di CI, tak ada di `CLAUDE.md` | salin perintah nyatanya |
| **Cara deploy** | **hidup di CI/Dockerfile, tak terekam** | **`0X-deployment.md` — lima pertanyaan §A2** |
| **Arsitektur** | **hanya terbaca dari kode** | **`0X-architecture.md` ringkas; kesimpulannya naik ke `CLAUDE.md`** |
| Dokumen tanpa pemicu | `docs/x.md` nol rujukan | masukkan router atau hapus |
| Peta graphify tercampur | ada node `document` | rebuild `--code-only` + `.graphifyignore` (§A1) |

Lalu **tanyakan mau dikerjakan yang mana**, dan kerjakan hanya itu. Jangan borong.

---

## Yang paling sering ditemukan

1. **`CLAUDE.md` jadi gudang** — semua ditumpuk sampai jendela konteks terbebani. Solusi: ubah jadi
   router, badan aturan pindah ke dokumen.
2. **Status hidup di kepala orang.** Tak ada satu tempat pun yang menjawab "sudah sampai mana".
3. **Keputusan besar tak terekam** — kenapa X bukan Y sudah hilang, dan tiap beberapa bulan
   diperdebatkan ulang.
4. **DoD ada di CI tapi tidak di `CLAUDE.md`** — jadi agen tak tahu syarat "selesai", dan menandai
   pekerjaan beres saat kelihatan jalan.
5. **Dokumen bagus yang tak pernah dibuka** karena tak ada baris pemicunya di router.

## Batas yang harus dihormati

- Jangan merapikan kode. Audit ini soal **sistem konteks**, bukan refactor.
- Jangan mengubah CI, dependensi, atau konfigurasi yang sudah jalan.
- Jangan menghapus dokumen. Usulkan; user yang membuang.
- Kalau proyeknya ternyata sudah punya sistem yang lebih baik dari template ini — **katakan**, dan
  jangan ganti. Template ini titik awal, bukan standar.
