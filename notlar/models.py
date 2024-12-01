# Create your models here.
from django.db import models
from django.contrib.auth.models import User  # User modelini ekliyoruz


class Note(models.Model):
    CATEGORY_CHOICES = [
        ("genel", "Genel"),
        ("ders", "Ders"),
        ("is", "İş"),
        ("spor", "Spor"),
        ("teknoloji", "Teknoloji"),
        ("saglik", "Sağlık"),
        ("egitim", "Eğitim"),
    ]
    DERS_CHOICES = [
        ("elektrik_makinalari", "Elektrik Makineleri"),
        ("sinyaller_sistemler", "Sinyaller ve Sistemler"),
        ("devre_teorisi", "Devre Teorisi"),
        ("elektronik", "Elektronik"),
        ("kontrol_sistemleri", "Kontrol Sistemleri"),
        ("enerji_sistemleri", "Enerji Sistemleri"),
        ("elektrik_guc_sistemleri", "Elektrik Güç Sistemleri"),
        ("dijital_elektronik", "Dijital Elektronik"),
        ("mikrodenetleyiciler", "Mikrodenetleyiciler"),
        ("haberlesme_sistemleri", "Haberleşme Sistemleri"),
        ("elektromanyetik_alanlar", "Elektromanyetik Alanlar"),
        ("endustriyel_uygulamalar", "Endüstriyel Uygulamalar"),
        ("yenilenebilir_enerji", "Yenilenebilir Enerji Sistemleri"),
        ("robotik", "Robotik"),
        ("otomasyon", "Otomasyon Sistemleri"),
        ("yapay_zeka", "Yapay Zeka"),
        ("bilgisayar_muhendisligi", "Bilgisayar Mühendisliği"),
        ("sensör_teknolojileri", "Sensör Teknolojileri"),
        ("guc_elektronigi", "Güç Elektroniği"),
        ("optik_iletime", "Optik İletişim Sistemleri"),
        ("motor_kontrol", "Motor Kontrol Sistemleri"),
        ("isaret_isleme", "İşaret İşleme"),
    ]
    title = models.CharField(max_length=100)
    content = models.TextField()
    file = models.FileField(upload_to="notlar/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_shared = models.BooleanField(default=False)
    kategori = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        verbose_name="Kategori",
        default="genel",
    )
    ders_kategori = models.CharField(
        max_length=50,
        choices=DERS_CHOICES,
        blank=True,
        null=True,
        verbose_name="Ders Kategori",
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE
    )  # Kullanıcıya ilişkilendirme

    def __str__(self):
        return self.title
        # get_display methodları ekleyerek seçenekleri güzel bir şekilde almak

    def get_kategori_display(self):
        return dict(self.CATEGORY_CHOICES).get(self.kategori, self.kategori)

    def get_ders_kategori_display(self):
        return dict(self.DERS_CHOICES).get(self.ders_kategori, self.ders_kategori)
