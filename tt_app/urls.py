from django.urls import path
from .views import producto_view, usuario_view

urlpatterns = [
    path("", usuario_view.home, name="home"),
    path("registro/", usuario_view.registro, name="registro"),
    path("ingreso/", usuario_view.ingreso, name="ingreso"),
    path("logout/", usuario_view.cerrar_sesion, name="logout"),
    path("crear_producto/", producto_view.crear_producto, name="crear_producto"),
    path("productos/", producto_view.productos, name="productos"),
    path("buscar_productos/", producto_view.buscar_productos, name="buscar_productos"),
    path(
        "productos/id/<int:id>", producto_view.detalle_producto, name="detalle_producto"
    ),
    path("productos/id/<int:id>/preguntar", producto_view.preguntar, name="preguntar"),
]
