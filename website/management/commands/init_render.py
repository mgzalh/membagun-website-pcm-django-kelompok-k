import os
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Inisialisasi data awal dan superuser admin untuk deployment production (Render)"

    def handle(self, *args, **options):
        # 1. Jalankan seed data PCM
        self.stdout.write("Menjalankan seed data PCM...")
        try:
            call_command("seed_pcm")
            self.stdout.write(self.style.SUCCESS("Berhasil mengisi data PCM."))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f"Gagal seed_pcm: {e}"))

        # 2. Buat atau update Superuser Admin
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
