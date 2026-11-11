from .models import OrganizationProfile, RelatedLink


def organization_context(request):
    return {
        "organization": OrganizationProfile.objects.first(),
        "related_links": RelatedLink.objects.all(),
    }
