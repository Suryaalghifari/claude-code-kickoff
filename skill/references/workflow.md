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

**Sebelum menulis baris pertama di proyek existing: cari dua tetangga.** Ini menjawab tiga
pertanyaan sekaligus — nulis di mana, bentuknya bagaimana, dan apakah aku melanggar yang sudah ada.

```bash
# 1. di mana barang sejenis tinggal?
ls <dir-yang-menampung-hal-serupa>/
git log --diff-filter=A --name-only --format= | grep -i "<jenis>" | head

# 2. dua implementasi terdekat — tiru bentuknya, bukan isinya
grep -rl "<antarmuka/konsep sejenis>" <src> | head -3
```

Yang ditiru dari tetangga: **letak berkas · penamaan · lapisan yang dilewati · bentuk masukan &
keluaran · cara error ditangani.** Kalau dua tetangga ternyata berbeda satu sama lain, itu **temuan**
— sebutkan ke user, jangan diam-diam pilih salah satu; kamu baru saja menemukan inkonsistensi yang
sudah ada sebelum kamu datang.

> **Menyimpang dari pola tetangga itu keputusan, bukan selera.** Kalau memang harus berbeda,
> alasannya ditulis — komentar "why" untuk simpangan kecil, `decisions/00X` kalau ia menetapkan
> pola baru yang akan diikuti berkas berikutnya. Simpangan tanpa jejak akan dibaca sebagai
> kecerobohan oleh orang berikutnya, lalu "dirapikan" balik.

Konsistensi lebih berharga daripada perbaikan gaya setempat. Pola yang jelek tapi seragam masih bisa
diperbaiki sekali jalan; dua pola yang bersaing harus dibereskan dulu sebelum apa pun bisa berubah.

**Jangan melebar.** Rapikan yang kamu sentuh; jangan merapikan yang tidak diminta. Perbaikan
menyelinap membuat diff jadi sulit ditinjau dan sulit di-rollback.

### 5. Tutup dengan benar

1. **`/verify`** — kelima lapis, termasuk alur nyata
2. Protokol `SYSTEMMAP` 5 langkah: status → entri LOG → utang → kosongkan checkpoint → user commit
3. Sarankan nama branch + pesan commit; **user yang mengeksekusi**

Belum diverifikasi = **🟨**, bukan ✅.

---

## Tiga mode, tiga perintah

| | `/work` tambah | `/revise` ubah | `/fix` bug |
|---|---|---|---|
| Langkah 2 | opsional, sering kosong | **wajib** — ini inti pekerjaannya | **wajib** + `git log -S` cari kapan ia masuk |
| Risiko utama | salah bentuk sejak awal | **regresi** — mengulang bug lama | **menambal gejala, bukan sebab** |
| Sebelum mulai | — | *"apa yang bisa rusak, dan bagaimana membuktikannya tidak?"* | **reproduksi dulu** — belum bisa mengulang gagalnya = belum boleh memperbaiki |
| Bukti verifikasi | alur baru jalan | baru jalan **dan lama tak rusak** | **gagal → perbaiki → lolos**, berurutan |
| Entri LOG | apa yang dibangun | apa yang berubah & **kenapa yang lama tak cukup** | **akar sebabnya apa** |

**Kelima langkahnya identik** — yang berbeda cuma bobot dan bukti. Karena itu `work.md` memuat alur
lengkapnya dan `revise.md`/`fix.md` hanya menyatakan deltanya. Menyalin kelima langkah ke tiga
berkas berarti tiga salinan yang pasti berbeda suatu hari, dan yang basi selalu yang lebih mudah
dibaca.

> **Salah mode itu mahal.** Menggarap revisi lewat `/work` melewati penggalian riwayat — dan itu
> langkah yang mencegah regresi. Ragu antara revisi dan bug? **Ambil `/fix`**: ia menuntut
> reproduksi, dan menuntut bukti lebih banyak tak pernah merugikan.

## Pekerjaan yang terputus di tengah

Sesi bisa berhenti kapan saja — konteks habis, terminal ditutup. Protokol menulis di **akhir**, jadi
tanpa checkpoint seluruh bagian tengah hilang, dan sesi berikutnya melihat 🟨 lalu **mengulang dari
awal**. Sebagian pekerjaan tak bisa diulang: migrasi yang sudah jalan, data yang sudah terbentuk.

Karena itu `SYSTEMMAP.md` punya **§Sedang Berjalan** — diisi saat masuk langkah 4 dan di tiap titik
jeda, dikosongkan di langkah 5. Tiga baris: **sudah beres (jangan diulang) · berikutnya · setengah
jalan.** Hook `SessionStart` memancarkannya di awal sesi berikutnya, dan hanya kalau tak kosong.

Berhenti mendadak → **`/pause`**: menulis checkpoint lalu berhenti. Bukan penutupan — tak ada
`/verify`, tak ada ✅, tak ada entri LOG.

---

## Blok untuk `CLAUDE.md`

Salin ini ke bagian aturan (hitung sebagai satu aturan, tetap patuhi pagar 3 baris per butir):

```markdown
## Alur satu pekerjaan

1. **Orientasi** — cek `SYSTEMMAP`; belum ada di peta? tambahkan sebagai 🟨
2. **Gali** — `grep -i "<modul>" docs/SYSTEMMAP-LOG.md docs/decisions/*.md` **sebelum menyentuh
   kode lama**. Kode yang terlihat aneh sering aneh karena alasan
3. **Putuskan** — mengubah arah / menutup opsi / berhari-hari → tulis `docs/decisions/00X` dulu
4. **Kerjakan** — cari **2 tetangga sejenis** dulu, tiru letak & bentuknya; menyimpang dari pola
   mereka = tulis alasannya. Isi §Sedang Berjalan. Jangan melebar dari yang diminta
5. **Tutup** — `/verify` → protokol SYSTEMMAP → kosongkan §Sedang Berjalan → sarankan branch &
   commit (user yang eksekusi)

Perintahnya: **`/work`** tambah · **`/revise`** ubah yang ada · **`/fix`** bug (reproduksi dulu) ·
**`/pause`** simpan keadaan lalu berhenti.
```
