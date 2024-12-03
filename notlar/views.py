import os
from .models import Note
from .forms import NoteForm, UserRegistrationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserChangeForm


@login_required
def not_ekle(request):
    if request.method == "POST":
        form = NoteForm(request.POST, request.FILES)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            messages.success(request, "Not başarıyla eklendi!")
            return redirect("notlar")  # Notlar sayfasına yönlendir
    else:
        form = NoteForm()
    return render(request, "not_ekle.html", {"form": form})


def notlari_listele(request):
    notlar = Note.objects.filter(user=request.user)
    return render(request, "not_listele.html", {"notlar": notlar})


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Formdan gelen verileri alıyoruz
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"]

            # Kullanıcıyı oluşturuyoruz
            User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email,
            )

            messages.success(request, "Kayıt başarılı!")
            return redirect("login")
    else:
        form = UserRegistrationForm()

    return render(request, "register.html", {"form": form})


# Kullanıcı Girişi
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Başarıyla giriş yaptınız!")
            return redirect("home")  # Ana sayfanıza yönlendirin
        else:
            messages.error(request, "Geçersiz kullanıcı adı veya şifre")

    return render(request, "login.html")


def home(request):
    if request.is_mobile:
        return render(request, "mobile/index.html")  # Mobil için şablon
    return render(request, "index.html")


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def update_note(request, pk):
    # Notu al, ama sadece giriş yapan kullanıcıya aitse
    note = get_object_or_404(Note, pk=pk, user=request.user)
    if request.method == "POST":
        form = NoteForm(
            request.POST, request.FILES, instance=note
        )  # Var olan notu düzenle
        if form.is_valid():
            form.save()
            return redirect("notlar")
    else:
        form = NoteForm(instance=note)  # Var olan notun içeriği formda
    return render(request, "update_note.html", {"form": form})


@login_required
def delete_note(request, pk):
    # Notu al, ama sadece giriş yapan kullanıcıya aitse
    note = get_object_or_404(Note, pk=pk, user=request.user)

    if request.method == "POST":  # Sadece "POST" isteği ile silinebilir
        # Eğer notun bir dosyası varsa, dosyayı sil
        if note.file:
            file_path = note.file.path
            if os.path.exists(file_path):
                os.remove(file_path)  # Dosyayı sil

        note.delete()  # Notu veritabanından sil
        messages.success(request, "Not ve dosya başarıyla silindi.")
        return redirect("notlar")  # Notlar sayfasına yönlendir

    return render(request, "delete_note.html", {"note": note})


@login_required
def view_notes(request):
    notes = Note.objects.filter(
        user=request.user
    )  # Giriş yapan kullanıcıya ait notları filtrele
    return render(request, "view_notes.html", {"notes": notes})


@login_required
def profile_view(request):
    """Kullanıcının profilini görüntüleme."""
    user = request.user  # Giriş yapan kullanıcıyı al
    return render(request, "profile_view.html", {"user": user})
    # Kullanıcı bilgilerini şablona gönder


@login_required
def edit_profile(request):
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = CustomUserChangeForm(instance=request.user)

    return render(request, "edit_profile.html", {"form": form})


@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Şifreniz başarıyla güncellenmiştir!")
            update_session_auth_hash(
                request, form.user
            )  # Kullanıcı girişinin geçerliliğini korur
            return redirect("profile")  # Profil sayfasına yönlendir
        else:
            messages.error(
                request, "Şifre değiştirilirken bir hata oluştu. Lütfen tekrar deneyin."
            )
    else:
        form = PasswordChangeForm(request.user)

    return render(request, "change_password.html", {"form": form})


# Not Listele
@login_required
def not_listele(request):
    notlar = Note.objects.filter(user=request.user)  # Kullanıcının notları
    shared_notes = Note.objects.filter(is_shared=True)  # ÇALIŞMADI BU SORUN!!!!

    return render(
        request, "notlar.html", {"notlar": notlar, "shared_notes": shared_notes}
    )


def custom_logout(request):
    logout(request)  # Kullanıcıyı oturumdan çıkar
    return redirect("/")  # Ana sayfaya yönlendir


def password_change(request):
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()  # Şifreyi kaydet
            update_session_auth_hash(request, form.user)  # Oturum güncelle
            messages.success(request, "Şifreniz başarıyla değiştirildi!")
            return redirect("profile")


def shared_notes_view(request):
    # is_shared=True olan tüm notları al
    shared_notes = Note.objects.filter(is_shared=True)
    return render(request, "shared_notes.html", {"shared_notes": shared_notes})
