from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from .forms import RegistrationForm, CreacionDeProducto
from django.contrib.auth.forms import AuthenticationForm
from django.db import IntegrityError
from django.utils import timezone
from .models import CustomUser, Producto
from django.contrib.auth.decorators import login_required
from django.urls import reverse


# Create your views here.


def home(request):
    return render(request, "home.html")


def registro(request, *args, **kwargs):
    user = request.user
    if user.is_authenticated:
        return HttpResponse(f"Ya estás registrado como {user.email}.")
    context = {}

    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get("email").lower()
            raw_password = form.cleaned_data.get("password1")
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            dni = form.cleaned_data.get("dni")
            phone = form.cleaned_data.get("phone")
            birthdate = form.cleaned_data.get("birthdate")
            user = authenticate(
                email=email,
                password=raw_password,
                first_name=first_name,
                last_name=last_name,
                dni=dni,
                phone=phone,
                birthdate=birthdate,
            )
            destination = kwargs.get("next")
            if destination:
                return redirect(destination)
            return redirect(
                reverse("ingreso") + "?mensaje=El usuario se registró con éxito."
            )
        else:
            context["registration_form"] = form

    return render(request, "registro.html", context)


def ingreso(request):
    if request.method == "GET":
        return render(request, "ingreso.html", {"form": AuthenticationForm})
    else:
        usuario = authenticate(
            request,
            email=request.POST["username"],
            password=request.POST["password"],
        )
        if usuario is None:
            return render(
                request,
                "ingreso.html",
                {"form": AuthenticationForm, "error": "Usuario o contraseña inválidos"},
            )
        else:
            login(request, usuario)
            return redirect("home")


def cerrar_sesion(request):
    logout(request)
    return redirect(reverse("home") + "?mensaje=La sesión se cerró con éxito.")


def crear_producto(request):
    if request.method == "POST":
        form = CreacionDeProducto(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save(commit=False)
            # Asignar el usuario autenticado al producto
            producto.usuario = request.user
            # Establecer la fecha de publicación antes de guardar
            producto.fecha_de_publicacion = timezone.now()
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
        print("nao nao")
        return render(request, "products/productos.html", {"productos": productos})


def detalle_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    return render(request, "products/detalle.html", {"producto": producto})
