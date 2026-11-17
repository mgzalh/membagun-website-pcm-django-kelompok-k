import os
from datetime import timedelta
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone

from website.models import Article, Event


class Command(BaseCommand):
    help = "Inisialisasi data awal, berita, agenda, dan superuser admin untuk deployment production (Render)"

    def handle(self, *args, **options):
        # 1. Jalankan seed data PCM jika database masih kosong
        if Charity.objects.count() == 0 or Leader.objects.count() == 0:
            self.stdout.write("Menjalankan inisialisasi data PCM...")
            try:
                call_command("seed_pcm")
                self.stdout.write(self.style.SUCCESS("Berhasil mengisi data PCM dasar."))
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"Gagal seed_pcm: {e}"))
        else:
            self.stdout.write(self.style.SUCCESS("Data PCM sudah ada di database, lewati seed untuk menjaga data admin."))

        # 2. Seed Agenda Kegiatan yang rapi dan sesuai nama hari/waktunya
        Event.objects.all().delete()
        tz = timezone.get_current_timezone()
        events = [
            (
                "Kajian Rutin Ahad Pagi PCM Kottabarat",
                timezone.datetime(2026, 11, 22, 6, 0, tzinfo=tz),
                "Masjid Kottabarat Surakarta",
                "Kajian rutin pencerahan keislaman dan keumatan menghadirkan narasumber dari PP Muhammadiyah.",
            ),
            (
                "Rapat Koordinasi Majelis Dikdasmen & Amal Usaha",
                timezone.datetime(2026, 11, 25, 9, 0, tzinfo=tz),
                "Gedung Dakwah PCM Kottabarat Lt. 2",
                "Koordinasi persiapan tahun ajaran baru sekolah unggulan PK Kottabarat.",
            ),
            (
                "Baitul Arqam Pimpinan & Kader Ranting Kottabarat",
                timezone.datetime(2026, 11, 28, 8, 0, tzinfo=tz),
                "Balai Diklat PCM Kottabarat",
                "Penguatan ideologi bermuhammadiyah dan peningkatan kepemimpinan kader persyarikatan.",
            ),
        ]
        for name, starts_at, place, desc in events:
            Event.objects.create(name=name, starts_at=starts_at, place=place, description=desc)
        self.stdout.write(self.style.SUCCESS("Berhasil memperbarui 3 agenda kegiatan yang rapi."))

        # 3. Sinkronisasi Berita (sync_news) atau buat fallback artikel
        self.stdout.write("Menyinkronkan berita...")
        try:
            call_command("sync_news", limit=6)
            self.stdout.write(self.style.SUCCESS("Berhasil sinkronisasi berita dari portal resmi."))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f"Gagal sync_news otomatis: {e}"))

        # Fallback jika berita masih kosong
        if Article.objects.filter(status=Article.Status.PUBLISHED).count() == 0:
            now = timezone.now()
            articles = [
                (
                    "Semarak Milad Muhammadiyah ke-112 di Cabang Kottabarat",
                    "milad-muhammadiyah-112-kottabarat",
                    "Warga persyarikatan Muhammadiyah Kottabarat menggelar pawai ta'aruf dan syiar dakwah.",
                    "Pimpinan Cabang Muhammadiyah (PCM) Kottabarat menggelar rangkaian kegiatan semarak Milad Muhammadiyah ke-112 dengan berbagai agenda syiar keumatan dan bakti sosial di seluruh ranting.",
                    now - timedelta(days=1),
                ),
                (
                    "SD Muhammadiyah PK Kottabarat Raih Prestasi Tingkat Nasional",
                    "prestasi-sd-muhammadiyah-pk-kottabarat",
                    "Siswa berprestasi dari SD Muhammadiyah PK kembali mengukir prestasi gemilang.",
                    "Siswa-siswi SD Muhammadiyah Program Khusus Kottabarat kembali menorehkan prestasi membanggakan pada ajang olimpiade sains dan tahfidz tingkat nasional tahun 2026.",
                    now - timedelta(days=3),
                ),
                (
                    "Lazismu Kottabarat Salurkan Bantuan Pemberdayaan UMKM Syariah",
                    "lazismu-kottabarat-salurkan-bantuan-umkm",
                    "Program pemberdayaan mustahik menjadi muzakki terus digencarkan oleh Lazismu.",
                    "Kantor Layanan Lazismu PCM Kottabarat kembali menyalurkan bantuan modal usaha syariah bagi para pelaku UMKM binaan di wilayah ranting Mangkubumen dan Sumber.",
                    now - timedelta(days=5),
                ),
            ]
            for title, slug, excerpt, body, pub_at in articles:
                Article.objects.create(
                    title=title,
                    slug=slug,
                    excerpt=excerpt,
                    body=body,
                    status=Article.Status.PUBLISHED,
                    published_at=pub_at,
                )
            self.stdout.write(self.style.SUCCESS("Berhasil mengisi fallback artikel berita."))

        # 4. Buat atau update Superuser Admin
        username = os.environ.get("ADMIN_USERNAME", "admin")
        password = os.environ.get("ADMIN_PASSWORD", "AdminPCM2026!")
        email = os.environ.get("ADMIN_EMAIL", "admin@pcmkotabarat.org")

        User = get_user_model()
        user, created = User.objects.get_or_create(
            username=username,
            defaults={"email": email, "is_staff": True, "is_superuser": True},
        )
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save()

        if created:
            self.stdout.write(self.style.SUCCESS(f"Superuser '{username}' berhasil dibuat!"))
        else:
            self.stdout.write(self.style.SUCCESS(f"Superuser '{username}' berhasil diperbarui!"))
