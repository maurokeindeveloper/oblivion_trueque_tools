from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
<<<<<<< HEAD
from django.contrib.auth import login, logout, authenticate
from ..forms.producto_forms import CreacionDeProducto, PreguntaForm, RespuestaForm
=======
from ..forms.producto_forms import CreacionDeProducto, FormularioDePregunta
from ..forms.usuario_forms import check_cliente
>>>>>>> 83c356f7ac3edb7066c2e9d9cd6656c9294a5c80
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from ..models import Producto, Pregunta, Respuesta
from django.contrib.auth.decorators import login_required
from django.urls import reverse


@login_required
def crear_producto(request):
    chk=check_cliente(request)
    if chk["ok"]:
        return chk["return"]
    if request.POST:
        form = CreacionDeProducto(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.usuario = (
                request.user
            )  # Asignar el usuario autenticado al producto
            producto.fecha_de_publicacion = (
                timezone.now()
            )  # Establecer la fecha de publicación antes de guardar
            producto.save()  # guardamos el producto
            # Redirigir a la página de productos con mensaje de feedback
            return redirect(
                reverse("productos")
                + "?mensaje=El producto se ha agregado correctamente."
            )
    else:
        form = CreacionDeProducto()
    return render(
        request,
        "productos/crear_producto.html",
        {  # enviamos los siguientes parámetros:
            "form": form,  # el form definido en producto_forms.py
            "titulo": "Publicar producto",  # el titulo del form
            "boton": "Aceptar",  # el texto del botón de confirmación
            "obligatorios": True,  # mostrar la advertencia de campos obligatorios o no
        },
    )


def productos(request):
    productos = Producto.objects.exclude(activo=False).order_by("-promocionado")
    return render(request, "productos/productos.html", {"productos": productos})


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
            "productos/buscar_productos.html",
            {
                "productos": productos,
                "cadena": cadena,
            },
        )
    else:
        return render(request, "productos/productos.html", {"productos": productos})


def detalle_producto(request, id):
    producto = get_object_or_404(Producto, id=id)

    # Lista de preguntas acerca del producto
    preguntas = producto.preguntas.all().order_by("-fecha")
    formularioPregunta = PreguntaForm()
    context = {
        "producto": producto,
        "preguntas": preguntas,
        "formularioPregunta": formularioPregunta,
    }
    # Formulario para las preguntas y respuestas de los clientes
    return render(request, "productos/detalle_producto.html", context)

<<<<<<< HEAD

@login_required
def preguntar(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == "POST":
        form = PreguntaForm(request.POST)
        if form.is_valid():
            pregunta = form.save(commit=False)
            pregunta.producto = producto
            pregunta.cliente = request.user
            pregunta.save()
    return redirect("detalle_producto", producto_id=producto.id)
=======
@login_required
def preguntar(request, id):
    chk=check_cliente(request.user)
    if chk["ok"]:
        return chk["return"]
    producto = get_object_or_404(Producto, id=id)
>>>>>>> 83c356f7ac3edb7066c2e9d9cd6656c9294a5c80


@login_required
def responder(request, pregunta_id):
    pregunta = get_object_or_404(Pregunta, id=pregunta_id)
    if request.method == "POST":
        form = RespuestaForm(request.POST)
        if form.is_valid():
            respuesta = form.save(commit=False)
            respuesta.pregunta = pregunta
            respuesta.save()
    return redirect("detalle_producto", producto_id=pregunta.producto.id)
