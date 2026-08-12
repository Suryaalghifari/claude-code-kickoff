# Verifikasi — DoD yang Dijalankan, Bukan Diingat

Aturan #8 menuntut bukti. Tanpa alat, ia cuma himbauan yang dipatuhi saat sempat.

**Kasus yang membuat berkas ini ada:** sebuah fitur analytics lolos seluruh lint dan test, tapi
rusak diam-diam **15 hari**. Browser membuang requestnya tanpa error; tak satu pun test menyentuh
jalur browser sungguhan. Tidak ada suite yang bisa menangkap itu — hanya membuka browser yang bisa.

---

## Empat lapis, dan yang keempat yang menentukan

| Lapis | Membuktikan | Tidak membuktikan |
|---|---|---|
| Formatter | kode ter-format | apa pun soal perilaku |
| Static analysis | tipe & bug statis konsisten | perilaku saat jalan |
| Test | yang diuji lulus | yang tak diuji |
| **Alur nyata** | **fiturnya jalan untuk pemakai** | — |

Tiga lapis pertama otomatis dan murah. **Lapis keempat yang paling sering dilewat, dan satu-satunya
yang menangkap kegagalan diam.**

---

## Bentuk nyata lapis keempat

| Jenis proyek | Verifikasi yang sah | Yang **tidak** cukup |
|---|---|---|
| Web app | Buka **browser**, jalankan alurnya, periksa hasilnya tampil. Upload lewat form nyata (FormData) | `curl` — melewati CORS, cookie, CSP, dan perilaku browser |
| API | Panggil dari klien yang sebenarnya memakainya | test internal saja |
| CLI | Jalankan di terminal bersih, periksa exit code & keluaran | unit test |
| Library | Pakai dari proyek contoh di **luar** repo | test internal |
| Data pipeline | Jalankan pada data nyata, periksa keluarannya | "tak ada exception" |

**Yang wajib diperiksa di browser** dan tak bisa ditiru `curl`: request lintas-origin (CORS,
preflight) · cookie `httpOnly`/`SameSite` · CSP memblokir skrip/koneksi · `sendBeacon`/`keepalive` ·
upload `FormData` (boundary, ukuran) · redirect setelah login · apa yang benar-benar **ter-render**,
bukan cuma dikirim.

Kalau tersedia otomasi browser (mis. Chrome MCP), **pakai** — dan simpan tangkapan layarnya sebagai
bukti. Kalau tidak, minta user menjalankan alurnya dan melaporkan hasilnya; **jangan tandai ✅ atas
nama asumsi.**

---

## Jalankan berurutan, berhenti di kegagalan pertama

1. Formatter → 2. Static analysis → 3. Test → 4. Build → 5. **Alur nyata**

Gagal di tengah? **Berhenti, laporkan, perbaiki.** Jangan lanjut ke lapis berikutnya membawa
kegagalan — dan jangan pernah melaporkan "sebagian besar hijau".

## Lapis 6 — segarkan peta kode (bila proyek memakai graphify)

Bukan gerbang lulus/gagal; ini **perawatan**. Jalankan **setelah lima lapis hijau**, hanya bila
`graphify-out/` ada:

```bash
graphify update .        # AST-only, tanpa LLM
```

Kenapa di sini: langkah "gali" pada `/work` dan tiap query graphify membaca `graph.json`. Begitu
kode berubah tanpa peta diperbarui, sesi berikutnya berorientasi pada peta **basi** — dan peta basi
lebih berbahaya daripada tidak ada peta, karena ia terlihat berwibawa. Momen paling tepat
memperbaruinya adalah tepat setelah perubahan kode terbukti benar.

Ongkosnya kecil: pada monorepo 3 aplikasi (±5.600 node) **13 detik**.

> **`update` TIDAK membersihkan graf yang sudah tercampur.** Ia hanya me-re-extract berkas kode;
> node dokumen yang terlanjur masuk akan tetap di sana. Kalau grafnya tercampur, yang dibutuhkan
> **rebuild**, bukan update — lihat `audit.md` §A1.

Gagal atau `graphify` tak terpasang → **catat, jangan hentikan**. Peta basi tak membatalkan bukti
bahwa fiturnya jalan.

### Mengisi `{{LANGKAH_GRAPHIFY}}` di `commands-verify.md.tmpl`

Proyek **memakai** graphify (ada `graphify-out/`, atau user bilang ya) → tempel blok ini:

```markdown
Proyek ini punya peta kode graphify. Setelah lima lapis hijau:

    graphify update .

AST-only, tanpa LLM. Ini perawatan, bukan gerbang: gagal atau graphify tak terpasang → catat saja,
jangan hentikan. Peta yang basi membuat langkah "gali" pada /work berorientasi pada kode yang sudah
tak ada — dan itu lebih berbahaya daripada tak punya peta, karena terlihat berwibawa.
```

Proyek **tidak** memakai graphify → **hapus seluruh section 6**, jangan tinggalkan placeholder.
Jangan pula memasang graphify hanya karena template menyebutnya.

## Keluaran: blok bukti siap tempel

Setelah lima lapis hijau, hasilkan ini untuk `SYSTEMMAP-LOG.md`:

```markdown
### Bukti verifikasi
- Format: `<perintah>` → 0 masalah
- Analysis: `<perintah>` → 0 error
- Test: `<perintah>` → N lolos
- Build: `<perintah>` → sukses
- **Alur nyata:** <apa yang dijalankan, di mana, hasilnya apa>
  <mis. "Login admin → upload thumbnail 2,3 MB lewat form → gambar tampil di /projects
   dengan URL /media/xxx.webp. Chrome 141, tanpa error konsol.">
```

**Baris terakhir tak boleh berupa nama perintah.** Ia harus menceritakan alur yang dijalani dan apa
yang terlihat. Kalau kamu tak bisa menuliskannya, berarti kamu belum memverifikasi.

---

## Kejujuran melapor

- Ada yang gagal → **katakan, dengan keluarannya.** Jangan diringkas jadi "ada sedikit masalah".
- Ada lapis yang dilewat → **katakan lapis mana dan kenapa.** Melewati lapis 5 karena tak ada
  browser itu boleh; menyembunyikannya tidak.
- Belum diverifikasi = **🟨, bukan ✅.** Ini bukan formalitas: satu ✅ palsu membuat seluruh
  SYSTEMMAP tak bisa dipercaya, dan sekali kepercayaan itu hilang, tak ada yang membacanya lagi.
