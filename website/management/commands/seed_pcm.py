from datetime import datetime

from django.core.management.base import BaseCommand
from django.utils import timezone

from website.models import Article, Event, OrganizationProfile, RelatedLink


class Command(BaseCommand):
    help = "Mengisi database dengan profil dasar dan fakta PCM Kottabarat dari sumber terverifikasi."

    def handle(self, *args, **options):
        OrganizationProfile.objects.get_or_create(
            defaults={
                "name": "Pimpinan Cabang Muhammadiyah Kottabarat",
                "short_name": "PCM Kottabarat",
            }
        )
        self._article(
            title="Keluarga Besar PCM dan PCA Kottabarat Gelar Halalbihalal",
            slug="halalbihalal-pcm-pca-kottabarat-2025",
            published_at=datetime(2025, 4, 27, 12, 0),
            summary=(
                "PCM dan PCA Kottabarat mengadakan halalbihalal bertema "
                "“Merajut Kebersamaan, Meningkatkan Ukhuwah” bersama unsur PRM "
                "dan amal usaha di lingkungan Kottabarat."
            ),
            body=(
                "Kegiatan halalbihalal bersama PCM dan PCA Kottabarat berlangsung "
                "pada 27 April 2025 di aula SMP Muhammadiyah Program Khusus "
                "Kottabarat. Berita sumber menyebutkan kehadiran unsur PRM dan "
                "amal usaha di lingkungan Kottabarat, serta ajakan untuk "
                "menguatkan dakwah berkemajuan dan sinergi persyarikatan."
            ),
            source_url=(
                "https://muhammadiyahsolo.com/20250427/"
                "merajut-kebersamaan-keluarga-besar-pcm-pca-kottabarat-berhalalbihalal-9846"
            ),
        )
        self._article(
            title="PCM Kottabarat, Banjarsari, dan Solo Utara Gelar Pengajian Syiar Muktamar",
            slug="pengajian-syiar-muktamar-pcm-kottabarat-2022",
            published_at=datetime(2022, 10, 17, 12, 0),
            summary=(
                "PCM Kottabarat berkolaborasi dengan PCM Banjarsari dan Solo Utara "
                "menggelar pengajian syiar Muktamar ke-48 di Mangkubumen."
            ),
            body=(
                "Menurut berita yang diterbitkan 17 Oktober 2022, pengajian "
                "kolaboratif berlangsung sehari sebelumnya di Sasana Krida Warga "
                "Mangkubumen Banjarsari. Acara tersebut menyambut Muktamar "
                "Muhammadiyah dan Aisyiyah ke-48."
            ),
            source_url=(
                "https://muhammadiyahsolo.com/20221017/"
                "pcm-kottabarat-banjarsari-dan-solo-utara-gelar-pengajian-syiar-muktamar-2438"
            ),
        )
        self._event(
            name="Pengajian Syiar Muktamar Muhammadiyah dan Aisyiyah ke-48",
            starts_at=datetime(2022, 10, 16, 8, 0),
            place="Sasana Krida Warga Mangkubumen, Banjarsari",
            description="Agenda lampau berdasarkan berita Muhammadiyah Solo.",
            source_url=(
                "https://muhammadiyahsolo.com/20221017/"
                "pcm-kottabarat-banjarsari-dan-solo-utara-gelar-pengajian-syiar-muktamar-2438"
            ),
        )
        links = [
            ("PDM Kota Surakarta", "https://muhammadiyahsolo.com/", 1),
            ("PWM Jawa Tengah", "https://pwmjateng.com/", 2),
            ("PP Muhammadiyah", "https://muhammadiyah.or.id/", 3),
        ]
        for name, url, order in links:
            RelatedLink.objects.get_or_create(url=url, defaults={"name": name, "display_order": order})
        self.stdout.write(self.style.SUCCESS("Data awal PCM Kottabarat berhasil disiapkan."))
        self.stdout.write(
            self.style.WARNING(
                "Profil, pimpinan, ranting, amal usaha, kontak, dan tautan PWM perlu "
                "dilengkapi setelah diverifikasi dari pengurus atau sumber resmi."
            )
        )

    @staticmethod
    def _article(*, title, slug, published_at, summary, body, source_url):
        Article.objects.update_or_create(
            slug=slug,
            defaults={
                "title": title,
                "published_at": timezone.make_aware(published_at),
                "summary": summary,
                "body": body,
                "status": Article.Status.PUBLISHED,
                "source_name": "Muhammadiyah Solo",
                "source_url": source_url,
            },
        )

    @staticmethod
    def _event(*, name, starts_at, place, description, source_url):
        Event.objects.get_or_create(
            name=name,
            starts_at=timezone.make_aware(starts_at),
            defaults={
                "place": place,
                "description": description,
                "source_url": source_url,
            },
        )
