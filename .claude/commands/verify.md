---
description: Jalankan Definition of Done repo skill ini
---

Jalankan berurutan, **berhenti di kegagalan pertama**. Jangan lanjut membawa kegagalan, dan jangan
pernah melaporkan "sebagian besar hijau".

Repo ini isinya markdown + dua hook Python — tak ada build, tak ada suite test. Yang menggantikan
keduanya adalah **menjalankan hooknya sungguhan** dan **menjalankan skillnya sungguhan**.

## 1. Sintaks pemasang

```bash
bash -n install.sh
```

## 2. Hook — diuji dua arah

Hook rusak **gagal diam-diam**: ia terpasang, terlihat wajar, dan tak pernah menghalangi apa pun.
Karena itu keduanya wajib diperiksa, bukan hanya yang "tidak error".

```bash
printf '%s' '{"tool_input":{"file_path":"a.php","content":"password = \"Sup3rS3cretPw\""}}' \
  | ./skill/templates/hooks/secret-scan.py; echo "harus 2 → $?"

printf '%s' '{"tool_input":{"file_path":"a.php","content":"$k = config(\"app.key\");"}}' \
  | ./skill/templates/hooks/secret-scan.py; echo "harus 0 → $?"

printf '%s' 'bukan json' | ./skill/templates/hooks/secret-scan.py; echo "harus 0 → $?"
```

`session-start.py` diuji dari folder proyek ber-`docs/SYSTEMMAP.md`; dari folder tanpa itu ia harus
**diam** dan keluar 0.

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
grep -rn '{{' skill/references/     # tiap temuan harus punya section "Mengisi ..."
```

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

Empat langkah di atas membuktikan berkasnya utuh. **Tak satu pun membuktikan skillnya bekerja.**

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
- Placeholder di references/ → 0 tanpa penjelasan
- Router ↔ references → sinkron N/N
- **Alur nyata:** <apa yang dijalankan, di folder apa, hasilnya apa yang terlihat>
```

Baris terakhir tak boleh berupa nama perintah. Ada yang gagal atau dilewat → katakan yang mana,
dengan keluarannya.
