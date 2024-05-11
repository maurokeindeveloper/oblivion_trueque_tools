from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from ..models import usuarioModel
from django.utils import timezone
from django.contrib.auth.decorators import login_required
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
                usuario = usuarioModel.Usuario.objects.create(
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
