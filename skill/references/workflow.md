# Alur Satu Pekerjaan — Menambah & Merevisi Fitur

Bagian yang paling sering hilang dari sistem konteks: yang mengatur **hari kerja biasa**. Setup ada,
verifikasi ada, tapi di antaranya agen bekerja tanpa panduan — dan di situlah pengetahuan yang sudah
susah payah dikumpulkan diabaikan.

Alur ini masuk ke `CLAUDE.md` sebagai blok pendek (selalu dimuat, jadi selalu berlaku) dan
detailnya jadi `/work`.

---

## Lima langkah

### 1. Orientasi — di mana ini di peta

`SYSTEMMAP.md`: item ini sudah ada? statusnya apa? ada dependensi yang belum beres? Kalau belum ada
di peta, **tambahkan barisnya dulu** sebagai 🟨 — pekerjaan yang tak ada di peta selalu jadi
pekerjaan yang lupa dicatat.

### 2. Gali yang sudah diketahui — **langkah paling sering dilewat**

Sebelum menyentuh kode yang sudah ada:

```bash
grep -i "<modul/fitur>" docs/SYSTEMMAP-LOG.md docs/decisions/*.md
```

Yang dicari:

| Ketemu | Artinya |
|---|---|
| Entri LOG menyebut bagian ini | Pernah ada yang salah di sini. **Baca bagian "Yang sempat salah"** sebelum mengubah apa pun |
| Berkas `decisions/` | Bentuknya sekarang adalah hasil keputusan sadar, bukan kebetulan. Jangan dibongkar tanpa membaca alasannya |
| Komentar "why" di kode sekitar | Jebakan yang sudah pernah ditemukan orang lain |

**Kenapa ini genting:** kode yang terlihat aneh sering kali aneh *karena alasan*. Contoh nyata —
sebuah fitur analytics memakai `fetch keepalive` alih-alih `sendBeacon` yang lebih ringkas. Tanpa
membaca LOG, "merapikannya" kembali ke `sendBeacon` terasa seperti perbaikan; padahal itu persis
bug yang dulu membuat fitur rusak diam-diam selama 15 hari.

Tak ketemu apa-apa? Bagus — lanjut. Prosesnya murah, ketinggalannya mahal.

**Di proyek yang baru di-`--audit`, LOG masih kosong** — jadi langkah ini belum berbuah selama
beberapa minggu pertama. Sementara itu, riwayat git jadi penggantinya:

```bash
git log --oneline -- <berkas yang mau diubah>     # kenapa berkas ini sering disentuh
git log -S '<potongan kode mencurigakan>' --oneline # commit yang memperkenalkan/menghapusnya
```

Pesan commit `fix(...)` pada berkas yang sama = peringatan yang sama dengan entri LOG, cuma lebih
pendek. Nilainya bertambah tiap entri LOG baru ditulis; itulah kenapa langkah 5 tidak opsional.

### 3. Putuskan dulu kalau besar

Butuh berkas `decisions/00X` bila pekerjaan ini: **mengubah arah** · **menutup opsi lain** ·
**memakan berhari-hari** · atau **membatalkan keputusan lama**.

Yang terakhir punya aturan sendiri: **jangan sunting berkas keputusan lama.** Buat yang baru, tandai
yang lama `⚠️ DIGANTI oleh 00Y`. Riwayat keputusan harus menunjukkan bahwa pikiranmu berubah, bukan
berpura-pura selalu begini.

Pekerjaan kecil dan jelas → lewati, langsung kerja.

### 4. Kerjakan mengikuti yang sudah ada

Ikuti konvensi proyek **dan pola kode di sekitarnya**. Kalau modul sebelah menyelesaikan masalah
serupa dengan cara tertentu, ikuti — kecuali kamu punya alasan yang layak ditulis sebagai komentar
"why". Konsistensi lebih berharga daripada perbaikan gaya setempat.

**Jangan melebar.** Rapikan yang kamu sentuh; jangan merapikan yang tidak diminta. Perbaikan
menyelinap membuat diff jadi sulit ditinjau dan sulit di-rollback.

### 5. Tutup dengan benar

1. **`/verify`** — kelima lapis, termasuk alur nyata
2. Protokol `SYSTEMMAP` 4 langkah: status → entri LOG → utang → user commit
3. Sarankan nama branch + pesan commit; **user yang mengeksekusi**

Belum diverifikasi = **🟨**, bukan ✅.

---

## Menambah vs merevisi — bedanya nyata

| | Menambah fitur | Merevisi fitur |
|---|---|---|
| Langkah 2 | Opsional, sering kosong | **Wajib.** Ini inti pekerjaannya |
| Risiko utama | Salah bentuk sejak awal | **Regresi** — mengulang bug lama |
| Bukti verifikasi | Alur baru jalan | Alur baru jalan **dan yang lama tak rusak** |
| Entri LOG | Apa yang dibangun | **Apa yang berubah & kenapa yang lama tak cukup** |

Untuk revisi, tambahkan satu pertanyaan sebelum mulai: *"apa yang bisa rusak karena perubahan ini,
dan bagaimana saya membuktikannya tidak rusak?"* Jawabannya masuk ke rencana verifikasi, bukan
diserahkan ke harapan.

---

## Blok untuk `CLAUDE.md`

Salin ini ke bagian aturan (hitung sebagai satu aturan, tetap patuhi pagar 3 baris per butir):

```markdown
## Alur satu pekerjaan

1. **Orientasi** — cek `SYSTEMMAP`; belum ada di peta? tambahkan sebagai 🟨
2. **Gali** — `grep -i "<modul>" docs/SYSTEMMAP-LOG.md docs/decisions/*.md` **sebelum menyentuh
   kode lama**. Kode yang terlihat aneh sering aneh karena alasan
3. **Putuskan** — mengubah arah / menutup opsi / berhari-hari → tulis `docs/decisions/00X` dulu
4. **Kerjakan** — ikuti konvensi & pola kode sekitar. Jangan melebar dari yang diminta
5. **Tutup** — `/verify` → protokol SYSTEMMAP → sarankan branch & commit (user yang eksekusi)
```
