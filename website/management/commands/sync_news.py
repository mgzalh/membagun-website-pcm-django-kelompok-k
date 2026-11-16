import re
import urllib.request
from datetime import datetime
from html import unescape
from urllib.parse import urlparse

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import slugify

from website.models import Article


class Command(BaseCommand):
    help = "Sinkronisasi berita terbaru seputar Kottabarat dari portal muhammadiyahsolo.com"

    def add_arguments(self, parser):
        parser.add_argument(
            "--limit",
            type=int,
            default=8,
            help="Jumlah maksimal artikel yang diambil (default: 8)",
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

        pattern = re.compile(
            r'<a[^>]+href="(?P<url>https://muhammadiyahsolo\.com/(?P<date>\d{8})/[^"]+)"[^>]*>'
            r'[\s\S]*?<h2 class="card-title[^"]*">(?P<title>[\s\S]*?)</h2>[\s\S]*?</a>'
            r'[\s\S]*?<p class="card-text[^"]*">(?P<summary>[\s\S]*?)</p>',
            re.IGNORECASE,
        )

        matches = list(pattern.finditer(html))
        self.stdout.write(f"Ditemukan {len(matches)} artikel terkait Kottabarat.")

        count = 0
        for m in matches[:limit]:
            art_url = m.group("url")
            date_str = m.group("date")
            title = unescape(re.sub(r"<[^>]+>", "", m.group("title")).strip())
            summary = unescape(re.sub(r"<[^>]+>", "", m.group("summary")).strip())

            # Parse tanggal
            try:
                pub_date = datetime.strptime(date_str, "%Y%m%d")
                pub_aware = timezone.make_aware(pub_date.replace(hour=8, minute=0))
            except Exception:
                pub_aware = timezone.now()

            # Buat slug dari judul
            base_slug = slugify(title)[:200] or f"berita-{date_str}"

            self.stdout.write(f"Mengunduh detail: {title[:50]}...")

            # Ambil detail halaman artikel untuk gambar & isi lengkap
            body_text, img_url = self._fetch_article_detail(art_url, headers)
            if not body_text:
                body_text = summary

            # Cari atau buat artikel
            article = Article.objects.filter(source_url=art_url).first()
            if not article:
                # Cek slug bentrok
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
                    cover_credit="Dokumentasi Muhammadiyah Solo",
                )
            else:
                article.title = title
                article.summary = summary
                article.body = body_text
                article.published_at = pub_aware
                article.status = Article.Status.PUBLISHED

            # Download cover image jika tersedia dan belum punya cover
            if img_url and not article.cover:
                img_data, img_filename = self._download_image(img_url, headers)
                if img_data:
                    article.cover.save(img_filename, ContentFile(img_data), save=False)

            article.save()
            count += 1
            self.stdout.write(self.style.SUCCESS(f"  [OK] Tersimpan: {title[:60]}"))

        self.stdout.write(
            self.style.SUCCESS(
                f"\nBerhasil menyinkronkan {count} berita resmi dari muhammadiyahsolo.com!"
            )
        )

    def _fetch_article_detail(self, url, headers):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=12) as resp:
                html = resp.read().decode("utf-8", errors="ignore")

            # Cari gambar utama di /files/
            # Utamakan gambar ukuran besar/sedang (bukan thumbnail 150x100 atau logo)
            img_candidates = re.findall(
                r'https://muhammadiyahsolo\.com/files/\d{4}/\d{2}/[^"\'\s>]+\.(?:jpg|jpeg|png|webp)',
                html,
                re.I,
            )
            img_url = None
            for cand in img_candidates:
                if "logo" not in cand.lower() and "150x100" not in cand and "370x" not in cand:
                    img_url = cand
                    break
            if not img_url and img_candidates:
                for cand in img_candidates:
                    if "logo" not in cand.lower():
                        img_url = cand
                        break

            # Cari paragraf konten
            paras = re.findall(r'<p[^>]*>([\s\S]*?)</p>', html)
            clean_paras = []
            for p in paras:
                text = unescape(re.sub(r'<[^>]+>', '', p).strip())
                if len(text) > 40 and not text.startswith("Baca juga") and not text.startswith("Editor:"):
                    clean_paras.append(text)

            body_text = "\n\n".join(clean_paras[:10])
            return body_text, img_url
        except Exception:
            return "", None

    def _download_image(self, url, headers):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = resp.read()
                path = urlparse(url).path
                filename = path.split("/")[-1]
                return data, filename
        except Exception:
            return None, ""
