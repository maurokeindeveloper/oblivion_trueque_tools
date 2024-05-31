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

@login_required
def registro_empleado(request):
    if not request.user.is_admin:
        return HttpResponse("No tienes permisos para entrar a esta página.")
    if request.POST:
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
    return render(request, "registro_empleado.html", {
        "form": form,
        "titulo":"Registrar empleado",
        "boton":"Registrar",
    })

def registro(request, *args, **kwargs):    
    user=request.user
    if request.user.is_authenticated:
        return HttpResponse(f"Ya estás registrado como {user.email}.")

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
            return redirect(
                reverse("ingreso") + "?mensaje=El usuario se registró con éxito."
            )
    else:
        form = RegistrationForm()
    return render(request, "registro.html", {
        "form": form,
        "titulo": "Registrarse",
        "boton": "Registrarse"
    })


def ingreso(request):
    user = request.user
    if user.is_authenticated:
        return HttpResponse(f"Ya estás logeado como {user.email}.")
    
    parametros = {"form": AuthenticationForm, # el form a mostrar definido en forms.py
                  "titulo":"Iniciar sesión", # el titulo del formulario
                  "boton":"Iniciar sesión",} # el texto del botón de confirmación
    if request.method =="GET":
        return render(request, "ingreso.html", parametros)
    else:
        usuario = authenticate(
            request,
            email=request.POST["username"],
            password=request.POST["password"],
        )
        if usuario is None:
            print(parametros|{"error": "Usuario o contraseña inválidos"})
            return render(
                request,
                "ingreso.html", (parametros|{"error": "Usuario o contraseña inválidos"}), # agregamos el mensaje de error a los parámetros
            )
        else:
            login(request, usuario)
            return redirect("home")

@login_required
def cerrar_sesion(request):
    logout(request)
    return redirect(reverse("home") + "?mensaje=La sesión se cerró con éxito.")
