from django.urls import path
from .views import home, registro, ingreso, crear_producto,prodcutos,cerrar_sesion

urlpatterns = [
    path("", home, name="home"),
    path("registro/", registro, name="registro"),
    path("ingreso/", ingreso, name="ingreso"),
    path('logout/', cerrar_sesion, name='logout'),
    path("productos/", prodcutos, name="productos"),
    path("crear_producto/", crear_producto, name="crear_producto"),
]
