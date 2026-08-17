---
name: kickoff
description: "Menyiapkan dan menjalankan sistem konteks proyek melalui wawancara, dokumentasi berlapis, audit, sync, serta mode work, revise, fix, verify, dan pause. Pakai melalui /kickoff pada proyek baru maupun existing."
---

# /kickoff untuk Hermes

Router Hermes untuk metodologi kickoff. Simpan detail di `references/` dan baca hanya ketika fase
atau mode terkait benar-benar dijalankan.

## Cara pakai

```text
/kickoff
/kickoff --resume
/kickoff --audit
/kickoff --sync
/kickoff work <tugas>
/kickoff revise <perilaku yang diubah>
/kickoff fix <bug>
/kickoff verify
/kickoff pause
```

## Binding Hermes

References kanonis masih memakai nama artefak Claude pada beberapa bagian. Saat menjalankannya di
Hermes, terapkan binding berikut tanpa mengubah keputusan metodologisnya:

| Istilah kanonis | Binding Hermes |
|---|---|
| `CLAUDE.md` | `AGENTS.md` |
| `/work`, `/revise`, `/fix`, `/verify`, `/pause` | `/kickoff work`, `/kickoff revise`, `/kickoff fix`, `/kickoff verify`, `/kickoff pause` |
| `.claude/commands/verify.md` | bagian Definition of Done yang ditautkan dari `AGENTS.md` |
| `.claude/commands/*` | tidak dibuat; gunakan mode `/kickoff` |
| `SessionStart` | baca `AGENTS.md` lalu `docs/SYSTEMMAP.md` saat mulai sesi |
| hooks dan `.claude/settings.json` | tidak dibuat pada versi minimum Hermes |

Nama Claude yang memang membahas integrasi Claude Code bukan instruksi untuk membuat artefak
Hermes. Jangan meniru hook, settings, atau wire protocol Claude.

## Enam pagar

1. **Jangan menulis artefak sebelum Fase 3.** Pengecualian hanya `.kickoff-wawancara.md` dan entri
   `.gitignore` yang mengabaikannya selama wawancara.
2. **`AGENTS.md` maksimal 200 baris.** Ia router, bukan gudang.
3. **Tidak ada dokumen tanpa baris routing.** Dokumen tanpa pemicu baca tidak dibuat.
4. **Aturan bernomor 9+ mulai kosong.** Tambahkan hanya setelah kesalahan yang sama terjadi dua kali.
5. **Doc set dipilih lewat rubrik.** Jangan menyalin semua dokumen yang tersedia.
6. **Git dijalankan user.** Jangan `git init/add/commit/push/merge/rebase/cherry-pick`, membuat
   branch/PR, atau deploy. Boleh menyarankan perintahnya; pemeriksaan read-only tetap boleh.

## Dispatch mode

Mode pekerjaan tidak menjalankan Fase 1–5 kickoff:

- `work`, `revise`, atau `fix`: baca `references/workflow.md` saat mode dipanggil. Terapkan delta
  mode yang tertulis di sana; untuk `fix`, reproduksi kegagalan sebelum memperbaiki.
- `verify`: baca `references/verify.md`, lalu jalankan DoD proyek yang ditautkan dari `AGENTS.md`
  secara berurutan dan berhenti pada kegagalan pertama. Abaikan bagian pengujian hook Claude.
- `pause`: baca hanya `references/workflow.md` bagian pekerjaan terputus; isi
  `docs/SYSTEMMAP.md` §Sedang Berjalan lalu berhenti tanpa verify, ✅, atau entri LOG.
- `--audit`: baca `references/audit.md`; laporkan temuan dan berhenti sebelum menulis.
- `--sync`: baca `references/sync.md`, lalu reference kanonis yang diperintahkannya; laporkan diff
  dan berhenti sebelum menerapkan perubahan.

## Fase 1 — Wawancara

Baca `references/interview.md` sebelum bertanya. Jalankan empat ronde sampai tiga kriteria
konvergen terpenuhi. Hanya berkas gores dan entri `.gitignore` yang boleh ditulis. Lewati detail
hook/settings Claude; jangan menggantinya dengan desain baru.

## Fase 2 — Kunci keputusan dan pilih dokumen

1. Konfirmasikan tabel keputusan terkunci kepada user.
2. Baca `references/doc-rubric.md` dan pilih dokumen berdasarkan hal yang mahal diubah.
3. Baca `references/conventions.md` untuk menilai kompleksitas dari jawaban yang sudah ada.
4. Tunjukkan doc set beserta alasan sebelum membuatnya.

## Fase 3 — Hasilkan

Baca `references/protocol.md`, `references/git.md`, `references/rules.md`, dan bagian relevan dari
`references/workflow.md`. Gunakan `templates/AGENTS.md.tmpl`; isi semua placeholder.

Hasilkan hanya artefak yang dipilih:

| Artefak | Sumber |
|---|---|
| `AGENTS.md` | `templates/AGENTS.md.tmpl` |
| `docs/README.md` dan doc set terpilih | hasil wawancara + rubrik |
| `docs/SYSTEMMAP.md` | format di `references/protocol.md` |
| `docs/SYSTEMMAP-LOG.md` | `templates/SYSTEMMAP-LOG.md.tmpl` |
| `docs/decisions/README.md` | `templates/decisions-README.md.tmpl` |
| dokumen conventions + DoD konkret | `references/conventions.md` + hasil wawancara |
| dokumen Git | `references/git.md` sesuai skala |
| `.gitignore` | sesuai stack |

Hapus `.kickoff-wawancara.md` setelah isinya terserap. Jangan membuat `.claude/`, hooks, atau
settings Hermes pada versi minimum ini.

## Fase 4 — Verifikasi dan serahkan

Pastikan `AGENTS.md` ≤200 baris, tidak ada placeholder tersisa, routing dokumen dua arah lengkap,
SYSTEMMAP hanya berisi status, aturan bernomor memenuhi pagar tiga baris dari
`references/rules.md`, aturan 9+ kosong, dan DoD hanya punya satu sumber. Laporkan artefak yang
dibuat serta yang sengaja tidak dibuat. Git tetap dijalankan user.

## Fase 5 — Aktifkan kebiasaan kerja

Jelaskan lima mode `/kickoff`, aturan kegagalan-dua-kali, keputusan sebelum pekerjaan besar, serta
protokol SYSTEMMAP/decisions/LOG. Baca detail hanya dari `references/workflow.md`,
`references/rules.md`, dan `references/protocol.md` ketika menyampaikannya.

## Reference on-demand

| Reference | Baca saat |
|---|---|
| `references/interview.md` | Fase 1 |
| `references/doc-rubric.md`, `references/conventions.md` | Fase 2 |
| `references/protocol.md`, `references/git.md`, `references/rules.md` | Fase 3 |
| `references/workflow.md` | Fase 3/5 atau mode work/revise/fix/pause |
| `references/verify.md` | mode verify; bagian graphify hanya bila dipakai |
| `references/audit.md` | `--audit` |
| `references/sync.md` | `--sync` |
| `references/maintenance.md` | saat pembusukan ditemukan atau diminta |
