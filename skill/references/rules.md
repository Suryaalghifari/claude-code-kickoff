# Aturan yang Tumbuh & Definition of Done

## Kenapa aturan 9+ dimulai kosong

Aturan #1–#8 memang dikirim terisi — itu pagar dasar yang berlaku di proyek apa pun (git, konvensi,
SYSTEMMAP, DoD). Yang dimulai kosong adalah **#9 ke atas**: slot untuk aturan yang hanya kamu yang
bisa menemukannya.

Di proyek rujukan, tiga aturan yang paling banyak menyelamatkan pekerjaan **tak satu pun ada di
dokumen awal**. Semuanya masuk pada hari ke-2 dan ke-5, setelah gagal:

| Kapan | Aturan yang lahir | Pemicunya |
|---|---|---|
| hari ke-2 | Definition of Done + pola frontend wajib | AI berulang kali salah pola yang sama |
| hari ke-5 | Invarian keamanan | Hasil pentest |
| minggu ke-4 | Keputusan positioning terkunci | Arah produk sempat melayang |

Sebabnya sederhana: **di hari pertama kamu belum tahu mode kegagalanmu sendiri.** Tak ada yang bisa
menebak "media harus berupa uuid dari picker, bukan URL manual" sebelum melihat AI salah tiga kali.

Yang bisa disiapkan di depan cuma **slot dan disiplinnya** — bukan isinya.

## Aturan dua-kali

> Kesalahan yang sama terjadi **dua kali** → jadikan aturan bernomor di `CLAUDE.md`.

Sekali itu kecelakaan. Dua kali itu pola, dan pola bisa dicegah.

**Bentuk yang bekerja** — spesifik, punya alasan, dan bisa diperiksa:

```markdown
9. **Media = uuid dari picker, BUKAN URL manual.** Disimpan sebagai `*_media_id`; backend yang
   resolve uuid → `{ url }`. Lihat [docs/08-media.md](docs/08-media.md#upload).
```

Aturan di `CLAUDE.md` **boleh** menautkan ke dokumen — itu memang fungsinya sebagai router.
Yang tidak boleh adalah **komentar di kode** menautkan ke dokumen; lihat
[`conventions.md`](conventions.md) bagian komentar.

**Bentuk yang gagal** — kabur, tak bisa diperiksa, tak punya alasan:

```markdown
9. Tulis kode yang bersih dan ikuti best practice.
```

Aturan yang tak bisa diperiksa benar/salahnya bukan aturan; ia hiasan, dan ia melemahkan kepatuhan
pada aturan di sekitarnya.

## Pagar 3 baris

> **Satu aturan maksimal 3 baris.** Lebih dari itu, badannya pindah ke dokumen — sisakan perintah
> + tautan.

Ini pagar terpenting di berkas ini, karena pelanggarannya terasa seperti ketelitian. Diukur pada
proyek rujukan: dari 10 aturan, **tiga aturan terakhir memakan 71% blok aturan**, dan 26 baris di
antaranya ternyata **salinan** isi dokumen yang sudah ditautkan di aturan itu sendiri. Sementara
aturan #1–#7 yang rata-rata 1,9 baris justru yang paling tak pernah salah dipatuhi.

Panjang bukan ketegasan, dan salinan kedua selalu jadi yang pertama basi.

```markdown
❌ 17 baris berisi enam sub-invarian + ringkasan isi docs/10

✅ 10. **Invarian keamanan.** Enam invarian — header di origin · sanitasi input publik ·
       PII di luar payload global · error tanpa key mentah · rel="noopener" · CORS.
       Jangan langgar tanpa membaca [docs/10-security.md](docs/10-security.md#invarian).
```

Aturan yang butuh lebih dari 3 baris biasanya beberapa aturan yang dipaksa jadi satu nomor.

## Rawat berkalanya

- Aturan yang tak pernah relevan lagi (bagiannya sudah dihapus) → **buang**. Aturan mati menurunkan
  bobot aturan hidup.
- `CLAUDE.md` mendekati 200 baris → terapkan pagar 3 baris ke aturan terpanjang.
- **Aturan yang bisa ditegakkan hook, jadikan hook — lalu HAPUS dari `CLAUDE.md`.** Aturan di prompt
  itu himbauan; model bisa lupa. Hook itu penegakan, dan router ikut ramping. Lihat
  `maintenance.md`.

---

## Definition of Done

**Perintahnya tinggal di satu tempat saja: `.claude/commands/verify.md`.** Aturan #8 hanya
menunjuk ke sana:

```markdown
8. **Definition of Done = `/verify` hijau seluruhnya** — format, analysis, test, build, dan
   **alur nyata**. Perintahnya di `.claude/commands/verify.md`, satu sumber.
   "Kelihatan jalan" ≠ selesai; belum diverifikasi = 🟨, bukan ✅.
```

> Jangan tergoda menyalin daftar perintah ke `CLAUDE.md` "biar kelihatan". Uji lapangan pertama
> skill ini menghasilkan tepat itu — perintah kembar di `CLAUDE.md` #8 dan `/verify` — dan aturan
> #8 jadi 9 baris, satu-satunya yang melanggar pagar 3 baris. Dua salinan pasti berbeda suatu hari,
> dan yang basi selalu yang lebih mudah dibaca.

**Baris end-to-end itu yang paling penting**, dan yang paling sering kosong. Lint hijau membuktikan
kode ter-format; test hijau membuktikan yang diuji lulus. Keduanya **tidak** membuktikan fiturnya
jalan untuk pemakai.

Contoh bentuk nyata per jenis proyek:

| Jenis | Verifikasi end-to-end yang sah |
|---|---|
| Web app | Jalankan alurnya di **browser**, bukan hanya `curl`. Upload diuji lewat form nyata |
| CLI | Jalankan perintahnya di terminal bersih, periksa exit code & keluarannya |
| Library | Pakai dari proyek contoh di luar repo, bukan hanya dari test internal |
| Data pipeline | Jalankan pada data nyata, periksa keluarannya, bukan hanya "tak ada exception" |

Kasus nyata yang bikin aturan ini ada: sebuah fitur analytics lolos seluruh test dan lint, tapi
**rusak diam-diam 15 hari** — browser membuang requestnya tanpa error. Test tidak pernah menyentuh
jalur browser sungguhan. Tidak ada suite yang bisa menangkap itu; hanya membuka browser yang bisa.
