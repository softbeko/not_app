# Create your models here.
from django.db import models
from django.contrib.auth.models import User  # User modelini ekliyoruz


class Note(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    file = models.FileField(upload_to="notlar/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE
    )  # Kullanıcıya ilişkilendirme

    def __str__(self):
        return self.title
