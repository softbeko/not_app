from django.shortcuts import render, redirect, get_object_or_404
from .models import Note
from .forms import NoteForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserRegistrationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def not_ekle(request):
    if request.method == "POST":
        form = NoteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Veriyi veritabanına kaydet
            return redirect(
                "not_ekle"
            )  # Form gönderildikten sonra yeniden aynı sayfaya yönlendirme
    else:
        form = NoteForm()

    return render(request, "not_ekle.html", {"form": form})


def notlari_listele(request):
    notlar = Note.objects.all()
    return render(request, "not_listele.html", {"notlar": notlar})


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            User.objects.create_user(username=username, password=password)
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
            return redirect("view_notes")  # Notlar sayfasına yönlendir
    else:
        form = NoteForm(instance=note)  # Var olan notun içeriği formda
    return render(request, "update_note.html", {"form": form})


@login_required
def delete_note(request, pk):
    # Notu al, ama sadece giriş yapan kullanıcıya aitse
    note = get_object_or_404(Note, pk=pk, user=request.user)
    if request.method == "POST":  # Sadece "POST" isteği ile silinebilir
        note.delete()
        return redirect("view_notes")  # Notlar sayfasına yönlendir
    return render(request, "delete_note.html", {"note": note})


@login_required
def view_notes(request):
    notes = Note.objects.filter(
        user=request.user
    )  # Giriş yapan kullanıcıya ait notları filtrele
    return render(request, "view_notes.html", {"notes": notes})
