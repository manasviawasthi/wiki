from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>",views.title,name="title"),
    path("new",views.save,name="save"),
    path("error/<str:error>",views.error,name="error"),
    path("random",views.randompage,name="randompage"),
    path("edit/<str:title>",views.edit,name="edit")
]
