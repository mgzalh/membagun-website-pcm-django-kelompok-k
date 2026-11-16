from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class OrganizationProfile(models.Model):
    name = models.CharField(max_length=180, default="PCM Kottabarat")
    short_name = models.CharField(max_length=80, default="PCM Kottabarat")
    tagline = models.CharField(max_length=200, blank=True)
    about = models.TextField(blank=True)
    history = models.TextField(blank=True)
    vision = models.TextField(blank=True)
    missions = models.TextField(blank=True, help_text="Satu butir misi per baris.")
    office_address = models.TextField(blank=True)
    official_phone = models.CharField(max_length=40, blank=True)
    official_email = models.EmailField(blank=True)
    ktam_members = models.PositiveIntegerField(null=True, blank=True)
    hero_image = models.ImageField(upload_to="profile/", blank=True)
    hero_image_credit = models.CharField(max_length=180, blank=True)

    class Meta:
        verbose_name = "Profil organisasi"
        verbose_name_plural = "Profil organisasi"

    def __str__(self):
        return self.short_name

    def save(self, *args, **kwargs):
        if OrganizationProfile.objects.exclude(pk=self.pk).exists():
            raise ValueError("Profil organisasi hanya boleh memiliki satu baris.")
        return super().save(*args, **kwargs)

    @property
    def mission_list(self):
        return [mission.strip() for mission in self.missions.splitlines() if mission.strip()]


class Leader(models.Model):
    class Tier(models.TextChoices):
        ADVISOR = "penasehat", "1. Dewan Penasehat"
        CHIEF = "ketua", "2. Pucuk Pimpinan (Ketua Cabang)"
        VICE = "wakil", "3. Wakil Ketua Cabang"
        OFFICER = "harian", "4. Sekretariat & Kebendaharaan"
        PLENO = "pleno", "5. Anggota Pleno Cabang"

    tier = models.CharField(
        max_length=20,
        choices=Tier.choices,
        default=Tier.PLENO,
        verbose_name="Tingkat Hierarki Silsilah",
    )
    name = models.CharField(max_length=160, verbose_name="Nama Lengkap")
    position = models.CharField(max_length=120, verbose_name="Jabatan Resmi")
    period = models.CharField(max_length=40, blank=True, default="2022 - 2027", verbose_name="Periode")
    scope = models.CharField(
        max_length=160,
        blank=True,
        verbose_name="Bidang Koordinasi / Keterangan",
        help_text="Contoh: Koordinator Bidang: Tabligh, Tarjih, Ekonomi",
    )
    photo = models.ImageField(upload_to="leaders/", blank=True, verbose_name="Foto Pimpinan")
    photo_credit = models.CharField(max_length=180, blank=True, verbose_name="Kredit Foto")
    display_order = models.PositiveIntegerField(default=0, verbose_name="Urutan Tampilan")

    class Meta:
        ordering = ["display_order", "name"]
        verbose_name = "Pimpinan"
        verbose_name_plural = "Pimpinan"

    def __str__(self):
        return f"{self.name} — {self.position}"


class Council(models.Model):
    name = models.CharField(max_length=160, verbose_name="Nama Majelis / Lembaga")
    supervisor = models.CharField(max_length=160, blank=True, verbose_name="Supervisor Pimpinan")
    chairperson = models.CharField(max_length=160, verbose_name="Ketua Majelis")
    members = models.TextField(
        blank=True,
        help_text="Tulis satu nama anggota per baris",
        verbose_name="Daftar Anggota Majelis",
    )
    display_order = models.PositiveIntegerField(default=0, verbose_name="Urutan Tampilan")

    class Meta:
        ordering = ["display_order", "name"]
        verbose_name = "Majelis / Lembaga"
        verbose_name_plural = "Majelis & Lembaga"

    def __str__(self):
        return self.name

    @property
    def member_list(self):
        return [m.strip() for m in self.members.splitlines() if m.strip()]


class Branch(models.Model):
    name = models.CharField(max_length=160)
    chairperson = models.CharField(max_length=160, blank=True)
    address = models.TextField(blank=True)
    official_phone = models.CharField(max_length=40, blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Ranting"
        verbose_name_plural = "Ranting"

    def __str__(self):
        return self.name


class Charity(models.Model):
    class Field(models.TextChoices):
        EDUCATION = "pendidikan", "Pendidikan"
        HEALTH = "kesehatan", "Kesehatan"
        SOCIAL = "sosial", "Sosial"
        ECONOMY = "ekonomi", "Ekonomi"

    name = models.CharField(max_length=180)
    field = models.CharField(max_length=20, choices=Field.choices)
    description = models.TextField(blank=True)
    address = models.TextField(blank=True)
    image = models.ImageField(upload_to="charities/", blank=True)
    image_credit = models.CharField(max_length=180, blank=True)

    class Meta:
        ordering = ["field", "name"]
        verbose_name = "Amal usaha"
        verbose_name_plural = "Amal usaha"

    def __str__(self):
        return self.name


class PublishedArticleManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Article.Status.PUBLISHED, published_at__lte=timezone.now())


class Article(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draf"
        PUBLISHED = "published", "Terbit"

    title = models.CharField(max_length=220)
    slug = models.SlugField(max_length=240, unique=True, blank=True)
    summary = models.TextField(blank=True)
    body = models.TextField(blank=True)
    cover = models.ImageField(upload_to="news/", blank=True)
    published_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.DRAFT)
    source_name = models.CharField(max_length=160, blank=True)
    source_url = models.URLField(blank=True)
    cover_credit = models.CharField(max_length=180, blank=True)

    objects = models.Manager()
    published = PublishedArticleManager()

    class Meta:
        ordering = ["-published_at"]
        verbose_name = "Berita"
        verbose_name_plural = "Berita"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)[:220] or "berita"
            candidate = base_slug
            suffix = 2
            while Article.objects.filter(slug=candidate).exclude(pk=self.pk).exists():
                candidate = f"{base_slug[:230 - len(str(suffix))]}-{suffix}"
                suffix += 1
            self.slug = candidate
        return super().save(*args, **kwargs)


class Event(models.Model):
    name = models.CharField(max_length=200)
    starts_at = models.DateTimeField()
    place = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    source_url = models.URLField(blank=True)

    class Meta:
        ordering = ["starts_at"]
        verbose_name = "Agenda"
        verbose_name_plural = "Agenda"

    def __str__(self):
        return self.name


class Document(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to="documents/")
    uploaded_at = models.DateField(default=timezone.localdate)

    class Meta:
        ordering = ["-uploaded_at", "title"]
        verbose_name = "Dokumen"
        verbose_name_plural = "Dokumen"

    def __str__(self):
        return self.title


class IncomingMessage(models.Model):
    name = models.CharField(max_length=160)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-sent_at"]
        verbose_name = "Pesan masuk"
        verbose_name_plural = "Pesan masuk"

    def __str__(self):
        return f"{self.subject} — {self.name}"


class RelatedLink(models.Model):
    name = models.CharField(max_length=120)
    url = models.URLField()
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "name"]
        verbose_name = "Tautan terkait"
        verbose_name_plural = "Tautan terkait"

    def __str__(self):
        return self.name
