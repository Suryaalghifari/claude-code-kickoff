# Aturan Git

Default yang dipakai skill ini. Bagian **Inti** berlaku apa pun proyeknya; bagian
**Bergantung skala** ditanyakan saat wawancara.

---

## INTI — selalu dipasang

### 1. Git dijalankan USER, bukan AI

Aturan paling penting, dan yang paling sering dilanggar agen.

> **DILARANG** menjalankan `git init/add/commit/push/merge/cherry-pick/rebase`, membuat branch,
> membuka PR, atau men-deploy. **Boleh dan dianjurkan menyarankan** nama branch & pesan commit
> yang sesuai konvensi — **user yang mengeksekusi.**

Alasannya bukan soal kepercayaan, tapi kendali: commit adalah titik di mana pekerjaan jadi permanen
dan bercabang. Satu `git add .` membabi buta dari agen bisa menyeret berkas rahasia, artefak build,
atau perubahan setengah jadi ke riwayat yang lalu ikut ter-push.

Sampaikan saran dalam bentuk siap tempel:

```
Branch:  feat/kartu-project-spotlight
Commit:  feat(projects): kartu spotlight + badge tech dari API
```

### 2. Penamaan branch

Pola `tipe/deskripsi-singkat-kebab-case`. Tipe: `feat/` · `fix/` · `refactor/` · `chore/` · `docs/`.

- **Spesifik, bukan umum** — `feat/perbaikan` ❌ → `feat/kartu-project-spotlight` ✅
- Huruf kecil & dash; tanpa spasi, kapital, atau `_`
- Ringkas, 2–4 kata — nama branch bukan paragraf
- **Satu branch satu tujuan.** Kalau namanya butuh kata "dan", pecah

### 3. Pesan commit — Conventional Commits

```
feat(laporan): cetak laporan mutasi ke PDF
└┬─┘ └──┬───┘  └──────────┬─────────────┘
 │      │                 └── ringkasan: kata kerja, ≤60 char, tanpa titik
 │      └── skop (opsional): area yang disentuh
 └── tipe: sama seperti branch
```

| ❌ | ✅ |
|---|---|
| `update` | `fix(cache): invalidasi tag projects saat unpublish` |
| `fix bug` | `fix(auth): tolak JWT yang jti-nya di-blacklist` |
| `wip` | `feat(hero): badge tech stack dinamis dari API` |

- **Kata kerja perintah:** "tambah", "perbaiki", "hapus" — bukan "menambahkan"
- **Satu commit = satu perubahan utuh.** Dua hal tak terkait → dua commit
- **Jangan commit `wip`** ke branch yang akan di-PR
- **Badan menjelaskan KENAPA**, bukan apa — diff sudah menunjukkan apa. Enam bulan lagi `git log`
  satu-satunya yang ingat alasannya

### 4. Stage selektif

`git add <berkas yang relevan>` — **bukan** `git add .`. Ini yang mencegah `.env`, artefak build,
dan pekerjaan setengah jadi ikut terbawa.

### 5. Satu fitur = satu branch = satu PR

Branch dibuat dari `main` yang sudah `pull`. Selesai → push → PR.
**`main` tidak pernah menerima commit langsung.**

### 6. Merge commit, BUKAN squash

Saat merge PR, pilih **"Create a merge commit"**.

Alasannya praktis: merge commit menyisakan simpul `Merge pull request #N` yang mewakili **seluruh
PR sebagai satu titik**. Titik itu yang bisa dipetik saat deploy per-PR, dan yang bikin rollback =
membuang satu PR saja. Squash menghapus batas antar-PR, dan kemampuan itu hilang permanen.

> Kalau proyeknya tak akan pernah pakai deploy per-PR, squash boleh. Tanyakan dulu — jangan
> putuskan sendiri.

### 7. Dokumen ikut dalam PR fiturnya

Update `SYSTEMMAP.md` + entri `SYSTEMMAP-LOG.md` di-commit **bersama kode fiturnya**, bukan
belakangan. Ini satu-satunya cara peta tetap sinkron dengan kode.

### 8. Jangan commit secret

`.env` di-gitignore, `.env.example` yang di-commit. Berlaku juga untuk kunci, token, dan dump data.

---

## BERGANTUNG SKALA — tanyakan saat wawancara

### Lapisan branch

| Skala | Skema | Kapan |
|---|---|---|
| Kecil / solo / belum live | `feat/* → main` | Default. Cukup untuk sebagian besar proyek |
| Ada produksi | `feat/* → main → production` | Begitu ada pengguna nyata |
| Data nyata + banyak bagian saling bergantung | `feat/* → main → test → production` | Saat butuh uji integrasi & migrasi di lingkungan mirip produksi |

**Jangan pasang lapisan yang belum dibutuhkan.** Menambah `test` belakangan itu murah; merawat
lapisan yang tak terpakai itu beban tiap rilis.

### Deploy per-PR (cherry-pick)

Dipasang hanya bila ada branch produksi terpisah **dan** rilisnya ingin bertahap.

```bash
git log --oneline --merges origin/production..main   # PR yang belum naik
git checkout production && git pull origin production
git cherry-pick -m 1 <sha-merge-PR>                  # satu per satu, tes di antaranya
```

`-m 1` berarti "ikuti parent pertama" — sisi `main`, yaitu isi PR itu sendiri. Prinsipnya: **jangan
tumpahkan seluruh `main` sekaligus.** Kalau ada yang rusak, langsung ketahuan PR mana penyebabnya.

### Proteksi branch

Kalau repo di GitHub dan ada branch produksi: nyalakan proteksi pada `main`/`production` —
larang push langsung, wajibkan PR, wajibkan CI hijau.

---

## Yang ditulis ke `CLAUDE.md`

Hanya **aturan #1** yang masuk sebagai aturan bernomor (ia mengikat perilaku agen tiap saat).
Sisanya cukup satu baris tautan ke `docs/<NN>-git-workflow.md` — kecuali proyeknya tak punya
dokumen itu, baru ringkasan #2–#4 ikut masuk.
