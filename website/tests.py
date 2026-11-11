from datetime import timedelta

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.test import RequestFactory
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Article, IncomingMessage, OrganizationProfile


class PublicPageTests(TestCase):
    def test_public_pages_render(self):
        names = [
            "home",
            "profile",
            "leaders",
            "branches",
            "charities",
            "articles",
            "agenda",
            "downloads",
            "contact",
        ]
        for name in names:
            with self.subTest(page=name):
                response = self.client.get(reverse(f"website:{name}"))
                self.assertEqual(response.status_code, 200)

    def test_article_detail_is_available_when_published(self):
        article = Article.objects.create(
            title="Berita terbit",
            status=Article.Status.PUBLISHED,
            published_at=timezone.now() - timedelta(days=1),
        )
        response = self.client.get(reverse("website:article_detail", args=[article.slug]))
        self.assertEqual(response.status_code, 200)

    def test_draft_article_returns_404(self):
        article = Article.objects.create(title="Berita draf")
        response = self.client.get(reverse("website:article_detail", args=[article.slug]))
        self.assertEqual(response.status_code, 404)

    def test_future_article_returns_404(self):
        article = Article.objects.create(
            title="Berita masa depan",
            status=Article.Status.PUBLISHED,
            published_at=timezone.now() + timedelta(days=1),
        )
        response = self.client.get(reverse("website:article_detail", args=[article.slug]))
        self.assertEqual(response.status_code, 404)

    def test_article_list_has_six_items_per_page(self):
        for index in range(7):
            Article.objects.create(
                title=f"Berita {index}",
                status=Article.Status.PUBLISHED,
                published_at=timezone.now() - timedelta(days=index + 1),
            )
        first_page = self.client.get(reverse("website:articles"))
        second_page = self.client.get(reverse("website:articles"), {"page": 2})
        self.assertEqual(first_page.context["page_obj"].paginator.per_page, 6)
        self.assertEqual(len(first_page.context["page_obj"].object_list), 6)
        self.assertEqual(len(second_page.context["page_obj"].object_list), 1)

    def test_contact_form_saves_message(self):
        response = self.client.post(
            reverse("website:contact"),
            {
                "name": "Warga Kottabarat",
                "email": "warga@example.com",
                "subject": "Informasi kegiatan",
                "message": "Mohon informasi jadwal kegiatan mendatang.",
            },
        )
        self.assertRedirects(response, reverse("website:contact"))
        self.assertEqual(IncomingMessage.objects.count(), 1)

    def test_invalid_contact_message_is_not_saved(self):
        response = self.client.post(
            reverse("website:contact"),
            {
                "name": "A",
                "email": "invalid",
                "subject": "Tanya",
                "message": "singkat",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(IncomingMessage.objects.count(), 0)

    def test_duplicate_article_titles_get_unique_slugs(self):
        first = Article.objects.create(title="Judul Sama")
        second = Article.objects.create(title="Judul Sama")
        self.assertNotEqual(first.slug, second.slug)

    def test_organization_profile_cannot_be_duplicated(self):
        OrganizationProfile.objects.create()
        with self.assertRaises(ValueError):
            OrganizationProfile.objects.create()

    def test_contact_messages_are_read_only_in_admin(self):
        model_admin = admin.site._registry[IncomingMessage]
        request = RequestFactory().get("/admin/")
        request.user = get_user_model()(is_staff=True, is_superuser=True)
        self.assertFalse(model_admin.has_add_permission(request))
        self.assertTrue(model_admin.has_change_permission(request))
        self.assertFalse(model_admin.has_delete_permission(request))
        self.assertEqual(
            set(model_admin.get_readonly_fields(request)),
            {field.name for field in IncomingMessage._meta.fields},
        )
