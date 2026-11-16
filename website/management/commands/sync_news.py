import re
import urllib.request
from datetime import datetime
from html import unescape
from urllib.parse import unquote, urlparse

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import slugify

from website.models import Article


class Command(BaseCommand):
    help = "Sinkronisasi berita terbaru seputar Kottabarat dari portal muhammadiyahsolo.com beserta foto aslinya."

    def add_arguments(self, parser):
        parser.add_argument(
            "--limit",
            type=int,
            default=6,
            help="Jumlah maksimal artikel yang diambil (default: 6)",
        )

    def handle(self, *args, **options):
        limit = options["limit"]
        search_url = "https://muhammadiyahsolo.com/?s=kottabarat"
        self.stdout.write(f"Mengambil berita dari: {search_url}...")

        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        req = urllib.request.Request(search_url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                html = resp.read().decode("utf-8", errors="ignore")
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Gagal mengakses portal: {e}"))
            return

        # Ambil artikel dari kartu hasil pencarian
        cards = re.findall(
            r'<a[^>]+href="(?P<url>https://muhammadiyahsolo\.com/(?P<date>\d{8})/[^"]+)"[^>]*>'
            r'\s*<h2 class="card-title[^"]*">(?P<title>.*?)</h2>\s*</a>',
            html,
            re.DOTALL,
        )

        self.stdout.write(f"Ditemukan {len(cards)} artikel terkait Kottabarat.")

        count = 0
        for art_url, date_str, raw_title in cards[:limit]:
            title = unescape(re.sub(r"<[^>]+>", "", raw_title)).strip()

            # Parse tanggal publikasi
            try:
                pub_date = datetime.strptime(date_str, "%Y%m%d")
                pub_aware = timezone.make_aware(pub_date.replace(hour=8, minute=0))
            except Exception:
                pub_aware = timezone.now()

            self.stdout.write(f"\nMemproses: {title[:55]}...")

            # Ambil detail halaman artikel untuk isi lengkap dan foto asli
            summary, body_text, img_url = self._fetch_article_detail(art_url, headers)

            # Cek artikel di database
            article = Article.objects.filter(source_url=art_url).first()
            if not article:
                base_slug = slugify(title)[:200] or f"berita-{date_str}"
                slug = base_slug
                idx = 1
                while Article.objects.filter(slug=slug).exists():
                    slug = f"{base_slug[:190]}-{idx}"
                    idx += 1
                article = Article(
                    title=title,
                    slug=slug,
                    summary=summary,
                    body=body_text,
                    published_at=pub_aware,
                    status=Article.Status.PUBLISHED,
                    source_name="Muhammadiyah Solo",
                    source_url=art_url,
                    cover_credit="Dokumentasi Humas / Muhammadiyah Solo",
                )
            else:
                article.title = title
                article.summary = summary
                article.body = body_text
                article.published_at = pub_aware
                article.status = Article.Status.PUBLISHED

            # Download foto asli jika ada
            if img_url:
                self.stdout.write(f"  Mengunduh foto: {img_url}...")
                img_data, img_filename = self._download_image(img_url, headers)
                if img_data:
                    # Simpan foto asli sebagai cover
                    article.cover.save(img_filename, ContentFile(img_data), save=False)
                    self.stdout.write(self.style.SUCCESS(f"  [Foto OK] {img_filename}"))
                else:
                    self.stdout.write(self.style.WARNING("  [Foto Gagal diunduh]"))

            article.save()
            count += 1
            self.stdout.write(self.style.SUCCESS(f"  [Berita Tersimpan] ID: {article.pk}"))

        self.stdout.write(
            self.style.SUCCESS(
                f"\nBerhasil menyinkronkan {count} berita + FOTO ASLI dari muhammadiyahsolo.com!"
            )
        )

    def _fetch_article_detail(self, url, headers):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=12) as resp:
                html = resp.read().decode("utf-8", errors="ignore")

            # 1. Cari foto asli dari og:image (socmed-image.php?src=...)
            og_match = re.search(
                r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)["\']',
                html,
                re.I,
            )
            img_url = None
            if og_match:
                og_content = og_match.group(1)
                src_match = re.search(r'src=([^&"\']+)', og_content)
                if src_match:
                    img_url = unquote(src_match.group(1))
                elif "favicon" not in og_content and "logo" not in og_content and "default.jpg" not in og_content:
                    img_url = og_content

            # Jika og:image tidak dapat, cari dari tag img di dalam artikel
            if not img_url:
                imgs = re.findall(
                    r'https://muhammadiyahsolo\.com/files/\d{4}/\d{2}/[^"\'\s>]+\.(?:jpg|jpeg|png|webp)',
                    html,
                    re.I,
                )
                for im in imgs:
                    if "logo" not in im.lower() and "150x100" not in im:
                        img_url = im
                        break

            # 2. Cari paragraf konten
            paras = re.findall(r'<p[^>]*>([\s\S]*?)</p>', html)
            clean_paras = []
            for p in paras:
                text = unescape(re.sub(r"<[^>]+>", "", p).strip())
                if len(text) > 40 and not text.startswith("Baca juga") and not text.startswith("Editor:"):
                    clean_paras.append(text)

            summary = clean_paras[0] if clean_paras else ""
            body_text = "\n\n".join(clean_paras)
            return summary, body_text, img_url
        except Exception as e:
            return "", "", None

    def _download_image(self, url, headers):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=12) as resp:
                data = resp.read()
                path = urlparse(url).path
                filename = path.split("/")[-1]
                return data, filename
        except Exception:
            return None, ""
