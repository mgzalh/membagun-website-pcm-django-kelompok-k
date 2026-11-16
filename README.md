# Website PCM Kottabarat

Website berbasis Django untuk memenuhi tugas **TIF1336**.

Proyek ini masih memerlukan konfirmasi pengurus PCM untuk melengkapi profil, sejarah, visi-misi, susunan pimpinan, daftar ranting, amal usaha, kontak resmi, foto, dan tautan resmi PWM. Data yang belum terverifikasi sengaja tidak diisi dengan perkiraan.

---

## 📚 Sumber Data

| Data | Sumber | Tanggal Diambil |
|---|---|---|
| Kegiatan halalbihalal PCM dan PCA Kottabarat, nama Ketua PCM yang disebut dalam berita, dan konteks PRM/AUM | [Muhammadiyah Solo — Halalbihalal PCM-PCA Kottabarat](https://muhammadiyahsolo.com/20250427/merajut-kebersamaan-keluarga-besar-pcm-pca-kottabarat-berhalalbihalal-9846) | 12 November 2026 |
| Pengajian Syiar Muktamar bersama PCM Kottabarat, Banjarsari, dan Solo Utara | [Muhammadiyah Solo — Pengajian Syiar Muktamar](https://muhammadiyahsolo.com/20221017/pcm-kottabarat-banjarsari-dan-solo-utara-gelar-pengajian-syiar-muktamar-2438) | 12 November 2026 |
| Tautan wilayah PWM Jawa Tengah | [PWM Jawa Tengah](https://pwmjateng.com/) | 12 November 2026 |
| Logo Muhammadiyah | [Wikimedia Commons — Muhammadiyah.svg](https://commons.wikimedia.org/wiki/File:Muhammadiyah.svg), atribusi K. H. Siradj Dahlan, vektor oleh Hibensis, CC BY-SA 4.0 | 12 November 2026 |

**Catatan sumber data:**
- Berita seed merupakan ringkasan yang dilengkapi tautan ke sumber asli.
- Foto berita tidak digunakan karena gambar yang ditampilkan sumber saat pemeriksaan tidak dapat dipastikan sebagai foto kegiatan tersebut.
- Tambahkan hanya foto yang sudah memperoleh izin atau memiliki lisensi penggunaan yang sesuai, lalu cantumkan kreditnya.

---

## 💻 Menjalankan di Laptop

### Persyaratan

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)
- Git

### Langkah Instalasi

Jalankan perintah berikut melalui terminal:

```powershell
uv sync
uv run python manage.py migrate
uv run python manage.py seed_pcm
uv run python manage.py createsuperuser
uv run python manage.py runserver
```

Setelah server berjalan, buka alamat berikut:

- **Website:** http://127.0.0.1:8000/
- **Admin:** http://127.0.0.1:8000/admin/

SQLite digunakan sebagai database default jika `DATABASE_URL` kosong.

---

## 🐳 Menjalankan dengan Docker

Jalankan perintah berikut untuk membangun dan menjalankan aplikasi:

```powershell
docker compose up --build
```

Buka website melalui:

http://localhost:8000/

### Mengisi Data Awal dan Membuat Admin

Jalankan perintah berikut:

```powershell
docker compose exec web python manage.py seed_pcm
docker compose exec web python manage.py createsuperuser
```

**Informasi Docker:**
- Docker Compose menyediakan PostgreSQL 17.
- Database dan media menggunakan volume bernama agar data tetap tersimpan setelah container dihentikan.
- Perintah `docker compose down -v` akan menghapus volume, termasuk seluruh data database dan unggahan. Gunakan hanya jika memang ingin menghapusnya.

---

## ⚙️ Konfigurasi

Salin file `.env.example` menjadi `.env` jika diperlukan.

Jangan memasukkan file `.env` atau informasi rahasia ke GitHub.

| Variabel | Kegunaan |
|---|---|
| `SECRET_KEY` | Kunci rahasia Django; wajib di produksi |
| `DEBUG` | Gunakan `False` di produksi |
| `ALLOWED_HOSTS` | Host yang dipisahkan dengan koma |
| `CSRF_TRUSTED_ORIGINS` | Origin HTTPS lengkap yang dipisahkan dengan koma |
| `DATABASE_URL` | Kosong untuk SQLite atau URL PostgreSQL untuk server |
| `CONN_MAX_AGE` | Umur koneksi; gunakan `0` untuk pooler transaksi |
| `AWS_STORAGE_BUCKET_NAME` | Opsional, mengaktifkan penyimpanan unggahan kompatibel S3 |
| `AWS_S3_REGION_NAME`, `AWS_S3_ENDPOINT_URL`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` | Pengaturan object storage opsional melalui secret environment platform |

### Static Files dan Media

- Static files disajikan menggunakan WhiteNoise.
- Pada platform dengan filesystem sementara, atur object storage untuk media sebelum menerima unggahan melalui admin.
- Isi `AWS_S3_ENDPOINT_URL` dan kredensial sesuai penyedia S3 yang digunakan, misalnya Supabase Storage atau Cloudflare R2.

### Pengaturan Keamanan Produksi

Saat deployment menggunakan HTTPS, atur konfigurasi berikut setelah domain dan TLS berfungsi:

```python
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS
```

Jangan mengaktifkan HSTS sebelum memastikan seluruh situs siap dilayani hanya melalui HTTPS.

---

## 🧪 Pemeriksaan Aplikasi

Untuk menjalankan pengujian dan pemeriksaan konfigurasi Django, gunakan:

```powershell
uv run python manage.py test
uv run python manage.py check --deploy
```

---

## 📝 Pengelolaan Konten

Seluruh model dikelola melalui **Django Admin**.

Beberapa ketentuan pengelolaan konten:

- Berita harus berstatus **Terbit** dan tanggal terbitnya tidak boleh di masa depan agar tampil di halaman publik.
- Pesan masuk dari formulir kontak hanya dapat dibaca melalui admin.
- Profil organisasi berupa satu baris dan tidak dapat dihapus melalui admin.

---

## 🚀 Status Deployment

Platform produksi dan database cloud belum dipilih.

Tahapan yang masih perlu dilakukan:

1. Menetapkan pilihan platform deployment bersama kelompok.
2. Menyiapkan layanan object storage untuk menyimpan media.
3. Melakukan deployment aplikasi.
4. Mengisi URL produksi dan alasan pemilihan platform setelah deployment berhasil.

---

**Project:** Website PCM Kottabarat  
**Framework:** Django  
**Mata Kuliah:** TIF1336