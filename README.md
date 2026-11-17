# 🌐 Website Pimpinan Cabang Muhammadiyah (PCM) Kottabarat

<div align="center">

![Django](https://img.shields.io/badge/Django-6.0-092E20?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.12%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Render](https://img.shields.io/badge/Render-Hosted-46E3B7?style=for-the-badge&logo=render&logoColor=white)

**Tugas 1 Mata Kuliah Pemrograman Web Berbasis Framework (TIF1336)**  
*Program Studi Informatika · Universitas Muhammadiyah Surakarta*

[🌍 Kunjungi Website Production](https://pcm-kottabarat.onrender.com) · [🔒 Panel Admin](https://pcm-kottabarat.onrender.com/admin/)

</div>

---

## 📖 Tentang Proyek

Website resmi informasi publik untuk **Pimpinan Cabang Muhammadiyah (PCM) Kottabarat Surakarta**. Dibangun menggunakan framework **Django 6.0**, database **PostgreSQL 17**, dikontainerisasi dengan **Docker Compose**, dan disajikan dengan antarmuka modern menggunakan **CSS3 murni (Zero Framework Dependency)**.

### 🌟 Fitur Unggulan
- **Silsilah Pimpinan Dinamis (`/pimpinan/`):** Bagan pohon hierarki organisasi (Dewan Penasehat, Pucuk Pimpinan, Wakil Ketua, hingga Unsur Pembantu Pimpinan/Majelis) yang terhubung langsung ke database Django Admin.
- **Sinkronisasi Berita Otomatis:** Command crawler `sync_news` untuk mengambil berita terbaru seputar Kottabarat dari portal resmi [Muhammadiyah Solo](https://muhammadiyahsolo.com/) beserta foto aslinya.
- **Agenda Terjadwal (`/agenda/`):** Kalender kegiatan persyarikatan lengkap dengan hari, waktu WIB, dan lokasi.
- **Formulir Aspirasi & Kontak (`/kontak/`):** Terintegrasi langsung dengan database dan diproteksi token CSRF serta validasi server-side.
- **Panel Admin Instan (`/admin/`):** Manajemen konten terpadu dengan shortcut ikon gembok di footer website.
- **Zero-Dependency CSS:** Desain modern, bersih, dan responsif menggunakan CSS Grid, Flexbox, dan CSS Variables tanpa ketergantungan library eksternal (Bootstrap/Tailwind).

---

## 👥 Tim Pengembang (Kelompok K)

| Foto / Inisial | Nama | NIM | Peran Utama |
|:---:|---|:---:|---|
| 🏗️ | **Muhammad Ghafarel Zidane Al-Hakim** | L200240230 | **Koordinator & Frontend Architect:** Desain global (CSS murni), navbar melayang, hero visual, silsilah pimpinan, integrasi & merge conflict resolver |
| ⚙️ | **Rofid Hidayatullah** | L200240211 | **Backend & DevOps:** Models, views, routing URLs, forms, admin panel, konfigurasi Docker & PostgreSQL |
| ⚙️ | **Fais Bayu Saputra** | L200240171 | **Backend Core:** Inisialisasi Django, models dasar, context processors, konfigurasi `settings.py`, dokumentasi |
| 📄 | **Fawaz Kholifatullah** | L200240228 | **Frontend Engineer:** Halaman Profil (`profile.html`), Halaman Ranting (`branches.html`), Halaman Amal Usaha (`charities.html`) |
| 📰 | **Hillary Aryodhito Juan M.Y** | L200240215 | **Frontend Engineer:** Halaman Berita (`articles.html`), Detail Berita, Halaman Agenda, Unduhan, dan Formulir Kontak |

---

## 🛠️ Arsitektur & Teknologi

| Lapisan | Teknologi | Keterangan |
|---|---|---|
| **Framework Web** | Django 6.0 | Arsitektur MVT (Model - View - Template) |
| **Bahasa** | Python 3.12 / 3.14 | Bahasa pemrograman utama |
| **Database** | PostgreSQL 17 (Docker) / SQLite | Database relasional dengan ORM bawaan |
| **Server Produksi** | Gunicorn 23.0 + WhiteNoise | WSGI Application Server & Static Compressor |
| **Kontainerisasi** | Docker & Docker Compose | Isolasi service `web` dan `db` |
| **Penyimpanan Media** | FileSystemStorage / S3-compatible | Didukung modul `django-storages` |
| **Styling** | Vanilla CSS3 (Custom Design System) | Flexbox, CSS Grid, Responsive Media Queries |

---

## 🚀 Panduan Menjalankan Proyek

### Opsi A: Menggunakan Docker (Direkomendasikan)

Pastikan Docker Desktop sudah terpasang dan berjalan di komputer Anda.

1. **Clone repositori:**
   ```bash
   git clone https://github.com/mgzalh/membagun-website-pcm-django-kelompok-k.git
   cd membagun-website-pcm-django-kelompok-k
   ```

2. **Jalankan container:**
   ```bash
   docker compose up --build -d
   ```

3. **Inisialisasi data & superuser:**
   ```bash
   docker compose exec web python manage.py init_render
   ```

4. **Buka di browser:**
   - **Website Publik:** [https://pcm-kottabarat.onrender.com/](https://pcm-kottabarat.onrender.com/)
   - **Panel Admin:** [https://pcm-kottabarat.onrender.com/admin/login/?next=/admin/](https://pcm-kottabarat.onrender.com/admin/login/?next=/admin/)

---

### Opsi B: Menjalankan Lokal (Menggunakan uv / Python)

1. **Pasang dependensi:**
   ```bash
   uv sync
   # atau jika menggunakan pip: pip install -r requirements.txt
   ```

2. **Jalankan migrasi database:**
   ```bash
   uv run python manage.py migrate
   ```

3. **Muat data awal & buat admin:**
   ```bash
   uv run python manage.py init_render
   ```

4. **Jalankan development server:**
   ```bash
   uv run python manage.py runserver
   ```
   Akses melalui `http://127.0.0.1:8000/`.

---

## 🔐 Kredensial Akun Admin Bawaan

| Parameter | Nilai |
|---|---|
| **URL Login** | `/admin/` (atau klik ikon gembok di footer) |
| **Username** | `admin` |
| **Password** | `AdminPCM2026!` |

---

## 📂 Struktur Direktori Proyek

```text
├── config/                  # Konfigurasi inti proyek Django
│   ├── settings.py          # Pengaturan database, static, media, security
│   ├── urls.py              # Root URL routing & media serving
│   └── wsgi.py              # Konfigurasi WSGI Gunicorn
├── website/                 # Django App utama PCM Kottabarat
│   ├── management/commands/ # Custom command (init_render, seed_pcm, sync_news)
│   ├── models.py            # 8 Model ORM (Profile, Leader, Council, Article, dll)
│   ├── views.py             # Logika view pemrosesan data & rendering
│   ├── forms.py             # ContactForm ModelForm
│   ├── admin.py             # Kustomisasi Django Admin Panel
│   └── context_processors.py# Variabel global untuk seluruh template
├── templates/               # Berkas template Django (HTML5 + DTL)
│   └── website/             # Template tiap halaman (home, profile, leaders, dll)
├── static/                  # Berkas statis aset (CSS murni, SVG, gambar)
├── compose.yaml             # Orkestrasi Docker Compose (Django + PostgreSQL 17)
├── Dockerfile               # Konfigurasi build image container
└── pyproject.toml           # Dependensi Python & metadata proyek
```

---

## 📄 Lisensi & Hak Cipta

Proyek ini dikembangkan untuk tujuan akademis pada mata kuliah **Pemrograman Web Berbasis Framework (TIF1336)** Universitas Muhammadiyah Surakarta.
