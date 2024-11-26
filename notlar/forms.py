from django import forms
from .models import Note
from django.contrib.auth.models import User


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ["title", "content", "file"]


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "password", "password_confirm"]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password != password_confirm:
            raise forms.ValidationError("Şifreler uyuşmuyor.")
        return cleaned_data
