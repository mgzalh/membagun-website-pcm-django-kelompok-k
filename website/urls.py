from django.urls import path

from . import views

app_name = "website"

urlpatterns = [
    path("", views.home, name="home"),
    path("profil/", views.profile, name="profile"),
    path("pimpinan/", views.leaders, name="leaders"),
    path("ranting/", views.branches, name="branches"),
    path("amal-usaha/", views.charities, name="charities"),
    path("berita/", views.article_list, name="articles"),
    path("berita/<slug:slug>/", views.article_detail, name="article_detail"),
    path("agenda/", views.agenda, name="agenda"),
    path("unduhan/", views.downloads, name="downloads"),
    path("kontak/", views.contact, name="contact"),
]
