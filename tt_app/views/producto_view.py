from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from ..forms import RegistrationForm, CreacionDeProducto
from django.contrib.auth.forms import AuthenticationForm
from django.db import IntegrityError
from django.utils import timezone
from ..models import Usuario, Producto
from django.contrib.auth.decorators import login_required
from django.urls import reverse


def crear_producto(request):
    if request.method == "POST":
        form = CreacionDeProducto(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save(commit=False)
            # Asignar el usuario autenticado al producto
            producto.usuario = request.user
            # Establecer la fecha de publicación antes de guardar
            producto.fecha_de_publicacion = timezone.now()
            #hardcodeamos (de momento) una sucursal para el ingreso
            producto.sucursal=1
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
    return render(request, "products/detalle.html", {"producto": producto})
