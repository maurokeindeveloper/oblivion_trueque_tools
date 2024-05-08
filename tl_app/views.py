from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from .models import Usuario, Producto
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .forms import CreacionDeProducto
from django.contrib.auth import logout



# Create your views here.
def home(request):
    return render(request, "home.html")

def cerrar_sesion(request):
    logout(request)
    return redirect('home')

def registro(request):
    if request.method == "GET":
        return render(request, "registro.html", {"form": UserCreationForm})
    else:
        if request.POST["password1"] == request.POST["password2"]:
            try:
                usuario = Usuario.objects.create(
                    email=request.POST["email"],
                    password=request.POST["password"],
                    telefono=request.POST["telefono"],
                    fecha_de_nacimiento=request.POST["fecha_de_nacimiento"],
                    DNI=request.POST["DNI"],
                )
                usuario.save()
                return redirect("login")
            except IntegrityError:
                return render(
                    request,
                    "registro.html",
                    {
                        "form": UserCreationForm,
                        "error": "El email ingresado ya se encuentra registrado",
                    },
                )
    return render(
        request,
        "registro.html",
        {"form": UserCreationForm, "error": "Las contraseñas no coinciden"},
    )


def ingreso(request):
    if request.method == "GET":
        return render(request, "ingreso.html", {"form": AuthenticationForm})
    else:
        usuario = authenticate(
            request,
            username=request.POST["email"],
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


"""             return redirect("productos") """



def crear_producto(request):
    if request.method == 'POST':
        form = CreacionDeProducto(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.usuario = Usuario.objects.get(id=2)
            producto.fecha_de_publicacion = timezone.now()  # Establecer la fecha de publicación antes de guardar
            producto.save()
            return redirect('productos')  # Redirige a la página de productos
    else:
        form = CreacionDeProducto()
    return render(request, 'crear_producto.html', {'form': form})


def productos(request):
    productos = Producto.objects.all().order_by('nombre')
    return render(request, "products/productos.html",{
        "productos": productos
    })
def buscar_productos(request,cadena):
    productos = Producto.objects.filter(nombre__icontains=cadena).filter(descripcion__icontains=cadena)
    return render(request, "products/buscar_productos.html",{
        "productos": productos,
        "cadena":cadena
    })
def detalle_producto(request,id):
    producto = get_object_or_404(Producto, id=id)
    return render(request,"products/detalle.html",{
        "producto": producto
    })