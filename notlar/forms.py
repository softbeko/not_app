from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from .models import Note
from django.contrib.auth.forms import UserCreationForm


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ["title", "content", "file"]  # Note modelindeki alanları belirtin


class UserRegistrationForm(UserCreationForm):
    # Yeni alanlar ekliyoruz
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        ]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Bu e-posta adresi zaten kullanımda.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password1")
        password_confirm = cleaned_data.get("password2")

        if password != password_confirm:
            raise forms.ValidationError("Şifreler uyuşmuyor.")
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Her alana 'form-control' sınıfı ekliyoruz
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Her alana 'form-control' sınıfı ekliyoruz
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})
