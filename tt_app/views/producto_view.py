from django.shortcuts import render, redirect, get_object_or_404
from ..forms import CreacionDeProducto, FormularioDePregunta
from django.utils import timezone
from ..models import Producto, Usuario
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST


def crear_producto(request):
    if request.method == "POST":
        form = CreacionDeProducto(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save(commit=False)
            # Asignar el usuario autenticado al producto
            producto.usuario = request.user
            # Establecer la fecha de publicación antes de guardar
            producto.fecha_de_publicacion = timezone.now()
            # hardcodeamos (de momento) una sucursal para el ingreso
            producto.sucursal = 1
            producto.save()
            # Redirigir a la página de productos con mensaje de feedback

            return redirect(
                reverse("productos")
                + "?mensaje=El producto se ha agregado correctamente."
            )

    else:
        form = CreacionDeProducto()
    return render(request, "products/crear_producto.html", {"form": form})


def productos(request):
    productos = Producto.objects.exclude(activo=False).order_by("-promocionado")
    return render(request, "products/productos.html", {"productos": productos})


def buscar_productos(request):
    if request.method == "GET":
        cadena = request.GET.get("cadena")
        productos_nom = Producto.objects.exclude(activo=False).filter(
            nombre__icontains=cadena
        )
        productos_desc = Producto.objects.exclude(activo=False).filter(
            descripcion__icontains=cadena
        )
        productos = productos_nom.union(productos_desc).order_by("-promocionado")
        return render(
            request,
            "products/buscar_productos.html",
            {"productos": productos, "cadena": cadena},
        )
    else:
        return render(request, "products/productos.html", {"productos": productos})


def detalle_producto(request, id):
    producto = get_object_or_404(Producto, id=id)

    # Lista de preguntas acerca del producto
    preguntas = producto.preguntas.order_by("-fecha")

    # Formulario para las preguntas de los clientes
    form = FormularioDePregunta()

    return render(
        request,
        "products/detalle.html",
        {"producto": producto, "preguntas": preguntas, "formulario": form},
    )


def preguntar(request, id):
    producto = get_object_or_404(Producto, id=id)

    pregunta = None
    # Se realiza una pregunta
    form = FormularioDePregunta(data=request.POST)
    if form.is_valid():
        # Crea un objeto Pregunta sin guardarlo en la base de datos
        pregunta = form.save(commit=False)
        # Asigna el producto y el client a la pregunta - DEBEN SER LOS OBJETOS, NO LOS VALORES (O IDS)
        pregunta.producto = producto
        pregunta.cliente = producto.usuario
        # Guarda la pregunta en la base de datos
        pregunta.save()
    return render(
        request,
        "products/pregunta.html",
        {"producto": producto, "form": form, "pregunta": pregunta},
    )
