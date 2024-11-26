from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("not-ekle/", views.not_ekle, name="not_ekle"),
    path("notlar/", views.notlari_listele, name="notlar"),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("", views.home, name="home"),
    path("logout/", views.logout_view, name="logout"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path('notes/', views.view_notes, name='view_notes'),  # Notları listeleme
    path("notes/<int:pk>/update/", views.update_note, name="update_note"),
    path("notes/<int:pk>/delete/", views.delete_note, name="delete_note"),
]
