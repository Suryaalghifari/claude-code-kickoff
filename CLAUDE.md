# CLAUDE.md

Briefing untuk Claude Code di repo ini. **Baca ini dulu sebelum tugas apa pun.**

> **Batas keras: 200 baris.** Berkas ini **router**, bukan gudang.
> Repo ini memakai metodenya sendiri — kalau ia melanggar aturannya sendiri, itu bug.

---

## Apa proyek ini

Skill `/kickoff` untuk Claude Code: menyiapkan **sistem konteks** proyek baru — dokumen yang tepat,
aturan yang ditegakkan, dan tempat menyimpan keputusan. Bukan generator boilerplate; intinya
**wawancara** yang berputar sampai arah proyek konvergen, baru artefaknya dihasilkan.

Isinya **markdown + dua hook Python**. Tak ada aplikasi yang jalan, tak ada dependensi.

```
skill/
├── SKILL.md            instruksi utama — 5 fase + 6 pagar
├── references/         11 berkas metodologi (dimuat sesuai fase)
└── templates/          rangka berkas + hooks yang disalin ke proyek pengguna
install.sh              salin skill/ → ~/.claude/skills/kickoff/
```

---

## Keputusan TERKUNCI (jangan diubah tanpa instruksi user)

| Aspek | Keputusan | Alasan |
|-------|-----------|--------|
| Platform | **Claude Code saja** | Lapis penegakan (hooks, slash command) khas Claude Code. Klaim multi-platform berarti mengirim versi yang diam-diam kehilangan bagian terkuatnya |
| Bahasa | Narasi **Indonesia**, identifier & perintah Inggris | Sama dengan proyek yang dilayaninya |
| Bentuk | **Wawancara**, bukan folder yang disalin | Proyek berikutnya bebas jenisnya; doc set harus dipilih, bukan ditimpakan |
| Distribusi | Repo terpisah + `install.sh`, **bukan** langsung di `~/.claude/skills/` | Bisa diversikan & dibagikan; cadangan wajib **di luar** `skills/` — apa pun di dalamnya terbaca sebagai skill |
| Lisensi | **MIT** | Permisif; metodologi hanya berguna kalau boleh dipakai |
| Isi templat | Netral, **nol data pribadi** | Repo publik. Contoh memakai "proyek rujukan", bukan nama proyek nyata |

---

## Mulai sesi

1. [README.md](README.md) — bentuk repo & cara pakainya
2. [skill/SKILL.md](skill/SKILL.md) — 5 fase + 6 pagar yang mengikat perilaku skill
3. Baru buka referensi sesuai tabel di bawah

---

## Dokumen mana untuk tugas apa

| Kalau tugasnya… | Baca dulu |
|-----------------|-----------|
| Orientasi menyeluruh | [README.md](README.md) |
| Mengubah alur/fase skill | [skill/SKILL.md](skill/SKILL.md) |
| Pertanyaan wawancara, kriteria konvergen | [references/interview.md](skill/references/interview.md) |
| Dokumen apa yang layak dibuat | [references/doc-rubric.md](skill/references/doc-rubric.md) |
| Konvensi koding & penilai kompleksitas | [references/conventions.md](skill/references/conventions.md) |
| Aturan git yang dipasang ke proyek | [references/git.md](skill/references/git.md) |
| SYSTEMMAP / decisions / LOG | [references/protocol.md](skill/references/protocol.md) |
| Pagar 3 baris, aturan-dari-kegagalan, DoD | [references/rules.md](skill/references/rules.md) |
| Alur `/work` (tambah vs revisi fitur) | [references/workflow.md](skill/references/workflow.md) |
| Lapis verifikasi & blok bukti | [references/verify.md](skill/references/verify.md) |
| Mode `--audit` untuk proyek existing | [references/audit.md](skill/references/audit.md) |
| Mode `--sync` — proyek dari skill versi lama | [references/sync.md](skill/references/sync.md) |
| Ambang pembusukan, rotasi LOG, hook | [references/maintenance.md](skill/references/maintenance.md) |

> **Tidak ada dokumen tanpa baris di tabel ini.** Menambah referensi berarti menambah barisnya juga.

---

## Alur satu pekerjaan

1. **Orientasi** — baca `SKILL.md` bagian yang akan disentuh
2. **Gali** — `grep -ri "<topik>" skill/references/` sebelum menambah aturan baru; hampir setiap
   aturan sudah punya rumah, dan aturan kembar di dua berkas akan berbeda suatu hari
3. **Putuskan** — mengubah arah skill (platform, bentuk, distribusi) → bicarakan dengan user dulu
4. **Kerjakan** — ikuti konvensi di bawah. Jangan melebar dari yang diminta
5. **Tutup** — jalankan Definition of Done (aturan 8), lalu sarankan branch & commit

---

## Aturan kerja WAJIB

> **Satu aturan maksimal 3 baris.** Lebih panjang = badannya pindah ke referensi, sisakan
> perintah + tautan.

1. **GIT DIJALANKAN USER, BUKAN CLAUDE.** Jangan `git init/add/commit/push/merge/rebase`, membuat
   branch, atau membuka PR. **Boleh menyarankan** nama branch & pesan commit sesuai Conventional
   Commits — user yang mengeksekusi.
2. **Repo ini memakai metodenya sendiri.** Pagar 3 baris, larangan rujukan di komentar kode, dan
   "tak ada dokumen tanpa pemicu" berlaku **di sini juga**, bukan hanya di templat yang dihasilkan.
3. **Nol data pribadi.** Tanpa nama, domain, path mesin, atau nama proyek nyata di `skill/`.
   Contoh memakai "proyek rujukan" dan angka yang benar-benar diukur.
4. **Angka dalam dokumen harus nyata.** Tiap klaim terukur berasal dari pengukuran sungguhan;
   jangan mengarang statistik yang terdengar meyakinkan.
5. **Templat vs referensi.** `templates/` = berkas yang disalin ke proyek pengguna (boleh
   ber-`{{PLACEHOLDER}}`); `references/` = instruksi untuk Claude (**tak boleh** ada placeholder
   mentah yang tak dijelaskan cara mengisinya).
6. **Jangan menambah kemampuan yang belum diminta.** Skill ini gemuk = mati. Fitur ditambahkan
   setelah ada kebutuhan nyata, bukan sebelum.
7. **Setelah mengubah `skill/`, ingatkan user menjalankan `./install.sh`** — salinan terpasang di
   `~/.claude/skills/kickoff/` tidak ikut berubah sendiri.
8. **Definition of Done = `/verify` hijau seluruhnya** — pemasang, hook dua arah, placeholder,
   router, pasangan templat, dan **menjalankan skillnya sungguhan**. Perintahnya di
   [`.claude/commands/verify.md`](.claude/commands/verify.md), **satu sumber**.
9. **Mengubah aturan di `skill/references/` → WAJIB periksa pasangannya di `skill/templates/`.**
   `references/` cuma instruksi saat kickoff; `templates/` yang sampai ke proyek dan dibaca tiap
   ngoding. Perbaikan yang berhenti di `references/` tak pernah berlaku. Gerbangnya `/verify` §5.

<!--
  Aturan 10 ke atas SENGAJA KOSONG.

  Diisi hanya saat kesalahan yang sama terjadi DUA KALI. Sekali itu kecelakaan; dua kali itu pola.
  Aturan yang lahir dari kegagalan nyata jauh lebih dipatuhi daripada aturan yang ditulis di hari
  pertama — dan repo ini justru ada untuk mengajarkan hal itu.

  Bentuk yang bekerja — spesifik, beralasan, bisa diperiksa:
    9. **<larangan/keharusan konkret>.** <alasan singkat>. Lihat skill/references/<nama>.md.

  Bentuk yang gagal — kabur, tak bisa diperiksa:
    9. Tulis dokumentasi yang baik.
-->

---

## Perintah

```bash
./install.sh              # pasang ke ~/.claude/skills/kickoff/
./install.sh --uninstall  # lepas
bash -n install.sh        # cek sintaks

# uji ketiga hook dua arah → /verify §2, SATU SUMBER (jangan disalin ke sini)
```
