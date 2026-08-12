# Konvensi Koding — Berlapis Menurut Kompleksitas

Konvensi yang sama tak cocok untuk skrip 80 baris dan platform 3 aplikasi. Yang **kurang** bikin
kode berantakan; yang **berlebih** bikin proyek kecil mati sebelum jalan — dan itu mode kegagalan
yang lebih sering, karena terasa seperti profesionalisme.

Nilai dulu tingkatnya, baru pasang lapisannya.

---

## Menilai kompleksitas

**Jangan tanya user "ini kompleks atau tidak"** — ia tak punya kewajiban tahu. Skor sendiri dari
jawaban Ronde 1 & 2 yang sudah kamu kumpulkan:

| Sinyal | 0 | 1 | 2 |
|---|---|---|---|
| **Umur** — sekali jalan atau dirawat? | sekali pakai | beberapa bulan | bertahun |
| **Pembaca** — siapa yang membaca kodenya? | saya sendiri | saya + AI | ada orang lain |
| **Bagian** — berapa bagian yang saling bicara? | satu berkas/skrip | satu aplikasi | banyak app/service |
| **Taruhan** — ada data persisten / konsumen luar? | tidak | data lokal saja | data nyata / API dipakai pihak lain |

| Total | Tingkat | Pasang |
|---|---|---|
| 0–2 | **Ringan** | Lapis 0 |
| 3–5 | **Sedang** | Lapis 0 + 1 |
| 6–8 | **Berat** | Lapis 0 + 1 + 2 |

**Sampaikan hasilnya, jangan diam-diam.** Contoh:
*"Saya nilai ini Sedang (dirawat berbulan, ada data persisten, satu aplikasi) — jadi konvensinya
sampai Lapis 1: prinsip inti + formatter/linter otomatis + penamaan formal. Struktur berlapis dan
DTO saya lewati dulu; kalau nanti bagiannya bertambah, tinggal naik."*

User boleh menimpa. **Pendapatnya menang** — ia tahu rencana yang belum diceritakan.

> Ragu di antara dua tingkat? **Ambil yang lebih rendah.** Menaikkan konvensi belakangan itu
> murah — jalankan formatter sekali, tambahkan aturan. Menurunkan berarti membongkar abstraksi
> yang terlanjur menyebar.

---

## Lapis 0 — Inti (selalu, apa pun proyeknya)

Ini yang membuat kode bisa dibaca sendiri seminggu lagi. Tak ada proyek yang terlalu kecil untuk
ini, dan ongkosnya nol.

- **Nama = dokumentasi.** Nama menjelaskan *maksud*, bukan tipe.
  `$d`/`data2`/`handle()` ❌ → `$publishedAt`/`activeProjects`/`publishProject()` ✅
  Fungsi = kata kerja. Boolean = `is/has/can`. Koleksi = plural.
- **Komentar hanya "WHY" yang non-obvious.** Kalau komentar cuma menerjemahkan kode, hapus —
  perbaiki penamaannya.
  - Dibenarkan: keputusan non-obvious · jebakan ("jangan ubah urutan ini karena…") · aturan bisnis
    tak terlihat · workaround + alasan · regex/algoritma rumit
  - Dilarang: menerjemahkan kode jelas · penanda obvious (`// constructor`) · komentar usang
    (lebih buruk dari tanpa komentar)
- **Fungsi kecil & fokus.** Idealnya < 20 baris, satu tingkat abstraksi. Maks ~3–4 parameter.
  **Early return** daripada nested if.
- **Error handling eksplisit.** Jangan telan error diam-diam (`catch {}` kosong). Validasi di
  batas input — fail fast.
- **Konfigurasi via env/config, bukan hardcode** (URL, limit, flag, kredensial).
- **Tidak ada dead code / kode ter-komentar.** Git sudah menyimpan riwayat.
- **TODO berformat:** `// TODO: <apa> (<konteks/kapan>)`

### Komentar berdiri sendiri — tanpa rujukan

> **Komentar kode TIDAK merujuk ke mana pun.** Tanpa `§9.2`, tanpa `[R-04]`, tanpa
> `Lihat docs/01-data-model.md`, tanpa nomor tiket. Kalau alasannya penting, **tulis alasannya** —
> satu kalimat, di tempat ia berlaku.

```php
❌ // Idempotensi ditegakkan UNIQUE(client_uuid) di DB (§11.1).
❌ // Duplikat jadi 'skipped'. Lihat docs/01-data-model.md#idempotensi.
❌ // SPEC §10.4 — batch maks 100.

✅ // Duplikat client_uuid jadi 'skipped', bukan 500: UNIQUE di DB yang menegakkan,
   // bukan pengecekan aplikasi — jadi kirim ulang batch selalu aman.
✅ // Batch dibatasi 100: klien memecah sendiri, server menegakkan batasnya.
```

Rujukan apa pun punya tiga mode kegagalan yang tak dimiliki kalimat biasa: ia **membusuk
diam-diam** saat dokumen disusun ulang, ia **tak bisa dibaca sendiri** sehingga pembaca harus
membuka berkas lain hanya untuk tahu apakah komentar itu relevan, dan ia **mengunci kode ke satu
dokumen master** yang kalau hilang membuat seluruh komentar menunjuk ruang kosong — sementara
kodenya tetap terlihat seolah terdokumentasi.

Dokumen di `docs/` tetap saling menautkan; itu memang gunanya. Yang tidak boleh adalah kode
menautkan ke dokumen.

### Delapan pertanyaan sebelum menulis komentar

Jalankan berurutan. Berhenti di jawaban pertama yang cocok.

| # | Pertanyaan | Jawaban |
|---|---|---|
| 1 | Bisa dibuat jelas dengan nama variabel/fungsi? | **Jangan komentar** — perbaiki namanya |
| 2 | Bisa dibuat jelas dengan struktur kode? | **Jangan komentar** — perbaiki strukturnya |
| 3 | Ada business rule yang tidak obvious? | **Komentar** |
| 4 | Ada invariant / constraint penting? | **Komentar** |
| 5 | Ada alasan security / concurrency / performance? | **Komentar** |
| 6 | Ada workaround yang berpotensi dianggap bug? | **Komentar** |
| 7 | Cuma menjelaskan "apa yang dilakukan kode"? | **Jangan komentar** |
| 8 | Menjelaskan "kenapa harus seperti ini"? | **Komentar** |

Pertanyaan 1 dan 2 yang paling sering terlewat: sebagian besar komentar yang terasa perlu
sebenarnya penanda bahwa penamaan atau strukturnya yang belum benar.

> **Proyek existing yang sudah terlanjur memakai rujukan** (mode `--audit`): jangan lakukan
> penggantian massal — itu diff besar tanpa perubahan perilaku. Berhenti menambah yang baru, dan
> bersihkan yang lama hanya saat barisnya memang sedang disentuh.

## Lapis 1 — Konsistensi (Sedang ke atas)

Yang mulai berbayar begitu ada pembaca kedua — termasuk kalau pembaca keduanya AI.

- **Formatter + linter otomatis.** Nilai per-usaha tertinggi di seluruh dokumen ini: konsistensi
  dijaga alat, bukan disiplin manual. Pasang sejak hari pertama, bukan setelah berantakan.
- **DRY — rule of three.** Duplikasi *ketiga* baru diekstrak. Jangan over-abstract; abstraksi
  prematur juga masalah.
- **Penamaan formal per bahasa** (class/komponen `PascalCase`, fungsi/variabel `camelCase`,
  konstanta `UPPER_SNAKE`, tabel/kolom `snake_case`).
- **Satu class/komponen per berkas.** Nama berkas = nama isinya.
- **Type everything** sejauh bahasanya mendukung (`strict_types`, TS `strict`, hindari `any`).
- **Kelompokkan by fitur/domain**, bukan semata by tipe.
- Import terurut & bersih (otomatis via linter).

## Lapis 2 — Struktur (Berat saja)

Ini yang bikin proyek kecil mati. Pasang **hanya** kalau ada banyak bagian saling bergantung, data
nyata, atau konsumen eksternal.

- **Struktur berlapis.** Controller/handler **tipis** → Service pegang logic → Repository/Model
  pegang data. Tidak ada query DB di controller.
- **Validasi di objek terpisah** (Form Request / schema), bukan inline di handler.
- **Output lewat Resource/DTO** — bentuk keluaran terkontrol, jangan lempar model mentah.
- **Enum untuk status/tipe**, bukan string bertebaran.
- **SOLID** — terutama Single Responsibility ("butuh kata *dan* untuk menjelaskan fungsi → pecah")
  dan Dependency Inversion (bergantung pada abstraksi, memudahkan test & penggantian).
- **Test kontrak kritikal.** Nama deskriptif: `it_publishes_a_project_and_flushes_public_cache`.
- **Gate otomatis:** pre-commit (lint-staged) + CI wajib hijau sebelum merge.

---

## Bagian spesifik-stack: dihasilkan, bukan disalin

Lapis 0–2 di atas berlaku lintas bahasa. Aturan spesifik stack **ditulis dari stack yang benar-benar
dipilih** di Ronde 3 — jangan menyalin aturan Laravel ke proyek Go.

Bentuk yang dituju (contoh dari proyek rujukan, ambil **polanya** bukan isinya):

- **Standar dasar** — formatter apa, static analysis apa, aturan tipe apa
- **Larangan konkret** — mis. *"tak pernah raw SQL dengan interpolasi string"*, *"`env()` hanya di
  berkas config"*, *"hindari komponen God — maks ~200 baris"*
- **Satu contoh kode pendek** yang menunjukkan bentuk yang benar

Aturan spesifik yang baik selalu **bisa diperiksa**. *"Tulis kode bersih"* bukan aturan.

---

## Automasi — yang menegakkan semuanya

Konvensi ditegakkan alat, bukan ingatan. Isi sesuai stack, lalu **angka perintahnya masuk ke
Definition of Done** (`CLAUDE.md` aturan #8) supaya jadi satu sumber:

| Peran | Kapan jalan | Tingkat |
|---|---|---|
| Formatter | pre-commit + CI | Lapis 1 |
| Linter | pre-commit + CI | Lapis 1 |
| Static analysis / type check | CI | Lapis 2 |
| Runner test | CI, wajib hijau sebelum merge | Lapis 2 |

> Aturan yang bisa ditegakkan alat **jangan** ditulis sebagai prosa di dokumen. Prosa itu himbauan;
> linter itu penegakan. Tulis di dokumen hanya yang tak bisa dicek mesin — terutama gaya komentar
> dan pilihan penamaan.

---

## Ringkasan (untuk ditempel di dokumen proyek)

1. **Nama jelas > komentar.** Komentar hanya untuk "why".
2. **DRY** (rule of three), tapi jangan over-abstract.
3. **Fungsi kecil, early return, ≤3–4 parameter.**
4. **Type everything.**
5. **Konsistensi > kepintaran.** Konfigurasi, bukan hardcode.
6. **Automasi menjaga standar** — bukan disiplin manual.
7. *(Lapis 2)* **Single Responsibility.** Handler tipis → Service → Repository/Model.
