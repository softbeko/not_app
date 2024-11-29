from .models import Note
from .forms import NoteForm, UserRegistrationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserChangeForm


@login_required
def not_ekle(request):
    if request.method == "POST":
        form = NoteForm(request.POST, request.FILES)  # Formdan gelen veriyi al
        if form.is_valid():
            note = form.save(commit=False)  # Henüz veritabanına kaydetme
            note.user = request.user  # Giriş yapan kullanıcıyı ata
            note.save()  # Veritabanına kaydet
            notlar = Note.objects.all()
            return render(request, "not_listele.html", {"notlar": notlar})
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
            notlar = Note.objects.all()
            return render(
                request, "not_listele.html", {"notlar": notlar}
            )  # Notlar sayfasına yönlendir
    else:
        form = NoteForm(instance=note)  # Var olan notun içeriği formda
    return render(request, "update_note.html", {"form": form})


@login_required
def delete_note(request, pk):
    # Notu al, ama sadece giriş yapan kullanıcıya aitse
    note = get_object_or_404(Note, pk=pk, user=request.user)
    if request.method == "POST":  # Sadece "POST" isteği ile silinebilir
        note.delete()
        notlar = Note.objects.all()
        return render(request, "not_listele.html", {"notlar": notlar})
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
def not_listele(request):
    notlar = Note.objects.all()
    return render(request, "not_listele.html", {"notlar": notlar})


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
