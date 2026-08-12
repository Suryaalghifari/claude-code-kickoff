# claude-kickoff

Skill `/kickoff` untuk Claude Code: **menyiapkan sistem konteks proyek baru** — dokumen yang tepat,
aturan yang ditegakkan, dan tempat menyimpan keputusan, supaya agen AI tidak kemana-mana di tengah
jalan.

Bukan generator boilerplate. Intinya **wawancara**: arah proyek ditemukan dulu lewat tanya-jawab
dan revisi, baru artefaknya dihasilkan.

---

> **Claude Code saja.** Lapis penegakannya — hooks, `/work`, `/verify` — memakai mekanisme khas
> Claude Code dan tak punya padanan di agen lain. Metodologinya sendiri (`skill/references/`,
> ±1.200 baris markdown) netral dan bisa dibaca agen mana pun, tapi tanpa penegakan ia kembali
> jadi himbauan. Menyebutnya lintas-platform berarti menjanjikan sesuatu yang tak dikirim.

## Pasang

```bash
cd ~/Projects/claude-kickoff
chmod +x install.sh
./install.sh              # menyalin skill/ → ~/.claude/skills/kickoff/
./install.sh --uninstall  # melepas
```

Versi lama otomatis dicadangkan (`.bak.<timestamp>`), tak pernah ditimpa diam-diam.

## Pakai

```bash
mkdir ~/Projects/proyek-baru && cd ~/Projects/proyek-baru
claude
```

lalu ketik:

```
/kickoff              # proyek baru (folder boleh kosong)
/kickoff --resume     # lanjutkan wawancara yang tertunda
/kickoff --audit      # proyek sudah jalan, BELUM punya sistem konteks
/kickoff --sync       # proyek SUDAH punya, tapi lahir dari skill versi lama
```

Setelah kickoff, proyek dapat dua perintah sendiri:

```
/work <deskripsi>     # mulai satu pekerjaan — tambah atau revisi fitur
/verify               # jalankan Definition of Done lengkap + verifikasi alur nyata
```

---

## Cara kerjanya

Lima fase. **Tidak ada berkas yang ditulis sebelum Fase 3** — ini disengaja.

| Fase | Yang terjadi | Keluaran |
|---|---|---|
| **1 · Wawancara** | 4 ronde tanya-jawab, berputar sampai konvergen | Ringkasan 3 kalimat + daftar "mahal kalau salah" |
| **2 · Kunci** | Keputusan dikunci, doc set dipilih lewat rubrik | Daftar dokumen — ditunjukkan sebelum dibuat |
| **3 · Hasilkan** | Berkas dibuat & diisi dari hasil wawancara | `CLAUDE.md`, `docs/`, `SYSTEMMAP`, `decisions/`, `.claude/settings.json` |
| **4 · Verifikasi** | Cek batas 200 baris, nol placeholder, routing sinkron | Laporan + saran perintah commit |
| **5 · Serah terima** | Menjelaskan kebiasaan yang bikin sistem ini hidup | — |

### Empat ronde wawancara

1. **Apa yang dibangun** — untuk siapa, dan **apa tanda proyek ini selesai**
2. **Apa yang mahal kalau salah** — ronde paling menentukan; jawabannya langsung jadi doc set
3. **Keputusan terkunci** — stack & pilihan besar, tiap baris wajib punya alasan
4. **Cara kerja** — git, bahasa, gaya komentar, dan perintah Definition of Done

### Yang dihasilkan

```
CLAUDE.md                    router + keputusan terkunci + aturan (maks 200 baris)
docs/
├── README.md                index + konvensi dokumen
├── <NN>-*.md                hanya yang lolos rubrik "mahal diubah"
├── SYSTEMMAP.md             status saja — tanpa penalaran
├── SYSTEMMAP-LOG.md         riwayat & post-mortem, append-only
└── decisions/               keputusan skala-fitur, ditulis SEBELUM dikerjakan
.claude/
├── settings.json            allowlist izin + deny git + hooks
├── commands/verify.md       /verify — DoD dijalankan, bukan diingat
└── hooks/
    ├── session-start.py     suntik §Fokus + §Utang tiap awal sesi
    ├── secret-scan.py       tolak menulis rahasia ke berkas (blokir, exit 2)
    └── destructive-guard.py tolak perintah perusak data (blokir, exit 2)
.gitignore · .graphifyignore
```

## Kerja sehari-hari: `/work`

Setup dan verifikasi saja tak cukup — yang menentukan justru **hari kerja biasa**. Lima langkah,
dan langkah 2 yang paling sering dilewat:

1. **Orientasi** — cek `SYSTEMMAP`; belum ada di peta? tambahkan sebagai 🟨
2. **Gali** — `grep -i "<modul>" docs/SYSTEMMAP-LOG.md docs/decisions/*.md` **sebelum menyentuh
   kode lama**
3. **Putuskan** — mengubah arah / berhari-hari → tulis `docs/decisions/00X` dulu
4. **Kerjakan** — ikuti konvensi & pola sekitar; jangan melebar dari yang diminta
5. **Tutup** — `/verify` → protokol SYSTEMMAP → sarankan branch & commit

**Kenapa langkah 2 genting:** kode yang terlihat aneh sering aneh *karena alasan*. Pada proyek
rujukan, sebuah fitur analytics memakai `fetch keepalive` alih-alih `sendBeacon` yang lebih ringkas.
Tanpa membaca LOG, "merapikannya" balik ke `sendBeacon` terasa seperti perbaikan — padahal itu
persis bug yang dulu membuat fitur rusak diam-diam **15 hari**.

|  | Menambah fitur | Merevisi fitur |
|---|---|---|
| Langkah 2 | opsional | **wajib** — ini inti pekerjaannya |
| Risiko utama | salah bentuk sejak awal | **regresi** |
| Bukti verifikasi | alur baru jalan | alur baru jalan **dan yang lama tak rusak** |

> Di proyek yang baru di-`--audit`, LOG masih kosong — riwayat git jadi penggantinya
> (`git log --oneline -- <berkas>`, `git log -S '<potongan>'`) sampai entri mulai terkumpul.

## Peta kode graphify (opsional)

Kalau proyek memakainya, skill memasang alurnya di tiga titik:

| Kapan | Yang terjadi |
|---|---|
| **Kickoff / audit** | `.graphifyignore` dipasang, `graphify-out/` di-gitignore, graf dibangun **`--code-only`** |
| **`/verify` lapis 6** | `graphify update .` setelah lima lapis hijau — AST-only, ±13 detik pada monorepo 3 aplikasi |
| **`--audit` §A1** | Graf lama diperiksa; kalau tercampur → **rebuild**, bukan update |

**Kenapa `--code-only` wajib.** Diukur pada satu proyek nyata: dari 8.185 edge, hanya **3** yang
menyeberang dari node dokumen ke node kode. Sisi dokumen jadi pulau terpisah — ratusan node yang
mengencerkan hasil query, dan bisa terpilih jadi titik awal penelusuran sehingga query berangkat
dari wilayah yang salah. Navigasi dokumen sudah ditangani tabel routing `CLAUDE.md`.

> `graphify update` **tidak** membersihkan graf yang terlanjur tercampur — ia hanya me-re-extract
> berkas kode. Membersihkannya menuntut `rm -rf graphify-out/` lalu `graphify . --code-only`.

## Untuk proyek yang sudah jalan

`--audit` bukan "Fase 1–4 minus generate" — alurnya memang berbeda. Arah proyek sudah tertulis di
kode, jadi ia **dibaca dan dikonfirmasi**, bukan diwawancarai:

inventaris → turunkan keputusan dari manifest/CI/migrasi → **gali kandidat aturan dari `git log`** →
backfill SYSTEMMAP → laporkan celah → kerjakan hanya yang disetujui.

**Keuntungan yang tak dimiliki proyek baru:** riwayat git sudah memuat mode kegagalannya. Klaster
commit `fix` per skop menghasilkan kandidat aturan #9+ sejak hari pertama, tanpa menunggu gagal dua
kali.

```bash
git log --format=%s | grep -E '^fix' | sed -E 's/^fix\(([^)]*)\).*/\1/' | sort | uniq -c | sort -rn
```

Tervalidasi pada proyek rujukan: tiga klaster teratas — `admin` (8×), `media` (7×), `security` (6×) —
**persis sama** dengan tiga aturan yang ditulis tangan pemiliknya setelah berbulan-bulan. Riwayat
sudah memuat aturannya sebelum siapa pun menuliskannya.

> Aturan mutlak mode ini: **jangan timpa apa pun.** Berkas yang sudah ada hanya diubah setelah
> perubahannya ditunjukkan dan disetujui, satu per satu.

## Kalau skillnya sendiri berubah: `--sync`

Proyek hasil `/kickoff` memegang **salinan** `templates/`. Memperbaiki skill lalu `./install.sh`
**tidak** menyentuh salinan itu — jadi proyek lama tetap membaca aturan yang sudah dicabut, tiap
sesi, tanpa ada yang menyadarinya. Gejalanya khas: *"aturannya sudah saya perbaiki, tapi kok masih
dilanggar terus."*

`--sync` bekerja dari **tabel penanda aturan mati** (`references/sync.md` §S2) — bukan mendiff
seluruh berkas. Tiap aturan yang dicabut mewariskan satu penanda yang bisa di-`grep` di proyek
lama, beserta berkas mana yang harus disunting.

| | `--audit` | `--sync` |
|---|---|---|
| Untuk | belum punya sistem konteks | sudah punya, tapi versi lama |
| Membaca | kode proyek | artefak generate vs templat sekarang |

> Batas terpentingnya: **`--sync` tidak menyentuh kode.** Aturan komentar yang berubah tidak berarti
> membersihkan komentar lama secara massal — aturan baru berlaku untuk yang ditulis sesudahnya.

## Melawan pembusukan

Sistem konteks tak rusak mendadak; ia menggemuk sampai tak ada yang membacanya. Ambang di
`references/maintenance.md` — semuanya diturunkan dari pengukuran nyata, bukan angka karangan:

| Gejala | Ambang | Tindakan |
|---|---|---|
| `CLAUDE.md` menggemuk | 200 baris | badan aturan → dokumen |
| Satu aturan jadi mini-dokumen | **3 baris** | perintah + tautan saja |
| Dokumen menampung 2 topik | 400 baris | pecah |
| LOG tak terkelola | ~40 entri | arsip per kuartal |
| Dokumen tanpa pemicu | 0 rujukan | masuk router, atau hapus |

Pagar **3 baris per aturan** lahir dari pengukuran ini: pada proyek rujukan, 3 dari 10 aturan
memakan **71% blok aturan**, dan 26 baris di antaranya ternyata *salinan* isi dokumen yang sudah
ditautkan di aturan itu sendiri. Aturan #1–#7 yang rata-rata 1,9 baris justru yang paling tak pernah
salah dipatuhi. Panjang bukan ketegasan.

Perawatan paling menguntungkan: **tiap aturan yang bisa dicek mesin → naikkan jadi hook, lalu hapus
dari `CLAUDE.md`.** Router ikut ramping dan penegakannya justru menguat.

---

## Tiga prinsip yang menyangga semuanya

**1. `CLAUDE.md` itu router, bukan gudang.**
Dokumen yang selalu dimuat harus kecil; sisanya dipanggil saat dibutuhkan lewat tabel *"kalau
tugasnya X, baca Y"*. Pada proyek rujukan: 11 KB selalu dimuat, 646 KB on-demand. Kalau semuanya
ikut tiap sesi, jendela konteks habis sebelum satu baris kode dibaca.

**2. Dokumen dibuat untuk yang mahal diubah.**
Dari data proyek rujukan — konvensi koding **100%** bertahan, skema data **88%**, design system
**90%**; sementara spesifikasi API cuma **40%** (60% ditulis ulang sambil ngoding). Yang bertahan
adalah yang mahal diubah. Menulis spesifikasi endpoint lengkap di hari pertama = mengarang.

**3. Aturan lahir dari kegagalan, bukan antisipasi.**
Aturan bernomor 9 ke atas **sengaja kosong**. Di proyek rujukan, tiga aturan yang paling banyak
menyelamatkan pekerjaan tak satu pun ada di dokumen awal — semuanya masuk pada hari ke-2 dan ke-5,
setelah gagal. Di hari pertama kamu belum tahu mode kegagalanmu sendiri.

> **Kebiasaan yang bikin sistem ini hidup:** kesalahan yang sama terjadi **dua kali** → jadikan
> aturan bernomor di `CLAUDE.md`. Sekali itu kecelakaan; dua kali itu pola.

---

## Tiga berkas, tiga umur informasi

Kerancuan terbesar sistem semacam ini muncul saat ketiganya dicampur — biasanya `SYSTEMMAP.md`
membengkak karena penalaran tak punya rumah lain.

| Berkas | Umur | Isi | Uji cepat |
|---|---|---|---|
| `SYSTEMMAP.md` | berubah tiap hari | tabel status | *"berubah minggu depan?"* |
| `decisions/*.md` | beku setelah diputuskan | kenapa ini, kenapa bukan yang lain | *"akan ditanya 'kenapa dulu begitu' 6 bulan lagi?"* |
| `SYSTEMMAP-LOG.md` | append-only | apa yang terjadi & apa yang sempat salah | *"sudah terjadi dan tak akan berubah?"* |

`decisions/` ditulis **sebelum** mengerjakan; `SYSTEMMAP-LOG.md` **sesudah**.

---

## Konvensi koding — berlapis, tidak seragam

Konvensi yang sama tak cocok untuk skrip 80 baris dan platform 3 aplikasi. Yang **kurang** bikin
kode berantakan; yang **berlebih** bikin proyek kecil mati sebelum jalan — dan itu mode kegagalan
yang lebih sering, karena terasa seperti profesionalisme.

Skill menilai tingkatnya sendiri dari empat sinyal yang **sudah** terkumpul di Ronde 1 & 2 (umur
proyek · jumlah pembaca · jumlah bagian · taruhan data), lalu menyampaikan hasil penilaiannya untuk
dikoreksi. User tak perlu menilai kompleksitas proyeknya sendiri.

| Tingkat | Yang dipasang |
|---|---|
| **Ringan** | Lapis 0 — nama = dokumentasi · satu konsep satu nama · komentar & docblock default nol · fungsi kecil & early return · error eksplisit · tanpa hardcode |
| **Sedang** | + Lapis 1 — formatter & linter otomatis · DRY rule-of-three · penamaan formal · type everything |
| **Berat** | + Lapis 2 — struktur berlapis · validasi terpisah · Resource/DTO · enum status · SOLID · gate CI |

Aturan **spesifik-stack** (Laravel, Nuxt, Go, apa pun) **dihasilkan dari stack yang dipilih**, bukan
disalin — yang dibawa cuma bentuknya: standar dasar, larangan konkret yang bisa diperiksa, dan satu
contoh kode pendek.

> Ragu antara dua tingkat → **ambil yang lebih rendah.** Menaikkan konvensi belakangan itu murah;
> menurunkan berarti membongkar abstraksi yang terlanjur menyebar.

Detail: [`skill/references/conventions.md`](skill/references/conventions.md).

## Aturan git

Yang **inti** dipasang di tiap proyek: git dijalankan user (bukan AI) · Conventional Commits ·
`tipe/deskripsi-kebab-case` · satu fitur = satu branch = satu PR · stage selektif (bukan
`git add .`) · dokumen ikut dalam PR fiturnya · jangan commit secret.

Yang **bergantung skala** ditanyakan saat wawancara: lapisan branch (`main` saja ·
`main → production` · `main → test → production`), dan apakah rilis bertahap per-PR — sebab
jawabannya menentukan **merge commit vs squash**.

Detail lengkap: [`skill/references/git.md`](skill/references/git.md).

---

## Struktur repo ini

```
skill/
├── SKILL.md                  instruksi utama — 5 fase + 6 pagar
├── references/
│   ├── interview.md          4 ronde pertanyaan + kriteria konvergen
│   ├── doc-rubric.md         rubrik "mahal diubah" → doc set
│   ├── conventions.md        penilai kompleksitas + konvensi berlapis
│   ├── git.md                aturan git: inti + bergantung skala
│   ├── protocol.md           SYSTEMMAP / decisions / LOG
│   ├── rules.md              pagar 3 baris + aturan-dari-kegagalan + DoD
│   ├── workflow.md           alur satu pekerjaan; tambah vs revisi
│   ├── verify.md             lima lapis verifikasi + blok bukti
│   ├── audit.md              alur proyek existing tanpa sistem konteks
│   ├── sync.md               menyamakan proyek lama dengan templat sekarang
│   └── maintenance.md        ambang pembusukan, rotasi LOG, hook
└── templates/                rangka berkas + hooks yang disalin ke proyek
install.sh
```

Mengubah skill = edit di `skill/`, lalu `./install.sh` lagi.

## Lisensi

[MIT](LICENSE). Pakai, ubah, sebarkan — metodologi hanya berguna kalau boleh dipakai.

## Catatan

- Semua perintah git di repo ini **dijalankan user, bukan AI** — sama seperti aturan yang dipasang
  skill ini ke proyek yang dilayaninya.
- Angka & contoh yang dikutip di sini berasal dari satu proyek nyata (369 commit, 15 dokumen,
  ~1 bulan). Bukan angka industri — perlakukan sebagai satu titik data, bukan hukum.
