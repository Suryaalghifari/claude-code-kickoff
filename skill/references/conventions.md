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
- **Satu konsep = satu nama, di seluruh repo.** Sinonim lebih merusak daripada nama jelek: nama
  jelek yang konsisten tetap bisa di-`grep`; dua nama untuk satu benda membuat pencarian
  mengembalikan **separuh** hasil, dan yang mencari tak pernah tahu ada separuh lagi.
- **Komentar: default NOL.** Ia pengecualian yang harus dibenarkan, bukan kelengkapan berkas.
  Uji tunggalnya di bawah — berlaku untuk `//` **maupun** docblock.
- **Fungsi kecil & fokus.** Idealnya < 20 baris, satu tingkat abstraksi. Maks ~3–4 parameter.
  **Early return** daripada nested if.
- **Error handling eksplisit.** Jangan telan error diam-diam (`catch {}` kosong). Validasi di
  batas input — fail fast.
- **Konfigurasi via env/config, bukan hardcode** (URL, limit, flag, kredensial).
- **Tidak ada dead code / kode ter-komentar.** Git sudah menyimpan riwayat.
- **TODO berformat:** `// TODO: <apa> (<konteks/kapan>)`

### Saat bahasanya campur

Keputusan bahasa (Ronde 4) menentukan **bahasa mana** yang dipakai — ia **tidak** dengan sendirinya
mencegah satu konsep punya dua nama. Justru proyek yang sengaja memakai istilah domain lokal paling
rawan: istilah Inggris ikut masuk lewat nama framework, dan keduanya hidup berdampingan.

Bentuk nyata di proyek rujukan — istilah domain dikunci berbahasa Indonesia, tapi satu konsep tetap
lahir dua kali:

```
MovementController · MovementSyncController · ResolveMovement     ← satu sisi
CetakBuktiMutasi                                                  ← sisi lain
```

*Movement* dan *mutasi* benda yang sama. Rekan tim yang mencari `mutasi` kehilangan tiga berkas;
yang mencari `movement` kehilangan satu — dan tak ada yang memberi tahu bahwa hasilnya tak lengkap.

Pagar yang bekerja: **untuk tiap konsep domain, pilih satu istilah dan pakai di seluruh lapis** —
kolom DB, model, controller, endpoint, komponen UI. Kalau istilah lokal yang dipilih, nama teknis
framework boleh tetap Inggris (`Controller`, `Request`, `Resource`) — yang tak boleh adalah
**kata bendanya** ikut berganti bahasa.

Bisa diperiksa, dan murah: `grep -ric "<istilah-a>\|<istilah-b>" <src>` — dua-duanya keluar dengan
jumlah berarti? Itu duplikasi konsep, bukan gaya.

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

### Uji tunggal sebelum menulis komentar

> **Tanpa komentar ini, apakah engineer kompeten akan "merapikan" baris ini dan merusaknya?**

Tidak → **jangan tulis**; perbaiki nama atau strukturnya. Uji ini menggantikan seluruh daftar
"kapan boleh berkomentar", dan penggantian itu disengaja: **daftar berkategori dibaca sebagai
menu.** Versi sebelumnya berisi sepuluh izin lawan tiga larangan, dengan satu kategori
("menjelaskan kenapa harus begini") yang bisa dijawab *ya* untuk baris apa pun — satu baris itu
menetralkan sembilan lainnya, dan saringannya berhenti menyaring.

Komentar yang lolos uji ini selalu spesifik dan menyebut akibat:

```js
❌ // Kirim data analytics ke server
✅ // fetch keepalive, bukan sendBeacon: sendBeacon dibuang diam-diam saat tab ditutup.
```

**Tiga larangan tanpa pengecualian:**

1. **Menerjemahkan kode.** Termasuk penanda obvious (`// constructor`) dan komentar usang — yang
   terakhir lebih buruk daripada tanpa komentar.
2. **Merujuk ke mana pun** — lihat bagian di atas.
3. **Header berkas yang meringkas isinya** — lihat di bawah.

### Docblock tunduk pada uji yang sama

Titik buta paling mahal: semua larangan di atas terbaca sebagai aturan untuk `//`, sehingga
**docblock lolos dari semuanya** dan dihasilkan sebagai kelengkapan berkas.

Diukur pada proyek rujukan (123 berkas kode aplikasi, 8.377 baris): komentar totalnya **10,2%** —
wajar. Tapi **34% di antaranya docblock**, dan pada 10 berkas terpadat docblock mencapai **65%**
dari seluruh komentar. Sepuluh berkas itu semuanya **di bawah 40 baris**. Sebabnya: header adalah
**ongkos tetap** ±13 baris tak peduli berkasnya 21 baris atau 400 — jadi rasionya meledak justru
di berkas terkecil, dan di situlah ia paling tak berguna.

Bentuknya khas — komponen 21 baris dibuka 13 baris header yang mendaftar tiap `variant → kelas
CSS`, padahal pemetaan itu ada 10 baris di bawahnya:

```
❌ /**                              ❌ /**
    * BaseBadge — badge dgn variant.     * Komposisi:
    * variant:                           * - Sidebar kiri (collapsible)
    *   success → bg-success             * - Header sticky atas
    *   warning → bg-warning             * - Footer bawah
    */                                   */
   (pemetaan yang sama, 10 baris        (isi <template> yang sama,
    di bawahnya)                         20 baris di bawahnya)
```

Keduanya **salinan kedua dari kode di berkas yang sama** — dan berlaku hukum yang sama dengan
perintah kembar di `CLAUDE.md`: dua salinan pasti berbeda suatu hari, dan yang basi selalu yang
lebih mudah dibaca. Ubah satu kelas CSS, header itu langsung berbohong tanpa satu pun test gagal.

**Docblock dibenarkan hanya untuk yang tak terbaca dari signature:** satuan (`ms`? `detik`?) ·
efek samping · invarian pemanggilan ("harus dipanggil setelah X") · jebakan perilaku framework.

Yang **tidak** pernah dibenarkan: meringkas isi berkas · mendaftar ulang props/varian/komposisi ·
mengulang nama berkas · `@param`/`@return` yang cuma menyalin tipe yang sudah tertulis.

> Satu berkas boleh punya dua-duanya: header upacara **dan** satu kalimat yang benar-benar layak.
> Pada proyek rujukan ditemukan header 13 baris yang 11 barisnya menyalin `<template>`, sementara
> 2 baris terakhirnya menjelaskan perilaku auto-unwrap framework yang memang tak terbaca dari
> kode. **Buang 11, simpan 2.** Jangan buang seluruh bloknya, dan jangan pertahankan seluruhnya.

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

1. **Komentar default NOL.** Tulis hanya kalau tanpanya orang akan "merapikan" baris itu lalu
   merusaknya. **Docblock tunduk uji yang sama** — jangan buka berkas dengan ringkasan isinya.
2. **Satu konsep = satu nama** di seluruh lapis, termasuk saat bahasanya campur.
3. **DRY** (rule of three), tapi jangan over-abstract.
4. **Fungsi kecil, early return, ≤3–4 parameter.**
5. **Type everything.**
6. **Konsistensi > kepintaran.** Konfigurasi, bukan hardcode.
7. **Automasi menjaga standar** — bukan disiplin manual.
8. *(Lapis 2)* **Single Responsibility.** Handler tipis → Service → Repository/Model.
