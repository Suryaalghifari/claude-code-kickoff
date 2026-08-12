# Wawancara Kickoff — 4 Ronde

Tujuan seluruh wawancara: **menghentikan keraguan sebelum baris kode pertama.** Bukan mengumpulkan
kelengkapan data.

## Cara menjalankan

- **Satu ronde satu giliran.** Tunggu jawaban sebelum lanjut.
- **Sodorkan usulan, jangan interogasi.** User biasanya datang dengan gagasan kasar. Format yang
  bekerja: *"Dari yang kamu ceritakan, saya menangkap X. Untuk Y saya sarankan A karena Z —
  alternatifnya B kalau nanti butuh C. Betul begitu?"*
- **Boleh berputar.** Kalau jawaban ronde 2 mengubah ronde 1, kembali ke ronde 1. Konvergensi lebih
  penting dari urutan.
- **Berhenti bertanya kalau sudah cukup.** Kelengkapan bukan tujuan; kejelasan arah iya.

---

## Ronde 1 — Apa yang dibangun

1. Apa yang dibangun, dalam satu kalimat? Kalau ada yang mirip, sebutkan sebagai patokan.
2. Siapa pemakainya, dan apa yang mereka lakukan dengannya?
3. **Ini yang membedakan proyek jadi dan proyek terbengkalai:** apa tanda proyek ini *selesai*?
   Kalau tak bisa dijawab, gali sampai bisa.
4. Sekali jalan lalu ditinggal, atau dirawat bertahun-tahun? (menentukan seberapa ketat konvensinya)
5. Kerja sendiri, atau ada orang lain yang akan membaca kodenya?

**Keluaran:** ringkasan 3 kalimat yang dibenarkan user. Kalau ia mengoreksi, tulis ulang dan
konfirmasi lagi — jangan lanjut sebelum benar.

---

## Ronde 2 — Apa yang mahal kalau salah

Ronde paling menentukan. Jawabannya langsung jadi doc set.

1. **Kalau ini salah di minggu ke-3, apa yang paling bikin sengsara?** Biarkan user menyebut
   sendiri dulu, jangan disodori daftar.
2. Lalu telusuri satu per satu yang relevan:
   - Bentuk data / skema — sudah ada data nyata yang harus dimigrasi kalau berubah?
   - Kontrak antar-bagian (API, format berkas, protokol) — ada pihak lain yang bergantung?
   - Tampilan / desain — perubahan menyentuh banyak berkas sekaligus?
   - Auth & keamanan — bocornya permanen?
   - Cara deploy / lingkungan — bisa dicoba ulang dengan murah?
3. Untuk tiap yang disebut: **kalau salah, ongkos perbaikannya jam atau minggu?**
4. Sebaliknya — apa yang **murah** diubah kapan saja? (ini sengaja **tidak** didokumentasikan
   di depan)

**Keluaran:** daftar dimensi mahal-diubah, terurut. Masuk ke `doc-rubric.md`.

---

## Ronde 3 — Keputusan terkunci

Untuk tiap dimensi mahal dari Ronde 2, pancing keputusannya sampai final.

1. Bahasa/runtime, framework, penyimpanan data, autentikasi — sejauh yang relevan saja.
2. **Bentuk repo** — satu folder untuk semua · satu repo banyak bagian (berbagi tooling) · repo
   terpisah per bagian. *(Ambil yang paling kecil yang cukup: memecah belakangan itu pekerjaan
   tersendiri, tapi menggabung lebih murah daripada memecah.)* Ini **paling mahal diubah** dari
   seluruh tabel — mengganti ORM itu sakit, memecah repo di bulan ketiga itu proyek baru.
3. **Akses data** — ORM · query builder · SQL mentah, **dan di mana query boleh tinggal**
   (model/repository saja, atau bebas di handler?). Batas "di mana" ini yang menentukan apakah
   query buruk bisa ditemukan belakangan; tanpanya ia tersebar dan tak ada yang bisa mengauditnya.
4. Untuk tiap keputusan, **wajib ada alasan sebaris**. Keputusan tanpa alasan akan dibongkar ulang
   tiga minggu lagi, dan itu persis yang mau dicegah.
5. Kalau user ragu: sodorkan rekomendasi + trade-off, jangan lempar balik pertanyaan mentah.
6. Kalau memang belum bisa diputuskan, tandai `[BELUM]` — **jangan** ditebak. Keputusan palsu lebih
   berbahaya dari keputusan yang tertunda.

> Poin 2 & 3 ditanyakan **sekali**, lalu jadi baris keputusan terkunci. Jangan berubah jadi diskusi
> struktur folder ideal — bentuk yang benar mengikuti jawaban poin 2, bukan sebaliknya.

**Keluaran:** tabel `| Aspek | Keputusan | Alasan |` siap tempel ke `CLAUDE.md`.

---

## Ronde 4 — Cara kerja

Ini yang bikin agen tidak kemana-mana sehari-hari.

1. **Git** — baca `references/git.md` dulu, lalu tanyakan **tiga hal ini saja**; sisanya pakai
   default dari sana tanpa bertanya:
   - Operasi git dijalankan user, atau AI boleh? *(default: **user** — sarankan ini)*
   - Lapisan branch: `main` saja · `main → production` · `main → test → production`?
     *(pilih yang paling kecil yang cukup — menambah lapisan belakangan itu murah)*
   - Rilis bertahap per-PR (merge commit + cherry-pick), atau rilis seluruh `main` sekaligus?
     *(jawabannya menentukan merge commit vs squash — jangan diputuskan sendiri)*
2. **Bahasa** — kode, komentar, dan dokumen. (Umum: identifier Inggris, komentar & dokumen Indonesia)
3. **Gaya komentar** — minimal "why" saja, atau deskriptif? *(default: minimal "why")*
   > Seberapa ketat konvensi lainnya **jangan ditanyakan** — kamu sudah punya bahannya dari Ronde
   > 1 & 2 (umur proyek, jumlah pembaca, jumlah bagian, taruhan data). Skor sendiri lewat
   > `references/conventions.md`, lalu **sampaikan hasil penilaianmu** untuk dikoreksi. User tak
   > punya kewajiban menilai kompleksitas proyeknya sendiri; kamu yang menilai, ia yang memutuskan.
4. **Definition of Done** — perintah nyatanya apa? Isi yang berlaku, hapus yang tidak:
   - formatter: `_______`
   - static analysis / type check: `_______`
   - test: `_______`
   - build: `_______`
   - **verifikasi end-to-end: bagaimana bentuk nyatanya di proyek ini?**
5. **Hooks** — ada perintah yang ingin ditegakkan/dilarang otomatis? (lihat `settings.json.tmpl`)
6. Ada preferensi keras dari proyek sebelumnya yang wajib dibawa?

> Poin 4 bagian terakhir jangan dilewat. "Lint hijau" bukan bukti fitur jalan — dan di situlah
> mayoritas pekerjaan ditandai selesai padahal belum.

**Keluaran:** isi aturan wajib 1–7 di `CLAUDE.md` + blok perintah DoD yang konkret.

---

## Kriteria konvergen

Berhenti mewawancara **hanya** kalau ketiganya terpenuhi:

- [ ] Ringkasan 3 kalimat dibenarkan user
- [ ] Tiap baris keputusan terkunci punya alasan (atau ditandai `[BELUM]` secara sadar)
- [ ] Daftar mahal-diubah lengkap, dan user setuju itu memang daftarnya

Belum terpenuhi? Katakan bagian mana yang masih kabur, lalu lanjutkan. **Jangan** menutupi
kekaburan dengan menghasilkan dokumen — dokumen yang lahir dari jawaban setengah matang justru
mengunci arah yang salah.
