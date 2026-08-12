# Protokol SYSTEMMAP · DECISIONS · LOG

Tiga berkas, tiga umur informasi. Rancu terbesar dari sistem semacam ini muncul saat ketiganya
dicampur di satu berkas — biasanya `SYSTEMMAP.md` yang membengkak karena penalaran tak punya
rumah lain.

| Berkas | Umur | Isi | Larangan |
|---|---|---|---|
| `SYSTEMMAP.md` | berubah tiap hari | Tabel status. Itu saja | **Tanpa paragraf penalaran** |
| `docs/decisions/*.md` | beku setelah diputuskan | Kenapa ini, kenapa bukan yang lain | Bukan tempat status |
| `SYSTEMMAP-LOG.md` | append-only | Apa yang terjadi, apa yang sempat salah | Jangan sunting entri lama |

**Uji cepat saat ragu menaruh sesuatu:**

- Berubah minggu depan? → SYSTEMMAP
- Akan ditanya "kenapa dulu begitu?" enam bulan lagi? → decisions
- Sudah terjadi dan tak akan berubah? → LOG

---

## `SYSTEMMAP.md` — status saja

Satu tabel per fase. Kolom: `# · Item · Status · Dependensi · Tanggal · Ref`.
Status: ⬜ belum · 🟨 dikerjakan · ✅ selesai · ⏸️ ditunda.

**Wajib bisa dipindai dalam satu menit.** Kalau butuh lebih lama, ada yang salah tempat.

Fokus saat ini ditulis **satu baris**, dengan tautan ke berkas keputusannya:

```markdown
## 🎯 Fokus: <nama> — alasan di [decisions/00X-<slug>.md](decisions/00X-<slug>.md)
```

Bukan tiga paragraf. Kalau ada tiga paragraf yang ingin ditulis, itu tandanya kamu sedang membuat
berkas keputusan — buat berkasnya.

---

## `docs/decisions/` — keputusan skala-fitur

Ditulis **SEBELUM** mengerjakan sesuatu yang besar, bukan sesudah. Fungsinya sama persis dengan
dokumen arsitektur di awal proyek: menghentikan keraguan sebelum ngoding. Bedanya cuma skala.

Nama berkas: `00X-<slug>.md`, bernomor urut, tak pernah dihapus.

```markdown
# 00X — <Judul keputusan>

**Status:** 🔒 TERKUNCI <tanggal>   ·   **Terkait:** <item SYSTEMMAP>

## Yang diputuskan
<satu paragraf — apa yang akan dikerjakan>

## Kenapa sekarang
<apa yang membuatnya jadi prioritas dibanding antrean lain>

## Yang dipertimbangkan & ditolak
| Opsi | Kenapa tidak |
|---|---|

## Konsekuensi yang diterima
<yang jadi lebih sulit karena keputusan ini — jangan dikosongkan>
```

**Bagian "ditolak" jangan dilewat.** Itu satu-satunya bagian yang tak bisa direkonstruksi
belakangan. Kesimpulan selalu bisa dibaca dari kode; alternatif yang gugur menguap selamanya.

Keputusan berubah? **Buat berkas baru** yang menggantikan, tandai yang lama
`⚠️ DIGANTI oleh 00Y`. Jangan disunting — riwayat harus mencerminkan apa yang benar terjadi.

---

## `SYSTEMMAP-LOG.md` — post-mortem, append-only

Ditulis **SESUDAH** pekerjaan selesai. Entri baru **di paling atas**.

```markdown
## YYYY-MM-DD #ID

<satu kalimat: apa yang berubah>

### Yang dikerjakan
### Yang sempat salah   ← bagian paling bernilai, jangan dikosongkan kalau ada
### Bukti verifikasi     ← bukan "lint hijau" — bukti fitur benar-benar jalan
### Sisa / utang
```

Bagian **"yang sempat salah"** adalah alasan utama berkas ini ada. Bug yang gagal terdeteksi,
asumsi yang meleset, sinyal yang menyesatkan — itu yang menyelamatkanmu enam bulan lagi, bukan
daftar berkas yang diubah.

---

## Saat sebuah pekerjaan selesai — 4 langkah

1. **Status** di `SYSTEMMAP.md` → ✅ (tanggal + ref), dan cek dependensi: ada yang jadi terbuka?
2. **Entri** baru di paling atas `SYSTEMMAP-LOG.md` + satu baris di `SYSTEMMAP.md §Log`
   *(format entri sudah tersedia sebagai blok siap-salin di header LOG — salin, jangan diingat;
   anchor tautannya rapuh dan putusnya diam-diam)*
3. **Utang** yang belum tuntas → `§Utang Terbuka`, **jangan dikubur di dalam entri log**
4. **Kosongkan `§Sedang Berjalan`** — pekerjaannya sudah ditutup; checkpoint yang tertinggal akan
   dibaca sesi berikutnya sebagai pekerjaan menggantung, dan itu lebih menyesatkan daripada kosong
5. **User yang commit** — bersama kode fiturnya, supaya peta selalu sinkron

### `§Sedang Berjalan` — checkpoint, bukan catatan kerja

Diisi saat **mulai mengerjakan** dan di tiap titik jeda; dikosongkan di langkah 4 di atas. Maks 5
baris, tiga isian: **sudah beres (jangan diulang) · berikutnya · setengah jalan.**

Bedanya dengan §Utang Terbuka: utang itu yang **sengaja ditunda** dan boleh menggantung berminggu;
ini yang **sedang berlangsung** dan seharusnya kosong lagi hari itu juga. Keduanya tercampur =
dua-duanya berhenti dipercaya.

Baris "sudah beres" yang paling menentukan — ia mencegah pengulangan hal yang tak bisa diulang:
migrasi yang sudah jalan, data yang sudah terbentuk, panggilan ke layanan luar.

> Jangan menandai ✅ sebelum Definition of Done hijau **seluruhnya**, termasuk verifikasi
> end-to-end. Belum diverifikasi = 🟨, bukan ✅. "Kelihatan jalan" ≠ selesai.
