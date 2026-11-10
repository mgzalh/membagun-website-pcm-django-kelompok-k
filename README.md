# Website PCM Kottabarat

Website Django untuk tugas TIF1336. Proyek ini masih memerlukan konfirmasi pengurus PCM untuk melengkapi profil, sejarah, visi-misi, susunan pimpinan, daftar ranting, amal usaha, kontak resmi, foto, dan tautan resmi PWM. Data yang belum terverifikasi sengaja tidak diisi dengan perkiraan.

## Sumber data

| Data | Sumber | Tanggal diambil |
| --- | --- | --- |
| Kegiatan halalbihalal PCM dan PCA Kottabarat, nama Ketua PCM yang disebut dalam berita, dan konteks PRM/AUM | [Muhammadiyah Solo — Halalbihalal PCM-PCA Kottabarat](https://muhammadiyahsolo.com/20250427/merajut-kebersamaan-keluarga-besar-pcm-pca-kottabarat-berhalalbihalal-9846) | 12 November 2026 |
| Pengajian Syiar Muktamar bersama PCM Kottabarat, Banjarsari, dan Solo Utara | [Muhammadiyah Solo — Pengajian Syiar Muktamar](https://muhammadiyahsolo.com/20221017/pcm-kottabarat-banjarsari-dan-solo-utara-gelar-pengajian-syiar-muktamar-2438) | 12 November 2026 |
| Tautan wilayah PWM Jawa Tengah | [PWM Jawa Tengah](https://pwmjateng.com/) | 12 November 2026 |
| Logo Muhammadiyah | [Wikimedia Commons — Muhammadiyah.svg](https://commons.wikimedia.org/wiki/File:Muhammadiyah.svg), atribusi K. H. Siradj Dahlan, vektor oleh Hibensis, CC BY-SA 4.0 | 12 November 2026 |

Berita seed adalah ringkasan dengan tautan ke sumber. Foto berita tidak diambil karena gambar yang ditampilkan sumber saat pemeriksaan tidak dapat dipastikan sebagai foto kegiatan tersebut. Tambahkan hanya foto yang sudah memperoleh izin atau memiliki lisensi penggunaan yang sesuai, lalu cantumkan kreditnya.

## Menjalankan di laptop

Persyaratan: Python 3.12+, [uv](https://docs.astral.sh/uv/), Git.

```powershell
uv sync
uv run python manage.py migrate
uv run python manage.py seed_pcm
uv run python manage.py createsuperuser
uv run python manage.py runserver
```

Buka <http://127.0.0.1:8000/>. Panel admin tersedia di `/admin/`. SQLite digunakan jika `DATABASE_URL` kosong.

## Docker

```powershell
docker compose up --build
```

Buka <http://localhost:8000/>. Untuk mengisi data awal dan membuat akun admin:

```powershell
docker compose exec web python manage.py seed_pcm
docker compose exec web python manage.py createsuperuser
```

Compose menyediakan PostgreSQL 17 dan volume bernama agar database serta media tetap ada setelah container dihentikan. `docker compose down -v` menghapus volume tersebut, termasuk semua data database dan unggahan, sehingga gunakan hanya jika memang ingin menghapusnya.

## Konfigurasi

Salin `.env.example` menjadi `.env` bila perlu. Jangan memasukkan `.env` atau rahasia ke Git.

| Variabel | Kegunaan |
| --- | --- |
| `SECRET_KEY` | Kunci rahasia Django; wajib di produksi |
| `DEBUG` | `False` di produksi |
| `ALLOWED_HOSTS` | Host yang dipisahkan koma |
| `CSRF_TRUSTED_ORIGINS` | Origin HTTPS lengkap yang dipisahkan koma |
| `DATABASE_URL` | Kosong untuk SQLite; URL PostgreSQL untuk server |
| `CONN_MAX_AGE` | Umur koneksi; gunakan `0` untuk pooler transaksi |
| `AWS_STORAGE_BUCKET_NAME` | Opsional: aktifkan penyimpanan unggahan kompatibel S3 |
| `AWS_S3_REGION_NAME`, `AWS_S3_ENDPOINT_URL`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` | Pengaturan object storage opsional; isi lewat secret environment platform |

Static files disajikan WhiteNoise. Di platform dengan filesystem sementara, atur object storage untuk media sebelum menerima unggahan admin. Isi `AWS_S3_ENDPOINT_URL` dan kredensial sesuai penyedia S3 yang dipilih (misalnya Supabase Storage atau Cloudflare R2).

Saat deployment HTTPS, atur `SECURE_SSL_REDIRECT=True`, `SESSION_COOKIE_SECURE=True`, `CSRF_COOKIE_SECURE=True`, dan `SECURE_HSTS_SECONDS` setelah domain serta TLS berfungsi. Jangan mengaktifkan HSTS sebelum memastikan seluruh situs siap dilayani hanya melalui HTTPS.

## Pemeriksaan

```powershell
uv run python manage.py test
uv run python manage.py check --deploy
```

## Pengelolaan konten

Semua model dikelola lewat Django Admin. Berita harus berstatus **Terbit** dan tanggal terbitnya tidak boleh di masa depan agar tampil publik. Pesan masuk dari formulir kontak hanya dapat dibaca di admin. Profil organisasi berupa satu baris dan tidak dapat dihapus lewat admin.

## Status deployment

Belum dipilih platform produksi dan database cloud. Tetapkan pilihan kelompok, siapkan layanan object storage untuk media, lalu masukkan URL produksi dan alasan pemilihan ke bagian ini setelah deployment berhasil.
