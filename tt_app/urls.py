from django.urls import path
from .views import (
    producto_view,
    usuario_view,
    trueque_view,
    venta_view,
    sucursal_view,
    estadistica_view,
)

urlpatterns = [
    path("", usuario_view.home, name="home"),
    path("registro/", usuario_view.registro, name="registro"),
    path("ingreso/", usuario_view.ingreso, name="ingreso"),
    path("logout/", usuario_view.cerrar_sesion, name="logout"),
    path("crear_producto/", producto_view.crear_producto, name="crear_producto"),
    path(
        "modificar_producto/<int:id>",
        producto_view.modificar_producto,
        name="modificar_producto",
    ),
    path(
        "eliminar_producto/<int:id>",
        producto_view.eliminar_producto,
        name="eliminar_producto",
    ),
    path("productos/", producto_view.productos, name="productos"),
    path("buscar_productos/", producto_view.buscar_productos, name="buscar_productos"),
    path(
        "buscar_productos_trueques_programados/",
        producto_view.buscar_productos_trueques_programados,
        name="buscar_productos_trueques_programados",
    ),
    path(
        "productos/id/<int:id>", producto_view.detalle_producto, name="detalle_producto"
    ),
    path(
        "registro_empleado/", usuario_view.registro_empleado, name="registro_empleado"
    ),
    path(
        "trueques_entrantes/",
        trueque_view.trueques_entrantes,
        name="trueques_entrantes",
    ),
    path(
        "aceptar-solicitud/<int:trueque_id>/",
        trueque_view.aceptar_solicitud,
        name="aceptar-solicitud",
    ),
    path(
        "rechazar-solicitud-interes/<int:trueque_id>/",
        trueque_view.rechazar_solicitud_interes,
        name="rechazar-solicitud-interes",
    ),
    path(
        "rechazar-solicitud-horario/<int:trueque_id>/",
        trueque_view.rechazar_solitud_horario,
        name="rechazar-solicitud-horario",
    ),
    path(
        "rechazar-solicitud-fecha/<int:trueque_id>/",
        trueque_view.rechazar_solicitud_fecha,
        name="rechazar-solicitud-fecha",
    ),
    path(
        "rechazar-solicitud-otros/<int:trueque_id>/",
        trueque_view.rechazar_solicitud_otros,
        name="rechazar-solicitud-otros",
    ),
    path(
        "cancelar_trueque/<int:id>/<int:estado>/<str:ret>",
        trueque_view.cancelar_trueque,
        name="cancelar_trueque",
    ),
    path("solicitar/<int:id>/", trueque_view.solicitar, name="solicitar"),
    path("trueque/id/<int:id>", trueque_view.detalle_trueque, name="detalle_trueque"),
    path(
        "trueques_salientes/",
        trueque_view.trueques_salientes,
        name="trueques_salientes",
    ),
    path(
        "trueques_por_concretar/",
        trueque_view.trueques_por_concretar,
        name="trueques_por_concretar",
    ),
    path(
        "trueques_finalizados/",
        trueque_view.trueques_finalizados,
        name="trueques_finalizados",
    ),
    path("productos/id/<int:id>/preguntar", producto_view.preguntar, name="preguntar"),
    path("productos/id/<int:id>/responder", producto_view.responder, name="responder"),
    path(
        "filtrar_productos/<int:categoria>",
        producto_view.filtrar_productos,
        name="filtrar_productos",
    ),
    path("mis_productos/<int:id>", producto_view.mis_productos, name="mis_productos"),
    path("empleados", usuario_view.listado_empleados, name="empleados"),
    path(
        "trueques_programados/",
        trueque_view.trueques_programados,
        name="trueques_programados",
    ),
    path(
        "trueques_concretados/",
        trueque_view.trueques_concretados,
        name="trueques_concretados",
    ),
    path(
        "registrar-ventas/<int:trueque_id>",
        venta_view.registrar_ventas,
        name="registrar_ventas",
    ),
    path(
        "concretar-trueque/<int:trueque_id>/",
        trueque_view.confirmar_trueque,
        name="concretar_trueque",
    ),
    path(
        "listar-ventas-trueque/<int:trueque_id>",
        venta_view.listar_ventas,
        name="listar_ventas_trueque",
    ),
    path(
        "cancelar-trueques-programados/",
        trueque_view.cancelar_trueque_programado,
        name="cancelar_trueques_programados",
    ),
    path("sucursales/", sucursal_view.listado_sucursales, name="sucursales"),
    path(
        "promocionar-producto/<int:id>",
        producto_view.promocionar,
        name="promocionar_producto",
    ),
    path(
        "modificar_empleado/<int:id>/",
        usuario_view.modificar_empleado,
        name="modificar_empleado",
    ),
    path(
        "eliminar_empleado/<int:id>/",
        usuario_view.eliminar_empleado,
        name="eliminar_empleado",
    ),
    path("crear-sucursal/", sucursal_view.crear_sucursal, name="crear_sucursal"),
    path(
        "modificar_sucursal/<int:id>/",
        sucursal_view.modificar_sucursal,
        name="modificar_sucursal",
    ),
    path(
        "eliminar_sucursal/<int:id>/",
        sucursal_view.eliminar_sucursal,
        name="eliminar_sucursal",
    ),
    path(
        "generar_estadisticas_ventas",
        estadistica_view.generar_estadisticas_ventas,
        name="generar_estadisticas_ventas",
    ),
    path(
        "generar_estadisticas_trueques",
        estadistica_view.generar_estadisticas_trueques,
        name="generar_estadisticas_trueques",
    ),
]
