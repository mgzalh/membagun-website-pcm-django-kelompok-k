from django.contrib import admin

from .models import (
    Article,
    Branch,
    Charity,
    Council,
    Document,
    Event,
    IncomingMessage,
    Leader,
    OrganizationProfile,
    RelatedLink,
)

admin.site.site_header = "Admin Website PCM Kottabarat"
admin.site.site_title = "Admin PCM Kottabarat"
admin.site.index_title = "Pengelolaan konten website"


@admin.register(OrganizationProfile)
class OrganizationProfileAdmin(admin.ModelAdmin):
    list_display = ["name", "short_name", "official_email", "ktam_members"]

    def has_add_permission(self, request):
        return not OrganizationProfile.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Leader)
class LeaderAdmin(admin.ModelAdmin):
    list_display = ["name", "position", "tier", "period", "display_order"]
    search_fields = ["name", "position", "scope"]
    list_filter = ["tier", "period"]
    list_editable = ["display_order", "tier"]
    fieldsets = (
        (
            "Identitas Pimpinan",
            {
                "fields": ("name", "position", "tier", "period"),
                "description": "Pilih Tingkat Hierarki Silsilah agar posisi di bagan otomatis tepat.",
            },
        ),
        (
            "Detail & Bidang",
            {
                "fields": ("scope", "display_order"),
            },
        ),
        (
            "Foto Profil (Opsional)",
            {
                "fields": ("photo", "photo_credit"),
            },
        ),
    )


@admin.register(Council)
class CouncilAdmin(admin.ModelAdmin):
    list_display = ["name", "chairperson", "supervisor", "display_order"]
    search_fields = ["name", "chairperson", "supervisor", "members"]
    list_editable = ["display_order"]


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ["name", "chairperson"]
    search_fields = ["name", "chairperson"]


@admin.register(Charity)
class CharityAdmin(admin.ModelAdmin):
    list_display = ["name", "field"]
    search_fields = ["name", "description"]
    list_filter = ["field"]


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ["title", "status", "published_at"]
    search_fields = ["title", "summary", "body"]
    list_filter = ["status", "published_at"]
    prepopulated_fields = {"slug": ["title"]}
    date_hierarchy = "published_at"


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ["name", "starts_at", "place"]
    search_fields = ["name", "place"]
    list_filter = ["starts_at"]
    date_hierarchy = "starts_at"


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ["title", "uploaded_at"]
    search_fields = ["title", "description"]
    date_hierarchy = "uploaded_at"


@admin.register(IncomingMessage)
class IncomingMessageAdmin(admin.ModelAdmin):
    list_display = ["subject", "name", "email", "sent_at", "is_read"]
    search_fields = ["name", "email", "subject"]
    list_filter = ["is_read", "sent_at"]
    readonly_fields = [field.name for field in IncomingMessage._meta.fields]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return super().has_view_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(RelatedLink)
class RelatedLinkAdmin(admin.ModelAdmin):
    list_display = ["name", "url", "display_order"]
    search_fields = ["name", "url"]
