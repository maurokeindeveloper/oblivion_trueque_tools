from django.urls import path
from .views import accountView, productoView

urlpatterns = [
    path("", accountView.home, name="home"),
    path("registro/", accountView.registro, name="registro"),
    path("ingreso/", accountView.ingreso, name="ingreso"),
    path('logout/', accountView.cerrar_sesion, name='logout'),

    path("crear_producto/", productoView.crear_producto, name="crear_producto"),
    path("productos/", productoView.productos, name="productos"),
    path("buscar_productos/", productoView.buscar_productos, name="buscar_productos"),
    path("productos/id/<int:id>", productoView.detalle_producto, name="detalle_producto"),
]
