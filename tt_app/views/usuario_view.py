from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from ..forms import RegistrationForm, RegistrarEmpleado
from django.contrib.auth.forms import AuthenticationForm
from ..models import Usuario, Producto
from django.contrib.auth.decorators import login_required
from django.urls import reverse


# Create your views here.


def home(request):
    preview = Producto.objects.exclude(activo=False).order_by("-promocionado")[
        :5
    ]  # Los productos que se van a mostrar en el home #
    return render(request, "home.html", {"productos": preview})


def registro_empleado(request):
    if request.method == "POST":
        form = RegistrarEmpleado(request.POST)
        if form.is_valid():
            empleado = form.save(commit=False)
            empleado.is_staff = True  # Marcar al empleado como staff
            empleado.set_password(
                form.cleaned_data["password"]
            )  # Establecer la contraseña correctamente
            empleado.save()
            return redirect(
                reverse("productos")
                + "?mensaje=El empleado se ha agregado correctamente."
            )
    else:
        form = RegistrarEmpleado()
    return render(request, "registro_empleado.html", {"form": form})


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
