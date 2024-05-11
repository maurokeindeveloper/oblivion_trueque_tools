from django.urls import path
from . import view
from .views import productView

urlpatterns = [
    path("", views.home, name="home"),
    path("registro/", views.registro, name="registro"),
    path("ingreso/", views.ingreso, name="ingreso"),
    path('logout/', views.cerrar_sesion, name='logout'),
    path("crear_producto/", views.crear_producto, name="crear_producto"),
    path("productos/", views.productos, name="productos"),
    path("buscar_productos/",views.buscar_productos, name="buscar_productos"),
    path("productos/id/<int:id>",views.detalle_producto, name="detalle_producto"),
]
