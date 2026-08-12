# Perawatan — Melawan Pembusukan

Sistem konteks tak rusak mendadak; ia menggemuk perlahan sampai tak ada yang membacanya. Ambang di
bawah diturunkan dari pengukuran proyek nyata, bukan angka karangan.

Jalankan tiap **~1 bulan** atau saat `/kickoff --audit`.

---

## Pemeriksaan

```bash
wc -l CLAUDE.md docs/*.md
grep -c '^## ' docs/SYSTEMMAP-LOG.md          # jumlah entri log
ls docs/decisions/*.md 2>/dev/null | wc -l
```

| Gejala | Ambang | Tindakan |
|---|---|---|
| `CLAUDE.md` menggemuk | **200 baris** | Pindahkan badan aturan terpanjang ke dokumen, sisakan perintah + tautan |
| Satu aturan jadi mini-dokumen | **3 baris** | Sama — badan ke dokumen, tautan tinggal |
| Dokumen menampung 2 topik | **400 baris** | Pecah |
| LOG tak terkelola | **~40 entri / ~800 baris** | Arsip per kuartal (di bawah) |
| Dokumen tanpa pemicu | 0 rujukan di router | Masukkan tabel routing, atau hapus |
| Aturan mati | bagiannya sudah dihapus | Buang — aturan mati melemahkan yang hidup |
| Keputusan tak terekam | ada 🎯 tanpa berkas `decisions/` | Tulis surut, tandai jujur `(ditulis surut)` |
| Placeholder tertinggal | ada `{{` di berkas proyek | Isi |

### Kenapa ambangnya segitu

Pada proyek rujukan, dari 10 aturan bernomor, **tiga aturan terakhir memakan 71% blok aturan** —
dan 26 baris di antaranya ternyata **salinan** dari isi dokumen yang sudah ditautkan. Aturan #1–#7
yang rata-rata 1,9 baris justru yang paling tak pernah salah dipatuhi. Panjang bukan ketegasan.

LOG-nya mencapai **68 entri / 1.919 baris** tanpa mekanisme rotasi — satu-satunya bagian yang
tumbuh linear tanpa rem.

---

## Rotasi LOG

Pada ~40 entri, pindahkan entri lama ke arsip:

```
docs/SYSTEMMAP-LOG.md              ← kuartal berjalan
docs/log-archive/2026-Q3.md        ← yang lama, utuh, tak disunting
```

`SYSTEMMAP-LOG.md` menyimpan tautan ke arsip di bagian bawah. Entri lama **tak pernah diubah atau
diringkas** — dipindahkan apa adanya. Riwayat yang diedit belakangan berhenti jadi riwayat.

Tabel ringkas di `SYSTEMMAP.md §Log` tetap memuat **semua** baris, tautannya menyesuaikan ke arsip.

---

## Naikkan aturan jadi hook

Rawat berkala yang paling menguntungkan: **tiap aturan yang bisa dicek mesin, pindahkan ke hook,
lalu hapus dari `CLAUDE.md`.** Router ikut ramping, dan penegakannya justru menguat — aturan di
prompt bisa dilupakan model; hook tidak.

| Bentuk aturan | Bisa jadi |
|---|---|
| "Jangan jalankan `git commit/push`" | `permissions.deny` |
| "Jangan tulis rahasia ke berkas" | `PreToolUse` pada `Write\|Edit` |
| "Jangan jalankan perintah yang menghapus data" | `permissions.deny` **+** `PreToolUse` pada `Bash` — deny mencocokkan bentuk perintah, hook membaca seluruh stringnya |
| "Baca peta/status dulu sebelum mulai" | `SessionStart` |
| "Format harus X" | linter di pre-commit, bukan prosa di dokumen |

Yang **tak bisa** jadi hook dan memang harus tinggal sebagai prosa: gaya komentar, pilihan
penamaan, keputusan arsitektur.

---

## Tanda sistemnya sudah tak dipercaya

Kalau salah satu muncul, berhenti menambah dan bereskan dulu:

- Ada ✅ di SYSTEMMAP untuk sesuatu yang ternyata tak jalan → **satu ✅ palsu meracuni seluruh
  peta**; sesudah itu tak ada yang membacanya lagi
- `decisions/` kosong padahal sudah beberapa kali ganti arah
- Bagian "Yang sempat salah" di LOG selalu "—" → entah proyeknya ajaib, entah entrinya tak jujur
- User berhenti membuka SYSTEMMAP dan bertanya langsung "sudah sampai mana?"
