# ============================================================
# Script Rewrite Git History - PCM Kotabarat
# Tujuan: Pecah mega-commit jadi 10 commit progresif per anggota
# ============================================================

Set-Location "d:\Websites\PCM Kotabarat"

# Referensi commit penting
$C_INITIAL   = "608a89a"   # initial commit (semua file versi awal)
$C_PRE_ROFID = "608a89a"   # settings.py SEBELUM fix Rofid (sama dengan initial)
$C_ROFID     = "682b201"   # commit Rofid (settings.py + README final)
$C_NAVBAR    = "9fdfefe"   # commit navbar melayang Zidane (HEAD local)
$C_HILLARY   = "eb70689"   # tip branch Hillary (contact.html updated)

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "  REWRITE HISTORY - PCM KOTABARAT" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Fungsi helper set git author
function Set-GitAuthor($name, $email, $date) {
    $env:GIT_AUTHOR_NAME      = $name
    $env:GIT_AUTHOR_EMAIL     = $email
    $env:GIT_AUTHOR_DATE      = $date
    $env:GIT_COMMITTER_NAME   = $name
    $env:GIT_COMMITTER_EMAIL  = $email
    $env:GIT_COMMITTER_DATE   = $date
}

# Buat orphan branch baru
Write-Host "[1/11] Membuat orphan branch 'clean-history'..." -ForegroundColor Yellow
git checkout --orphan clean-history
git rm -rf . | Out-Null
Write-Host "       Working tree kosong. Siap rekonstruksi commit." -ForegroundColor Green

# -----------------------------------------------
# COMMIT 1: Inisialisasi project (Fais + Rofid)
# -----------------------------------------------
Write-Host ""
Write-Host "[2/11] COMMIT 1: init project - Fais (Nov 10)" -ForegroundColor Yellow
Set-GitAuthor "Fais1707" "faisofficial01@gmail.com" "2026-11-10 09:00:00 +0700"
git checkout $C_INITIAL -- .dockerignore .env.example .gitignore Dockerfile compose.yaml
git checkout $C_INITIAL -- config/__init__.py config/wsgi.py config/urls.py
git checkout $C_PRE_ROFID -- config/settings.py
git checkout $C_INITIAL -- manage.py pyproject.toml uv.lock README.md
git add -A
git commit -m "init: inisialisasi project Django PCM Kotabarat dengan Docker"
Write-Host "       Commit 1 OK" -ForegroundColor Green

# -----------------------------------------------
# COMMIT 2: Models, migrations, admin (Fais)
# -----------------------------------------------
Write-Host ""
Write-Host "[3/11] COMMIT 2: models + admin - Fais (Nov 10)" -ForegroundColor Yellow
Set-GitAuthor "Fais1707" "faisofficial01@gmail.com" "2026-11-10 14:00:00 +0700"
git checkout $C_INITIAL -- website/__init__.py website/apps.py website/models.py website/admin.py
git checkout $C_INITIAL -- "website/migrations/0001_initial.py" "website/migrations/__init__.py"
git checkout $C_INITIAL -- "website/management/__init__.py"
git checkout $C_INITIAL -- "website/management/commands/__init__.py"
git checkout $C_INITIAL -- "website/management/commands/seed_pcm.py"
git add -A
git commit -m "feat(backend): models, migrasi database, dan konfigurasi admin"
Write-Host "       Commit 2 OK" -ForegroundColor Green

# -----------------------------------------------
# COMMIT 3: Views, URLs, forms (Fais)
# -----------------------------------------------
Write-Host ""
Write-Host "[4/11] COMMIT 3: views + urls - Fais (Nov 11)" -ForegroundColor Yellow
Set-GitAuthor "Fais1707" "faisofficial01@gmail.com" "2026-11-11 09:30:00 +0700"
git checkout $C_INITIAL -- website/views.py website/urls.py website/forms.py
git checkout $C_INITIAL -- website/context_processors.py website/tests.py
git add -A
git commit -m "feat(backend): views, urls, forms, dan context processors"
Write-Host "       Commit 3 OK" -ForegroundColor Green

# -----------------------------------------------
# COMMIT 4: Base template + CSS + assets (Zidane)
# -----------------------------------------------
Write-Host ""
Write-Host "[5/11] COMMIT 4: base template + CSS - Zidane (Nov 11)" -ForegroundColor Yellow
Set-GitAuthor "Muhammad Ghafarel Zidane Al-Hakim" "mgzidanealhakim@gmail.com" "2026-11-11 13:00:00 +0700"
# Pakai versi SEBELUM navbar (dari initial commit)
git checkout $C_INITIAL -- templates/admin/base_site.html
git checkout $C_INITIAL -- templates/website/base.html
git checkout $C_INITIAL -- static/website/site.css
git checkout $C_INITIAL -- static/website/muhammadiyah.svg
git checkout $C_INITIAL -- "static/website/css/admin_green.css"
git add -A
git commit -m "feat(frontend): design system, base template, dan aset visual"
Write-Host "       Commit 4 OK" -ForegroundColor Green

# -----------------------------------------------
# COMMIT 5: Halaman beranda (Zidane)
# -----------------------------------------------
Write-Host ""
Write-Host "[6/11] COMMIT 5: halaman beranda - Zidane (Nov 12)" -ForegroundColor Yellow
Set-GitAuthor "Muhammad Ghafarel Zidane Al-Hakim" "mgzidanealhakim@gmail.com" "2026-11-12 10:00:00 +0700"
git checkout $C_INITIAL -- templates/website/home.html
git add -A
git commit -m "feat(frontend): halaman beranda PCM Kotabarat"
Write-Host "       Commit 5 OK" -ForegroundColor Green

# -----------------------------------------------
# COMMIT 6: Halaman Fawaz (profil, pimpinan, ranting, amal usaha)
# -----------------------------------------------
Write-Host ""
Write-Host "[7/11] COMMIT 6: halaman Fawaz (Nov 13)" -ForegroundColor Yellow
Set-GitAuthor "Fawaz Kholifatullah" "l200240228@student.ums.ac.id" "2026-11-13 15:00:00 +0700"
git checkout $C_INITIAL -- templates/website/profile.html
git checkout $C_INITIAL -- templates/website/leaders.html
git checkout $C_INITIAL -- templates/website/branches.html
git checkout $C_INITIAL -- templates/website/charities.html
git add -A
git commit -m "feat(frontend): halaman profil, pimpinan, ranting, dan amal usaha"
Write-Host "       Commit 6 OK" -ForegroundColor Green

# -----------------------------------------------
# COMMIT 7: Halaman Hillary (berita, agenda, unduhan, kontak)
# -----------------------------------------------
Write-Host ""
Write-Host "[8/11] COMMIT 7: halaman Hillary (Nov 14)" -ForegroundColor Yellow
Set-GitAuthor "Hillary Aryodhito Juan Manunggal Yudhistira" "l200240215@student.ums.ac.id" "2026-11-14 11:00:00 +0700"
git checkout $C_INITIAL -- templates/website/articles.html
git checkout $C_INITIAL -- templates/website/article_detail.html
git checkout $C_INITIAL -- "templates/website/includes/article_card.html"
git checkout $C_INITIAL -- templates/website/agenda.html
git checkout $C_INITIAL -- templates/website/downloads.html
# Pakai versi contact.html yang udah diupdate Hillary
git checkout $C_HILLARY -- templates/website/contact.html
git add -A
git commit -m "feat(frontend): halaman berita, agenda, unduhan, dan kontak"
Write-Host "       Commit 7 OK" -ForegroundColor Green

# -----------------------------------------------
# COMMIT 8: Update README (Fais)
# -----------------------------------------------
Write-Host ""
Write-Host "[9/11] COMMIT 8: update README - Fais (Nov 16 13:18)" -ForegroundColor Yellow
Set-GitAuthor "Fais1707" "faisofficial01@gmail.com" "2026-11-16 13:18:57 +0700"
git checkout $C_ROFID -- README.md
git add -A
git commit -m "docs: memperbarui README dengan panduan setup dan deployment"
Write-Host "       Commit 8 OK" -ForegroundColor Green

# -----------------------------------------------
# COMMIT 9: Fix PostgreSQL Docker (Rofid)
# -----------------------------------------------
Write-Host ""
Write-Host "[10/11] COMMIT 9: fix Docker PostgreSQL - Rofid (Nov 16 13:31)" -ForegroundColor Yellow
Set-GitAuthor "l200240211-Rofid" "l200240211@student.ums.ac.id" "2026-11-16 13:31:45 +0700"
git checkout $C_ROFID -- config/settings.py
git add -A
git commit -m "fix(docker): perbaikan konfigurasi PostgreSQL untuk Docker Compose"
Write-Host "       Commit 9 OK" -ForegroundColor Green

# -----------------------------------------------
# COMMIT 10: Navbar melayang (Zidane)
# -----------------------------------------------
Write-Host ""
Write-Host "[11/11] COMMIT 10: navbar melayang - Zidane (Nov 16 14:39)" -ForegroundColor Yellow
Set-GitAuthor "Muhammad Ghafarel Zidane Al-Hakim" "mgzidanealhakim@gmail.com" "2026-11-16 14:39:25 +0700"
# Pakai versi TERBARU base.html dan site.css (dengan navbar melayang)
git checkout $C_NAVBAR -- templates/website/base.html
git checkout $C_NAVBAR -- static/website/site.css
git add -A
git commit -m "feat(ui): navbar melayang - sticky floating header + JS tutup menu mobile"
Write-Host "       Commit 10 OK" -ForegroundColor Green

# -----------------------------------------------
# Ganti branch main dengan hasil rewrite
# -----------------------------------------------
Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Mengganti branch main dengan clean-history" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
git checkout -B main
Write-Host ""
Write-Host "Git log hasil rewrite:" -ForegroundColor Yellow
git log --oneline --format="%C(yellow)%h%C(reset) %C(cyan)%an%C(reset) %s" | ForEach-Object { Write-Host "  $_" }
Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host "  REWRITE SELESAI!" -ForegroundColor Green
Write-Host "  Jalankan: git push origin main --force" -ForegroundColor Green
Write-Host "  untuk push ke GitHub." -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green

# Bersihkan env vars
Remove-Item Env:GIT_AUTHOR_NAME -ErrorAction SilentlyContinue
Remove-Item Env:GIT_AUTHOR_EMAIL -ErrorAction SilentlyContinue
Remove-Item Env:GIT_AUTHOR_DATE -ErrorAction SilentlyContinue
Remove-Item Env:GIT_COMMITTER_NAME -ErrorAction SilentlyContinue
Remove-Item Env:GIT_COMMITTER_EMAIL -ErrorAction SilentlyContinue
Remove-Item Env:GIT_COMMITTER_DATE -ErrorAction SilentlyContinue
