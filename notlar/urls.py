from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth.views import LoginView
from .views import custom_logout


urlpatterns = [
    path("not-ekle/", views.not_ekle, name="not_ekle"),
    path("notlar/", views.notlari_listele, name="notlar"),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("", views.home, name="index"),
    path("", views.home, name="home"),
    path("logout/", custom_logout, name="logout"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("notes/", views.view_notes, name="view_notes"),  # Notları listeleme
    path("notes/<int:pk>/update/", views.update_note, name="update_note"),
    path("notes/<int:pk>/delete/", views.delete_note, name="delete_note"),
    path("profile/", views.profile_view, name="profile"),  # Profil görüntüleme
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path(
        "profile/change-password/", views.change_password, name="change_password"
    ),  # Şifre değiştirme
    path("accounts/login/", LoginView.as_view(), name="login"),
    path("paylasilan-notlar/", views.shared_notes_view, name="shared_notes"),
]
