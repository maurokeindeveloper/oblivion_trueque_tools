from django.urls import path

from .views import home, registro, ingreso

urlpatterns = [
    path("", home, name="home"),
    path("registro/", registro, name="registro"),
    path("ingreso/", ingreso, name="ingreso"),
]
