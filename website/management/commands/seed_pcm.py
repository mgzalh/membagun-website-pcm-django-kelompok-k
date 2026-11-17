from datetime import datetime

from django.core.management.base import BaseCommand
from django.utils import timezone

from website.models import Branch, Charity, Leader, OrganizationProfile, RelatedLink


class Command(BaseCommand):
    help = "Mengisi database dengan profil resmi, pimpinan hierarkis, ranting, amal usaha, dan tautan resmi PCM Kottabarat."

    def handle(self, *args, **options):
        # 1. Profil Organisasi Resmi
        prof, _ = OrganizationProfile.objects.get_or_create(
            defaults={
                "name": "Pimpinan Cabang Muhammadiyah Kottabarat",
                "short_name": "PCM Kottabarat",
            }
        )
        prof.office_address = "Jl. Dr. Muwardi No. 24, Surakarta"
        prof.official_phone = "(0271) 714422"
        prof.official_email = "pcm.kottabarat@gmail.com"
        prof.tagline = "Gerakan Islam Berkemajuan Menuju Masyarakat Madani di Kottabarat"
        prof.about = (
            "Pimpinan Cabang Muhammadiyah (PCM) Kottabarat merupakan struktur persyarikatan "
            "di bawah PDM Kota Surakarta yang mengelola dakwah, pendidikan unggulan, dan layanan kemasyarakatan."
        )
        prof.ktam_members = None
        prof.save()

        # 2. Tautan Persyarikatan (Footer)
        RelatedLink.objects.all().delete()
        links = [
            ("PDM Kota Surakarta", "https://muhammadiyahsolo.com/", 1),
            ("PWM Jawa Tengah", "https://pwmjateng.com/", 2),
            ("PP Muhammadiyah", "https://muhammadiyah.or.id/", 3),
        ]
        for name, url, order in links:
            RelatedLink.objects.create(name=name, url=url, display_order=order)

        # 3. Silsilah Pimpinan Lengkap & Hierarkis (2022 - 2027)
        Leader.objects.all().delete()
        leaders = [
            # Tier: penasehat
            ("Drs. H. Marpuji Ali, M.Si.", "Penasehat 1", "penasehat", "2022 - 2027", "", 1),
            ("H. Sjamsuddin Dahlan", "Penasehat 2", "penasehat", "2022 - 2027", "", 2),
            ("Dr. Muhammad Ali, M.Pd", "Penasehat 3", "penasehat", "2022 - 2027", "", 3),
            # Tier: ketua
            ("Joko Susilo, S.TP., S.Pd.I., M.Pd", "Ketua Cabang", "ketua", "2022 - 2027", "", 10),
            # Tier: wakil
            ("Saifudin, SP", "Wakil Ketua I", "wakil", "2022 - 2027", "Koordinator Bidang: Tabligh, Tarjih, Ekonomi", 20),
            ("H. Kartono, S.Pd., M.Pd", "Wakil Ketua II", "wakil", "2022 - 2027", "Koordinator Bidang: Dikdasmen, Kader, Kesos", 21),
            # Tier: harian
            ("Retno Sugiyanto, S.Pd", "Sekretaris", "harian", "2022 - 2027", "", 30),
            ("Muhdiyatmoko, S.Pd., M.Pd", "Wakil Sekretaris", "harian", "2022 - 2027", "", 31),
            ("Mukseto", "Bendahara", "harian", "2022 - 2027", "", 32),
            ("Yusuf Aris Kurniawan, S.Pi", "Wakil Bendahara", "harian", "2022 - 2027", "", 33),
            # Tier: pleno
            ("H. Suwardi, S.Ag, M.Si", "Anggota Pleno", "pleno", "2022 - 2027", "", 40),
            ("Lasur Suryadi", "Anggota Pleno", "pleno", "2022 - 2027", "", 41),
        ]
        for name, pos, tier, period, scope, order in leaders:
            Leader.objects.create(
                name=name,
                position=pos,
                tier=tier,
                period=period,
                scope=scope,
                display_order=order,
            )

        # 4. Ranting (PRM) Resmi
        Branch.objects.all().delete()
        branches = [
            ("PRM Mangkubumen", "Lasur Suryadi", "Jl. Kenanga II/20 A Rt.01/V Mangkubumen Surakarta", ""),
            ("PRM Sumber Barat", "Retno Sugianto, S.Pd", "Jl. Kahuripan 79 Sumber, Surakarta", ""),
            ("PRM Sumber Timur", "H. Kartono, M.Pd", "Sumber, Surakarta", ""),
            ("PRM Badran", "Mukseto", "Gang Mawar 11 Badran Surakarta", ""),
            ("PRM Manahan", "H. Syamsudin Dahlan", "Jl. Samratulangi, Manahan, Surakarta", ""),
        ]
        for name, chair, addr, phone in branches:
            Branch.objects.create(name=name, chairperson=chair, address=addr, official_phone=phone)

        # 5. Amal Usaha (AUM)
        Charity.objects.all().delete()
        charities = [
            ("SD Muhammadiyah Program Khusus Kottabarat", "pendidikan", "Sekolah dasar unggulan berkarakter Islami dan bertaraf nasional.", "Jl. Kenanga No. 12, Surakarta"),
            ("SMP Muhammadiyah Program Khusus Kottabarat", "pendidikan", "Sekolah menengah pertama inovatif berbasis sains dan tahfidz.", "Jl. Pleret Raya, Banyuanyar, Surakarta"),
            ("SMA Muhammadiyah Program Khusus Kottabarat", "pendidikan", "Sekolah menengah atas pengembang riset, kepemimpinan, dan kader persyarikatan.", "Jl. Dr. Moewardi No. 24, Kottabarat"),
            ("Klinik Pratama PKU Muhammadiyah Kottabarat", "kesehatan", "Layanan kesehatan primer dan rawat jalan bagi warga persyarikatan dan masyarakat umum.", "Jl. Slamet Riyadi No. 340, Surakarta"),
            ("Lazismu Kantor Layanan Kottabarat", "sosial", "Pengelolaan dana ZISWAF dan program pemberdayaan ekonomi mustahik.", "Gedung Dakwah PCM Kottabarat Lt. 1"),
            ("BTM Mandiri Berkah Kottabarat", "ekonomi", "Baitut Tamwil Muhammadiyah penyedia pembiayaan mikro syariah bagi UMKM.", "Jl. Kenanga No. 14, Surakarta"),
        ]
        for name, field, desc, addr in charities:
            Charity.objects.create(name=name, field=field, description=desc, address=addr)

        self.stdout.write(self.style.SUCCESS("Data resmi PCM Kottabarat (Profil, Footer, Silsilah Pimpinan, Ranting, AUM) berhasil dimuat ke database."))
