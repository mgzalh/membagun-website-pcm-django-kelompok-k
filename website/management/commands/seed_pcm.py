from datetime import datetime

from django.core.management.base import BaseCommand
from django.utils import timezone

from website.models import Article, Branch, Charity, Event, Leader, OrganizationProfile, RelatedLink


class Command(BaseCommand):
    help = "Mengisi database dengan profil resmi, pimpinan, dan ranting PCM Kottabarat dari SK resmi."

    def handle(self, *args, **options):
        # Profil Organisasi Resmi
        prof, _ = OrganizationProfile.objects.get_or_create(
            defaults={
                "name": "Pimpinan Cabang Muhammadiyah Kottabarat",
                "short_name": "PCM Kottabarat",
            }
        )
        prof.office_address = "Jl. Dr. Muwardi No. 24, Surakarta"
        prof.tagline = "Gerakan Islam Berkemajuan Menuju Masyarakat Madani di Kottabarat"
        prof.about = (
            "Pimpinan Cabang Muhammadiyah (PCM) Kottabarat merupakan struktur persyarikatan "
            "di bawah PDM Kota Surakarta yang mengelola dakwah, pendidikan unggulan, dan layanan kemasyarakatan."
        )
        prof.ktam_members = None
        prof.save()

        # Pimpinan Resmi (2022 - 2027)
        Leader.objects.all().delete()
        leaders = [
            ("Drs. H. Marpuji Ali, M.Si.", "Penasehat", "2022 - 2027", 1),
            ("H. Sjamsuddin Dahlan", "Penasehat", "2022 - 2027", 2),
            ("Dr. Muhammad Ali, M.Pd", "Penasehat", "2022 - 2027", 3),
            ("Joko Susilo, S.TP., S.Pd.I., M.Pd", "Ketua Cabang", "2022 - 2027", 10),
            ("Saifudin, SP", "Wakil Ketua I", "2022 - 2027", 11),
            ("H. Kartono, S.Pd., M.Pd", "Wakil Ketua II", "2022 - 2027", 12),
            ("Retno Sugiyanto, S.Pd", "Sekretaris", "2022 - 2027", 13),
            ("Muhdiyatmoko, S.Pd., M.Pd", "Wakil Sekretaris", "2022 - 2027", 14),
            ("Mukseto", "Bendahara", "2022 - 2027", 15),
            ("Yusuf Aris Kurniawan, S.Pi", "Wakil Bendahara", "2022 - 2027", 16),
            ("H. Suwardi, S.Ag, M.Si", "Anggota Pleno", "2022 - 2027", 17),
            ("Lasur Suryadi", "Anggota Pleno", "2022 - 2027", 18),
            ("Nur Salam, S.Fil, M.Pd", "Ketua Majelis Dikdasmen", "2022 - 2027", 20),
            ("Purmoko, S.Kom", "Ketua Majelis Tabligh", "2022 - 2027", 21),
            ("Wagino Hadi Pranoto", "Ketua Majelis Ekonomi", "2022 - 2027", 22),
            ("Lasur Suryadi", "Ketua Majelis Wakaf", "2022 - 2027", 23),
            ("Hendro Susilo, S.Pd", "Ketua Majelis Kader", "2022 - 2027", 24),
            ("H. Kusnan, S.Pd", "Ketua Majelis Kesejahteraan Sosial & LAZISMU", "2022 - 2027", 25),
        ]
        for name, pos, period, order in leaders:
            Leader.objects.create(name=name, position=pos, period=period, display_order=order)

        # Ranting (PRM) Resmi
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

        # Amal Usaha (AUM)
        charities = [
            ("SD Muhammadiyah Program Khusus Kottabarat", "pendidikan", "Sekolah dasar unggulan berkarakter Islami dan bertaraf nasional.", "Jl. Kenanga No. 12, Surakarta"),
            ("SMP Muhammadiyah Program Khusus Kottabarat", "pendidikan", "Sekolah menengah pertama inovatif berbasis sains dan tahfidz.", "Jl. Pleret Raya, Banyuanyar, Surakarta"),
            ("SMA Muhammadiyah Program Khusus Kottabarat", "pendidikan", "Sekolah menengah atas pengembang riset, kepemimpinan, dan kader persyarikatan.", "Jl. Dr. Moewardi No. 24, Kottabarat"),
            ("Klinik Pratama PKU Muhammadiyah Kottabarat", "kesehatan", "Layanan kesehatan primer dan rawat jalan bagi warga persyarikatan dan masyarakat umum.", "Jl. Slamet Riyadi No. 340, Surakarta"),
            ("Lazismu Kantor Layanan Kottabarat", "sosial", "Pengelolaan dana ZISWAF dan program pemberdayaan ekonomi mustahik.", "Gedung Dakwah PCM Kottabarat Lt. 1"),
            ("BTM Mandiri Berkah Kottabarat", "ekonomi", "Baitut Tamwil Muhammadiyah penyedia pembiayaan mikro syariah bagi UMKM.", "Jl. Kenanga No. 14, Surakarta"),
        ]
        for name, field, desc, addr in charities:
            Charity.objects.get_or_create(name=name, defaults={"field": field, "description": desc, "address": addr})

        self.stdout.write(self.style.SUCCESS("Data resmi PCM Kottabarat berhasil dimuat ke database."))
