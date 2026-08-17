---
name: kickoff
description: "Menyiapkan sistem konteks untuk proyek baru — wawancara arah proyek dulu sampai konvergen, baru menghasilkan CLAUDE.md, doc set yang dipilih (bukan disalin), SYSTEMMAP/DECISIONS/LOG, dan hooks. Pakai saat memulai proyek dari nol, atau saat proyek berjalan belum punya sistem konteks. Trigger: /kickoff"
---

# /kickoff

Menyiapkan **sistem konteks berlapis** untuk proyek baru: dokumen yang tepat, aturan yang
ditegakkan, dan tempat menyimpan keputusan — supaya agen AI tidak kemana-mana di tengah jalan.

Ini **bukan** generator boilerplate. Inti kerjanya wawancara: arah proyek ditemukan dulu lewat
tanya-jawab dan revisi, baru artefaknya dihasilkan. Yang mekanis diotomatiskan, yang perlu
dipikirkan tetap dipikirkan.

## Cara pakai

```
/kickoff              # di folder proyek baru (boleh kosong)
/kickoff --resume     # lanjutkan wawancara yang tertunda
/kickoff --audit      # proyek sudah jalan, BELUM punya sistem konteks
/kickoff --sync       # proyek SUDAH punya sistem konteks, tapi lahir dari skill versi lama
```

---

## Aturan yang mengikat kerjamu di skill ini

Enam pagar ini menjaga hasilnya tetap ramping. Langgar salah satu, hasilnya jadi tumpukan dokumen
mati — mode kegagalan paling umum dari sistem semacam ini.

1. **JANGAN menulis file apa pun sebelum Fase 3** — **kecuali** berkas gores
   `.kickoff-wawancara.md` dan entri yang mengabaikannya di `.gitignore` (lihat Fase 1). Yang
   dilarang adalah **artefak**; transkrip sementara bukan artefak.
2. **`CLAUDE.md` maksimal 200 baris.** Ia router, bukan gudang. Tiap baris yang tak mengubah
   keputusan harus keluar.
3. **Tidak ada dokumen tanpa baris di tabel routing.** Dokumen yang tak punya pemicu tak pernah
   dibuka — jangan dibuat.
4. **Aturan bernomor 9 ke atas dimulai KOSONG.** Ia hanya boleh lahir dari kegagalan nyata yang
   sudah terjadi (lihat `references/rules.md`). Jangan mengarang aturan antisipatif.
5. **Doc set dipilih lewat rubrik, tidak disalin.** Rubriknya: apa yang mahal diubah belakangan
   (lihat `references/doc-rubric.md`).
6. **Git dijalankan USER.** Jangan `git init/add/commit/push`. Boleh menyarankan perintahnya.

---

## Fase 1 — Wawancara (hanya berkas gores + entri `.gitignore` yang boleh ditulis)

Pastikan apa yang dibangun dan apa yang mahal jika salah sudah jelas. Baca `references/interview.md`
**sebelum bertanya**; itu sumber kanonis untuk empat ronde, cara
menjalankannya, format berkas gores/`--resume`, dan tiga kriteria konvergen. Setelah tiap ronde,
perbarui `.kickoff-wawancara.md` serta entri `.gitignore` sesuai referensi. Jangan lanjut sebelum
semua kriteria konvergen terpenuhi dan user membenarkan arah proyek.

## Fase 2 — Kunci keputusan & pilih dokumen

1. Tulis ulang tabel keputusan terkunci, bacakan ke user untuk konfirmasi terakhir.
2. Terapkan `references/doc-rubric.md` ke daftar "mahal kalau salah" → keluar daftar dokumen.
3. **Nilai tingkat kompleksitas** dengan `references/conventions.md` — skor sendiri dari jawaban
   Ronde 1 & 2, jangan menambah pertanyaan. Sampaikan hasil & alasannya; user boleh menimpa.
4. **Tunjukkan daftar dokumennya sebelum dibuat**, beserta alasan tiap dokumen ada dan apa yang
   sengaja tidak dibuat. User boleh mencoret.

## Fase 3 — Hasilkan

Salin dari `templates/`, isi tiap `{{PLACEHOLDER}}` dari hasil wawancara. Jangan sisakan satu pun
placeholder mentah.

| Berkas | Sumber | Catatan |
|---|---|---|
| `CLAUDE.md` | `CLAUDE.md.tmpl` | ≤200 baris. Aturan 1–8 terisi, 9+ kosong |
| `docs/README.md` | `docs-README.md.tmpl` | Index + konvensi dokumen |
| `docs/<terpilih>.md` | — | Ditulis dari hasil wawancara, bukan template |
| `docs/SYSTEMMAP.md` | `SYSTEMMAP.md.tmpl` | **Status saja** — tanpa prosa |
| `docs/SYSTEMMAP-LOG.md` | `SYSTEMMAP-LOG.md.tmpl` | Kosong, append-only |
| `docs/decisions/README.md` | `decisions-README.md.tmpl` | Rumah keputusan skala-fitur |
| `docs/<NN>-conventions.md` | `conventions.md.tmpl` | Lapisan sesuai tingkat kompleksitas |
| `docs/<NN>-git-workflow.md` | `git-workflow.md.tmpl` | Isi dari `references/git.md` sesuai skala |
| `.claude/commands/work.md` | `commands-work.md.tmpl` | `/work` — **tambah** fitur. Memuat kelima langkah lengkap; lihat `references/workflow.md` |
| `.claude/commands/revise.md` | `commands-revise.md.tmpl` | `/revise` — **ubah** perilaku yang ada. Hanya delta; alurnya menunjuk `work.md` |
| `.claude/commands/fix.md` | `commands-fix.md.tmpl` | `/fix` — **bug**. Reproduksi dulu; hanya delta |
| `.claude/commands/pause.md` | `commands-pause.md.tmpl` | `/pause` — simpan §Sedang Berjalan lalu berhenti |
| `.claude/commands/verify.md` | `commands-verify.md.tmpl` | `/verify` — DoD dijalankan, lihat `references/verify.md` |
| `.claude/settings.json` | `settings.json.tmpl` | Hooks + allowlist + deny git + **deny perusak data** — isi `{{DENY_STACK}}` dari stack, lihat `references/interview.md` |
| `.claude/hooks/*.py` | `hooks/` | `chmod +x` setelah disalin, lalu **uji dua arah** |
| `.gitignore` | — | Sesuai stack. `.env` masuk, `.env.example` di-commit |
| ~~`.kickoff-wawancara.md`~~ | — | **HAPUS** di akhir fase ini — isinya sudah pindah ke `CLAUDE.md` & dokumen |
| `.graphifyignore` | `graphifyignore.tmpl` | Hanya bila pakai graphify — lihat di bawah |

Aturan pembagian isi ada di `references/protocol.md` — **patuhi ketat**. Kesalahan paling sering:
menaruh alasan/penalaran di `SYSTEMMAP.md`. Alasan masuk `docs/decisions/`, bukan tabel status.

### Peta kode graphify (opsional, tanya dulu)

Kalau user memakainya atau `graphify-out/` sudah ada, baca `references/verify.md` §Lapis 6 untuk
integrasi `/verify` dan `references/audit.md` §A1 untuk `--code-only`/rebuild. Jangan pasang tanpa
diminta; pada proyek baru, tunda membangun graf sampai ada kode.

## Fase 4 — Verifikasi & serahkan

Periksa sendiri sebelum lapor:

- [ ] `CLAUDE.md` ≤200 baris, nol `{{PLACEHOLDER}}` tersisa
- [ ] Tiap dokumen di `docs/` punya baris di tabel routing — dan sebaliknya
- [ ] `SYSTEMMAP.md` tak memuat paragraf penalaran
- [ ] Tiap aturan bernomor **≤3 baris** — **hitung, jangan taksir**; jalankan pemeriksa kanonis di
      `references/rules.md` §Menghitungnya
- [ ] Perintah DoD **hanya di `.claude/commands/verify.md`**; `CLAUDE.md` #8 cuma menunjuk ke sana
- [ ] **Tiap hook `chmod +x` dan diuji dua arah** — yang seharusnya lolos *dan* yang seharusnya
      diblokir, **terhadap berkas hasil templat, bukan buatan tangan**. Dua jebakan yang sudah
      memakan korban: `references/verify.md` §Menguji hook
- [ ] Aturan 9+ kosong · `.kickoff-wawancara.md` sudah dihapus

Lalu laporkan: apa yang dibuat, apa yang **sengaja tidak** dibuat + alasannya, dan sarankan perintah
commit untuk **dijalankan user**.

---

## Fase 5 — Yang harus disampaikan ke user di akhir

Sistem ini hidup dari satu kebiasaan, dan tanpa itu ia jadi dokumen mati. Sampaikan apa adanya:

> Tiap kali saya melakukan kesalahan yang sama **dua kali**, jadikan ia aturan bernomor di
> `CLAUDE.md`. Di situlah sistem ini mulai benar-benar bekerja — aturan yang lahir dari kegagalan
> nyata jauh lebih patuh daripada aturan yang ditulis di hari pertama.

Jelaskan `/work` · `/revise` · `/fix` · `/pause` memakai `references/workflow.md` §Tiga mode dan §Pekerjaan yang terputus; `/verify` wajib sebelum ✅.
Tegaskan `docs/decisions/` **sebelum** fitur besar dan `SYSTEMMAP-LOG.md` **sesudahnya** sesuai `references/protocol.md`.

---

## Mode untuk proyek yang sudah ada

**Pilih modenya dari apa yang sudah dimiliki proyek — tertukar berarti mengerjakan hal yang salah.**

| Punya sistem konteks? | Mode | Alurnya |
|---|---|---|
| **Belum** — arah proyek cuma tertulis di kode | `--audit` | inventaris → turunkan keputusan dari kode → **gali kandidat aturan dari `git log`** → backfill SYSTEMMAP → laporkan celah. `references/audit.md` |
| **Sudah**, tapi lahir dari skill versi lama | `--sync` | cari penanda aturan mati (§S2) → hormati batasnya → laporkan per seberapa sering dibaca → tutup dengan entri `#SYNC`. `references/sync.md` |

Tiga batas yang berlaku di **kedua** mode:

- **Laporkan lalu BERHENTI.** Menyajikan tabel temuan **bukan** izin untuk mulai menulis. Tunggu
  user menjawab, lalu kerjakan hanya yang disetujui — satu per satu, bukan sepaket.
- **Jangan timpa apa pun.** Berkas yang sudah ada hanya diubah setelah diff-nya ditunjukkan.
- **Jangan membersihkan kode.** Aturan yang berubah berlaku untuk yang ditulis **sesudahnya**.

## Perawatan berkala

Diminta merapikan sistem yang berjalan, atau `--audit` menemukan pembusukan → `references/maintenance.md`.

## Referensi

| Berkas | Isi | Baca saat |
|---|---|---|
| `references/interview.md` | 4 ronde pertanyaan + kriteria konvergen | Fase 1 |
| `references/doc-rubric.md` | Rubrik "mahal diubah" → doc set | Fase 2 |
| `references/conventions.md` | Penilai kompleksitas + konvensi berlapis | Fase 2 & 3 |
| `references/git.md` | Aturan git: inti + yang bergantung skala | Fase 3 |
| `references/protocol.md` | Aturan SYSTEMMAP / decisions / LOG | Fase 3 |
| `references/rules.md` | Pagar 3 baris + aturan-dari-kegagalan + DoD | Fase 3 & 5 |
| `references/workflow.md` | Alur work/revise/fix + checkpoint pause | Fase 3 & 5 |
| `references/verify.md` | Lima lapis verifikasi + blok bukti | Fase 3, saat mengisi `/verify` |
| `references/audit.md` | Alur proyek existing tanpa sistem konteks | `--audit` |
| `references/sync.md` | Menyamakan proyek lama dengan templat sekarang | `--sync` |
| `references/maintenance.md` | Ambang pembusukan, rotasi LOG, hook | `--audit` & perawatan |
