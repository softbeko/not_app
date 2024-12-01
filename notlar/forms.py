from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from .models import Note
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = [
            "title",
            "content",
            "file",
            "is_shared",
            "kategori",
            "ders_kategori",
        ]  # Note modelindek
        widgets = {
            "is_shared": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "kategori": forms.Select(
                attrs={"class": "form-select"}
            ),  # Kategori için dropdown menü
            "ders_kategori": forms.Select(
                attrs={"class": "form-select"}
            ),  # Alt kategori için dropdown menü
        }


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


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ["username", "password"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Formdaki tüm alanlara form-control sınıfını ekle
        for field in self.fields.values():
            field.widget.attrs.update(
                {
                    "class": "form-control",
                }
            )
