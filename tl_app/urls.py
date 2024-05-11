from django.urls import path
from . import view
from .views import productView

urlpatterns = [
    path("", view.home, name="home"),
    path("registro/", view.registro, name="registro"),
    path("ingreso/", view.ingreso, name="ingreso"),
    path('logout/', view.cerrar_sesion, name='logout'),
    path("crear_producto/", productView.crear_producto, name="crear_producto"),
    path("productos/", productView.productos, name="productos"),
    path("buscar_productos/<str:cadena>",productView.buscar_productos, name="buscar_productos"),
    path("productos/<int:id>",productView.detalle_producto, name="detalle_producto"),
]
