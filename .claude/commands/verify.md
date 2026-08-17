---
description: Jalankan Definition of Done repo skill ini
---

Jalankan berurutan, **berhenti di kegagalan pertama**. Jangan lanjut membawa kegagalan, dan jangan
pernah melaporkan "sebagian besar hijau".

Repo ini isinya markdown + tiga hook Python — tak ada build, tak ada suite test. Yang menggantikan
keduanya adalah **menjalankan hooknya sungguhan** dan **menjalankan skillnya sungguhan**.

## 1. Sintaks pemasang

```bash
bash -n install.sh
```

## 2. Hook — diuji dua arah

Hook rusak **gagal diam-diam**: ia terpasang, terlihat wajar, dan tak pernah menjalankan tugasnya.
Karena itu ketiganya wajib diperiksa dua arah, bukan hanya yang "tidak error".

```bash
printf '%s' '{"tool_input":{"file_path":"a.php","content":"password = \"Sup3rS3cretPw\""}}' \
  | ./skill/templates/hooks/secret-scan.py; echo "harus 2 → $?"

printf '%s' '{"tool_input":{"file_path":"a.php","content":"$k = config(\"app.key\");"}}' \
  | ./skill/templates/hooks/secret-scan.py; echo "harus 0 → $?"

printf '%s' 'bukan json' | ./skill/templates/hooks/secret-scan.py; echo "harus 0 → $?"
```

`session-start.py` — **uji terhadap berkas hasil templat, jangan buatan tangan.** SYSTEMMAP contoh
yang ditulis sendiri diam-diam menghindari persis kasus yang bikin hooknya ada; bug alarm palsu
lolos dari uji dengan cara itu, dan baru ketahuan di proyek nyata.

```bash
VERIFY_REPO_ROOT="$(pwd)"
VERIFY_TMP_ROOT="$(mktemp -d)"
mkdir -p "$VERIFY_TMP_ROOT/docs"
sed -e 's/{{FOKUS}}/x/' -e 's/{{FASE_1}}/Fase 1/' -e 's/{{N}}/1/' -e 's/{{ITEM}}/setup/' \
  skill/templates/SYSTEMMAP.md.tmpl > "$VERIFY_TMP_ROOT/docs/SYSTEMMAP.md"

VERIFY_EMPTY_OUT="$(cd "$VERIFY_TMP_ROOT" && \
  python3 "$VERIFY_REPO_ROOT/skill/templates/hooks/session-start.py")"
printf 'checkpoint kosong → %s peringatan (harus 0)\n' \
  "$(printf '%s\n' "$VERIFY_EMPTY_OUT" | grep -c 'Ada pekerjaan yang belum ditutup' || true)"

sed -i '/^## 🔄 Sedang Berjalan$/a\
- **Berikutnya:** uji checkpoint positif' \
  "$VERIFY_TMP_ROOT/docs/SYSTEMMAP.md"
VERIFY_CHECKPOINT_OUT="$(cd "$VERIFY_TMP_ROOT" && \
  python3 "$VERIFY_REPO_ROOT/skill/templates/hooks/session-start.py")"
printf '%s\n' "$VERIFY_CHECKPOINT_OUT" | grep -q 'uji checkpoint positif'
echo "checkpoint terbaca → harus 0: $?"
```

Dari folder tanpa `docs/SYSTEMMAP.md` ia harus **diam** dan keluar 0.

`destructive-guard.py` — arah "lolos" yang lebih penting di sini: hook yang memblokir kerja
sehari-hari akan dimatikan orang, dan begitu dimatikan ia tak melindungi apa pun.

```bash
g() { printf '%s' "{\"tool_input\":{\"command\":\"$1\"}}" \
      | ./skill/templates/hooks/destructive-guard.py >/dev/null 2>&1; echo "$2 → $?"; }

g 'php artisan migrate:fresh'          'harus 2'
g 'psql -c \"DROP DATABASE x;\"'       'harus 2'
g 'docker compose down -v'             'harus 2'
g 'git push --force origin main'       'harus 2'
g 'php artisan migrate'                'harus 0'
g 'rm -rf node_modules'                'harus 0'
g 'docker compose down'                'harus 0'
g 'git push --force-with-lease o b'    'harus 0'
```

## 3. Placeholder

`templates/` boleh ber-`{{PLACEHOLDER}}` — memang itu gunanya. `references/` **tidak**, kecuali
disertai cara mengisinya.

```bash
grep -rn '{{' skill/references/
```

Temuan **sah** kalau ia berupa: judul `### Mengisi {{X}} di …`, rujukan ke placeholder yang sudah
dijelaskan, contoh perintah yang justru **sedang mengisinya** (`sed 's/{{X}}/…/'`), atau kalimat
tentang placeholder secara umum. **Pelanggaran** hanya kalau `{{X}}` muncul sebagai isi yang
seakan-akan menunggu diisi, tanpa penjelasan cara mengisinya.

> Jangan ubah ini jadi "harus nol temuan". Cek yang selalu merah berhenti dibaca — dan yang hilang
> bukan cuma ceknya, tapi kepercayaan pada lapis di sekitarnya.

## 4. Router sinkron

Tiap berkas di `skill/references/` wajib punya baris di tabel routing `CLAUDE.md`, dan sebaliknya.

```bash
for f in skill/references/*.md; do
  grep -q "$(basename "$f")" CLAUDE.md || echo "TAK ADA DI ROUTER: $f"
done
```

## 5. Pasangan `references/` ↔ `templates/`

Aturan #9 lahir dari sini, dua kali: aturan diperbaiki di `references/`, templat yang menyalinnya
dibiarkan basi. Yang sampai ke proyek pengguna adalah `templates/` — jadi perbaikan yang berhenti
di `references/` **tidak pernah berlaku**, dan gejalanya muncul sebagai "aturannya ada tapi
dilanggar terus".

```bash
# aturan lama yang seharusnya sudah mati — harus nol temuan di KEDUA folder.
# sync.md DIKECUALIKAN: ia justru menyimpan penanda itu sebagai data (tabel §S2).
grep -rn 'Delapan pertanyaan\|hanya "WHY"\|non-obvious' skill/ --exclude=sync.md

# aturan yang baru dicabut wajib punya barisnya di tabel penanda —
# tanpa itu `--sync` buta, dan proyek lama memegang aturan mati selamanya
grep -c '^|' skill/references/sync.md

# pasangan yang wajib sejalan bila salah satunya disentuh
#   references/conventions.md  ↔  templates/conventions.md.tmpl
#   references/workflow.md     ↔  templates/commands-work.md.tmpl + CLAUDE.md.tmpl §Alur
#   references/verify.md       ↔  templates/commands-verify.md.tmpl
#   references/git.md          ↔  templates/git-workflow.md.tmpl
```

Yang diperiksa bukan kesamaan kata per kata — `templates/` memang lebih ringkas. Yang diperiksa:
**tak ada aturan di satu sisi yang sudah dicabut di sisi lain.**

## 6. Ambang ukuran

`SKILL.md` dimuat **tiap kali skill dijalankan** — sama seperti `CLAUDE.md` di proyek, jadi
ambangnya sama. Ia sempat tumbuh 189 → 224 baris dalam satu sesi tanpa ada yang menahan.

```bash
awk 'END{print FILENAME": "NR" (maks 200)"}' skill/SKILL.md
awk 'END{if(NR>400) print FILENAME": "NR" — LEBIH DARI 400, pecah"}' skill/references/*.md
awk 'END{print FILENAME": "NR" (maks 200)"}' CLAUDE.md
```

Lewat ambang → **badan penjelasnya pindah ke `references/`, sisakan perintah + tautan.** Yang tak
boleh dipangkas: keenam pagar dan tabel berkas Fase 3 — keduanya mengikat perilaku, bukan
menjelaskannya.

## 7. Alur nyata — yang paling menentukan

Enam pemeriksaan di atas membuktikan berkasnya utuh. **Tak satu pun membuktikan skillnya bekerja.**

```bash
mkdir -p /tmp/uji-kickoff && cd /tmp/uji-kickoff
claude          # lalu: /kickoff   (atau /kickoff --audit di salinan repo nyata)
```

Yang diperiksa: wawancaranya menajamkan atau terasa seperti formulir · tingkat kompleksitas yang
ditebak masuk akal · **tak ada keputusan terkunci yang alasannya tak pernah kamu sebut** ·
nol placeholder tertinggal di hasilnya · hook yang dihasilkan benar-benar jalan.

Poin ketiga yang paling penting: skill yang mengarang alasan lebih berbahaya daripada skill yang
bertanya terlalu sering.

## Keluaran

```markdown
### Bukti verifikasi
- `bash -n install.sh` → lolos
- Hook secret-scan → blokir 2, lolos 0, json rusak 0
- Hook session-start → checkpoint kosong tanpa peringatan, checkpoint terisi terbaca, berkas hilang diam
- Hook destructive-guard → blokir 4, lolos 4
- Placeholder di references/ → 0 tanpa penjelasan
- Router ↔ references → sinkron N/N
- **Alur nyata:** <apa yang dijalankan, di folder apa, hasilnya apa yang terlihat>
```

Baris terakhir tak boleh berupa nama perintah. Ada yang gagal atau dilewat → katakan yang mana,
dengan keluarannya.
