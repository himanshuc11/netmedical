from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('genres/', views.show_genres, name="genres"),
    path('genre/<str:genre>', views.show_medicine_by_genre, name="medicine_genre"),
    path('search/<str:name>', views.show_medicine_by_name, name="medicine_name"),
    path('medicine', views.medicine, name="medicine"),
    path('medicine_page/<str:medicine_name>',views.single_medicine, name="single_medicine"),

    path('update_cart/', views.update_cart, name="update_cart"),
    path('checkout/', views.checkout, name="checkout"),

    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
]
