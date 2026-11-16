from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import ContactForm
from .models import (
    Article,
    Branch,
    Charity,
    Council,
    Document,
    Event,
    Leader,
    OrganizationProfile,
)


def home(request):
    now = timezone.now()
    context = {
        "profile": OrganizationProfile.objects.first(),
        "branch_count": Branch.objects.count(),
        "charity_count": Charity.objects.count(),
        "latest_articles": Article.published.all()[:3],
        "upcoming_events": Event.objects.filter(starts_at__gte=now)[:3],
    }
    return render(request, "website/home.html", context)


def profile(request):
    return render(request, "website/profile.html", {"profile": OrganizationProfile.objects.first()})


def leaders(request):
    all_leaders = Leader.objects.all()
    context = {
        "advisors": all_leaders.filter(tier=Leader.Tier.ADVISOR),
        "chiefs": all_leaders.filter(tier=Leader.Tier.CHIEF),
        "vices": all_leaders.filter(tier=Leader.Tier.VICE),
        "officers": all_leaders.filter(tier=Leader.Tier.OFFICER),
        "plenos": all_leaders.filter(tier=Leader.Tier.PLENO),
        "councils": Council.objects.all(),
    }
    return render(request, "website/leaders.html", context)


def branches(request):
    return render(request, "website/branches.html", {"branches": Branch.objects.all()})


def charities(request):
    grouped = [
        (label, Charity.objects.filter(field=value))
        for value, label in Charity.Field.choices
    ]
    return render(request, "website/charities.html", {"grouped_charities": grouped})


def article_list(request):
    paginator = Paginator(Article.published.all(), 6)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(request, "website/articles.html", {"page_obj": page_obj})


def article_detail(request, slug):
    article = get_object_or_404(Article.published.all(), slug=slug)
    related_articles = Article.published.exclude(pk=article.pk)[:3]
    return render(
        request,
        "website/article_detail.html",
        {"article": article, "related_articles": related_articles},
    )


def agenda(request):
    now = timezone.now()
    context = {
        "upcoming_events": Event.objects.filter(starts_at__gte=now),
        "past_events": Event.objects.filter(starts_at__lt=now),
    }
    return render(request, "website/agenda.html", context)


def downloads(request):
    return render(request, "website/downloads.html", {"documents": Document.objects.all()})


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Pesan Anda berhasil dikirim. Terima kasih.")
            return redirect("website:contact")
    else:
        form = ContactForm()
    return render(
        request,
        "website/contact.html",
        {"form": form, "profile": OrganizationProfile.objects.first()},
    )
