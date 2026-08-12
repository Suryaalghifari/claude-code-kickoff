# Verifikasi — DoD yang Dijalankan, Bukan Diingat

Aturan #8 menuntut bukti. Tanpa alat, ia cuma himbauan yang dipatuhi saat sempat.

**Kasus yang membuat berkas ini ada:** sebuah fitur analytics lolos seluruh lint dan test, tapi
rusak diam-diam **15 hari**. Browser membuang requestnya tanpa error; tak satu pun test menyentuh
jalur browser sungguhan. Tidak ada suite yang bisa menangkap itu — hanya membuka browser yang bisa.

---

## Lima lapis, dan yang kelima yang menentukan

| Lapis | Membuktikan | Tidak membuktikan |
|---|---|---|
| 1 · Formatter | kode ter-format | apa pun soal perilaku |
| 2 · Static analysis | tipe & bug statis konsisten | perilaku saat jalan |
| 3 · Test | yang diuji lulus | yang tak diuji |
| 4 · Build | artefaknya jadi | artefaknya benar |
| **5 · Alur nyata** | **fiturnya jalan untuk pemakai** | — |

Empat lapis pertama otomatis dan murah. **Lapis kelima yang paling sering dilewat, dan satu-satunya
yang menangkap kegagalan diam.**

### Lapis 3 & database: hitung query-nya, jangan cuma "hijau"

Query buruk **lolos seluruh test fungsional** — hasilnya benar, yang salah ongkosnya. N+1 tak pernah
membuat assertion gagal; ia cuma membuat halaman lambat tiga bulan lagi saat barisnya jadi ribuan.

Karena itu, untuk alur yang menyentuh DB, lapis 3 memverifikasi **jumlah query**, bukan cuma hasil:

- Ada mekanismenya di stack (assertion jumlah query, query log, `EXPLAIN`) → pasang di test alur itu.
- Tidak ada → minimal **jalankan alurnya sekali dengan query log menyala dan baca angkanya.** Sekali
  lihat sudah cukup menangkap N+1.

Yang dicari bukan angka mutlak, tapi **pertumbuhannya**: jumlah query yang naik mengikuti jumlah
baris data = N+1, apa pun angkanya. Uji dengan 1 baris lalu 10 — kalau ikut naik, itu temuannya.

> Ini sengaja **gerbang, bukan bab**. Cara mengoptimasi query bukan pengetahuan yang kurang — yang
> kurang adalah sesuatu yang menangkapnya sebelum ia sampai produksi. Menambahkan teori ke dokumen
> tak menangkap apa pun; satu angka yang dibaca menangkapnya.

---

## Bentuk nyata lapis kelima

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

## Menguji hook — dua jebakan yang sudah memakan korban

Hook rusak **gagal diam-diam**, jadi ia wajib diuji dua arah. Tapi cara mengujinya sendiri punya
dua jebakan, keduanya ditemukan di pemakaian nyata:

**1. Uji terhadap berkas yang BENAR-BENAR dihasilkan, bukan buatan tangan.**

```bash
# ❌ bikin SYSTEMMAP contoh sendiri, lalu uji → lolos, padahal templatnya bermasalah
# ✅ hasilkan dari templatnya dulu, baru uji
sed -e 's/{{FOKUS}}/x/' -e 's/{{FASE_1}}/Fase 1/' templates/SYSTEMMAP.md.tmpl > docs/SYSTEMMAP.md
python3 .claude/hooks/session-start.py
```

Kasus nyatanya: `session-start.py` diuji terhadap SYSTEMMAP buatan tangan dan lolos. Pada berkas
hasil templat ia **selalu** memancarkan peringatan "ada pekerjaan belum ditutup" — contoh checkpoint
di dalam `<!-- ... -->` terbaca sebagai data, dan pemisah `---` ikut lolos filter. Tiap proyek baru
lahir dengan alarm palsu permanen. **Peringatan yang selalu muncul adalah peringatan yang berhenti
dibaca** — dan yang dilemahkannya justru satu-satunya mekanisme penjaga pekerjaan terputus.

Pelajaran umumnya: **hook membaca berkas nyata, jadi ujinya harus memakai berkas nyata.** Berkas
contoh yang kamu tulis sendiri diam-diam menghindari persis kasus yang bikin hook itu ada.

**2. Kasus uji perintah tinggal di berkas, jangan di baris perintah.**

`destructive-guard.py` membaca **seluruh string perintah**. Menguji lewat Bash yang memuat
`migrate:fresh` sebagai data uji membuat hook memblokir skrip ujinya sendiri. Itu bukti ia hidup,
tapi ujinya tak jadi jalan. Taruh kasusnya di berkas terpisah lalu suapkan lewat stdin.

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
