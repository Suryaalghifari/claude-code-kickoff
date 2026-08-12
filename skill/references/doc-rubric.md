# Rubrik Pemilihan Dokumen

**Aturan tunggal:** buat dokumen untuk tiap dimensi yang **mahal diubah belakangan**. Sisanya
jangan dibuat di depan — biarkan tumbuh bersama kode.

## Kenapa begitu — buktinya

Diukur dari satu proyek nyata (369 commit, 15 dokumen, ~1 bulan). Kolom "bertahan" = berapa persen
isi dokumen yang ditulis di depan masih utuh setelah kode berjalan:

| Dokumen | Bertahan | Ongkos salah | Vonis |
|---|---|---|---|
| Konvensi koding | 100% (nol revisi) | konsistensi seluruh repo | **tulis di depan** |
| Desain database | 88% | migrasi + data nyata | **tulis di depan** |
| Design system | 90% | menyentuh ratusan berkas | **tulis di depan** |
| Spesifikasi API | **40%** | ganti satu endpoint = murah | **jangan** — 60% ditulis ulang |
| Panduan frontend | 61% | sedang | rangka saja |
| Deployment | — (lahir hari ke-4) | — | **tunda** — jadi salah satu dok terpenting justru karena reaktif |

Polanya jelas: **yang bertahan adalah yang mahal diubah.** Menulis 766 baris spesifikasi endpoint
di hari pertama menghasilkan ~450 baris tebakan yang harus dibongkar.

Temuan kedua, sama pentingnya: dokumen yang **tak punya baris di tabel routing `CLAUDE.md`** nol
kali dibuka sepanjang proyek. Bukan karena isinya jelek — karena tak ada yang memicunya.

---

## Pemetaan

Dari daftar mahal-diubah (Ronde 2) ke dokumen:

| Kalau user menyebut… | Buat | Ukuran wajar |
|---|---|---|
| bentuk data, skema, migrasi | `0X-data-model.md` | lengkap — ini paling mahal |
| tampilan, warna, komponen, tema | `0X-design-system.md` | lengkap — token & aturan |
| konsistensi kode, banyak orang/AI menulis | `0X-conventions.md` | **sesuai tingkat** — lihat `conventions.md` |
| auth, PII, izin, data sensitif | `0X-security.md` | invarian saja, tumbuhkan dari temuan |
| kontrak antar-bagian, ada konsumen lain | `0X-contracts.md` | **rangka + 1 contoh saja** |
| alur/arsitektur berlapis | `0X-architecture.md` | ringkas — kesimpulannya naik ke `CLAUDE.md` |
| deploy, environment, rilis | — | **tunda** sampai deploy pertama benar-benar dekat |
| urutan pengerjaan, prioritas | — | sudah ditangani `SYSTEMMAP.md` |

## Yang selalu dibuat, apa pun proyeknya

- `CLAUDE.md` — router + keputusan terkunci + aturan
- `docs/README.md` — index + konvensi dokumen
- `docs/SYSTEMMAP.md` + `docs/SYSTEMMAP-LOG.md` — status & riwayat
- `docs/decisions/` — rumah keputusan skala-fitur
- `docs/<NN>-conventions.md` — **selalu ada, tapi isinya berlapis.** Bahkan proyek Ringan butuh
  Lapis 0 (penamaan, gaya komentar, fungsi kecil); ongkosnya nol dan ia yang bikin kode terbaca
  seminggu lagi. Yang berubah cuma berapa lapis yang dipasang — lihat `conventions.md`

## Yang tidak pernah dibuat di depan

Spesifikasi endpoint lengkap · panduan per-halaman/per-modul · deployment · panduan kontribusi ·
changelog · roadmap panjang di luar `SYSTEMMAP`.

---

## Pagar ukuran

- Satu dokumen **> 400 baris** → tanda ia menampung dua topik. Pecah.
- Dokumen yang tak muat dibaca sekali duduk tak akan dibaca utuh — oleh manusia maupun AI.
- Ragu antara membuat atau tidak → **jangan buat**. Menambah dokumen belakangan itu murah;
  membersihkan dokumen mati itu tak pernah dilakukan siapa pun.

## Sebelum lanjut ke Fase 3

Tunjukkan ke user: daftar dokumen yang akan dibuat, alasan tiap dokumen ada, dan **apa yang sengaja
tidak dibuat**. Bagian terakhir itu yang paling sering menyelamatkan — user sering baru sadar
sesuatu penting justru saat melihat ia tidak ada di daftar.
