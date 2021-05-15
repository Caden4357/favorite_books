from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('blog', views.blog_page),
    path('logout', views.logout),
    path('create_book', views.create_book),
    path("unfavorite/<int:id>", views.unfavorite),
    path("favorite/<int:id>", views.favorite),
    path("display/<int:id>", views.display),
    path("edit/<int:id>", views.edit),
    path("update/<int:id>", views.update),
    path("delete/<int:id>", views.destroy)

]
