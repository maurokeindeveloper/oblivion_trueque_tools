from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from ..forms.producto_forms import CreacionDeProducto, FormularioDePregunta
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from ..models import Producto
from django.contrib.auth.decorators import login_required
from django.urls import reverse

@login_required
def crear_producto(request):
    if request.POST:
        form = CreacionDeProducto(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save(commit=False)  
            producto.usuario = request.user # Asignar el usuario autenticado al producto
            producto.fecha_de_publicacion = timezone.now()  # Establecer la fecha de publicación antes de guardar
            producto.save() # guardamos el producto
            # Redirigir a la página de productos con mensaje de feedback
            return redirect(
                reverse("productos")
                + "?mensaje=El producto se ha agregado correctamente."
            )
    else:
        form = CreacionDeProducto()
    return render(request, "productos/crear_producto.html", {    # enviamos los siguientes parámetros:
        "form": form,   # el form definido en forms.py
        "titulo": "Publicar producto", # el titulo del form
        "boton": "Aceptar", # el texto del botón de confirmación
        "obligatorios": True, # mostrar la advertencia de campos obligatorios o no
    })


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
        return render(request,"productos/buscar_productos.html",{
            "productos": productos,
            "cadena": cadena,
        })
    else:
        return render(request, "productos/productos.html", {"productos": productos})


def detalle_producto(request, id):
    producto = get_object_or_404(Producto, id=id)

    # Lista de preguntas acerca del producto
    preguntas = producto.preguntas.order_by("-fecha")

    # Formulario para las preguntas de los clientes
    form = FormularioDePregunta()

    return render(
        request,
        "productos/detalle_producto.html",
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
        "productos/pregunta.html",
        {"producto": producto, "form": form, "pregunta": pregunta},
    )
