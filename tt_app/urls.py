from django.urls import path
from .views import producto_view, usuario_view, trueque_view

urlpatterns = [
    path("", usuario_view.home, name="home"),
    path("registro/", usuario_view.registro, name="registro"),
    path("ingreso/", usuario_view.ingreso, name="ingreso"),
    path("logout/", usuario_view.cerrar_sesion, name="logout"),
    path("crear_producto/", producto_view.crear_producto, name="crear_producto"),
    path("productos/", producto_view.productos, name="productos"),
    path("buscar_productos/", producto_view.buscar_productos, name="buscar_productos"),
    path("productos/id/<int:id>", producto_view.detalle_producto, name="detalle_producto"),
    path("registro_empleado/", usuario_view.registro_empleado, name="registro_empleado"),
    path("gestion_trueque/", trueque_view.gestion_trueque, name="gestion_trueque"),
    path("trueques_entrantes/", trueque_view.trueques_entrantes, name="trueques_entrantes"),
    path('aceptar-solicitud/<int:trueque_id>/', trueque_view.aceptar_solicitud, name='aceptar-solicitud'),
    path('cancelar_trueque/<int:id>/<int:estado>/<str:ret>', trueque_view.cancelar_trueque, name='cancelar_trueque'),
    path("trueques_salientes/", trueque_view.trueques_salientes, name="trueques_salientes"),
    path("trueques_por_concretar/", trueque_view.trueques_por_concretar, name="trueques_por_concretar"),
    path("trueques_finalizados/", trueque_view.trueques_finalizados, name="trueques_finalizados"),
    path("productos/id/<int:id>/preguntar", producto_view.preguntar, name="preguntar"),
    path("trueques_por_concretar/", trueque_view.trueques_por_concretar, name="trueques_por_concretar"),
    path("trueques_finalizados/", trueque_view.trueques_finalizados, name="trueques_finalizados")
]
