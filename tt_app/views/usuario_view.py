from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from ..forms.usuario_forms import RegistrarEmpleado,RegistrationForm,IngresoForm
from ..forms.usuario_forms import check_cliente,check_empleado,check_administrador
from ..models import Producto,Usuario,Venta
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import get_object_or_404


# Create your views here.


def home(request):
    preview = Producto.objects.exclude(activo=False).order_by("-promocionado")[
        :5
    ]  # Los productos que se van a mostrar en el home #
    return render(request, "home.html", {"productos": preview})

@login_required
def registro_empleado(request):
    chk=check_administrador(request.user)
    if chk["ok"]:
        return chk["return"]
    if request.POST:
        form = RegistrarEmpleado(request.POST)
        if form.is_valid():
            empleado = form.save(commit=False)
            empleado.is_staff = True  # Marcar al empleado como staff
            empleado.first_name = form.cleaned_data.get("first_name").capitalize()
            empleado.last_name = form.cleaned_data.get("last_name").capitalize()
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
    return render(request, "usuario/registro_empleado.html", {  # enviamos los siguientes parámetros:
        "form": form,                                   # el form definido en usuario_forms.py
        "titulo":"Registrar empleado",                  # el titulo del form
        "boton":"Registrar",                            # el texto del botón de confirmación
        "obligatorios": True, # mostrar la advertencia de campos obligatorios o no
    })

def registro(request, *args, **kwargs):   
    if request.user.is_authenticated:
        return HttpResponse(f"Ya estás registrado como {user.email}.")
    
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            cliente = form.save(commit=False)
            cliente.email = form.cleaned_data.get("email").lower()
            raw_password = form.cleaned_data.get("password1")
            cliente.first_name = form.cleaned_data.get("first_name").title()
            cliente.last_name = form.cleaned_data.get("last_name").title()
            dni = form.cleaned_data.get("dni")
            phone = form.cleaned_data.get("phone")
            birthdate = form.cleaned_data.get("birthdate")
            cliente.save()
            user = authenticate(
                email=cliente.email,
                password=raw_password,
                first_name=cliente.first_name,
                last_name=cliente.last_name,
                dni=dni,
                phone=phone,
                birthdate=birthdate,
            )
            return redirect(
                reverse("ingreso") + "?mensaje=El usuario se registró con éxito."
            )
    else:
        form = RegistrationForm()
    return render(request, "usuario/registro_cliente.html", {   # enviamos los siguientes parámetros:
        "form": form,                           # el form definido en usuario_forms.py
        "titulo":"Registrarse",                 # el titulo del form
        "boton":"Registrarse",                  # el texto del botón de confirmación
        "obligatorios": True, # mostrar la advertencia de campos obligatorios o no
    })

def ingreso(request):
    user = request.user
    if user.is_authenticated:
        return HttpResponse(f"Ya estás logeado como {user.email}.")
    
    parametros = {"form": IngresoForm(), # el form a mostrar definido en usuario_forms.py
                  "titulo":"Iniciar sesión",# el titulo del formulario
                  "boton":"Iniciar sesión", # el texto del botón de confirmación
                  "obligatorios": False, # mostrar la advertencia de campos obligatorios o no
    }
    if request.POST:
        parametros["form"] = IngresoForm(request.POST)
        if parametros["form"].is_valid():
            usuario = authenticate(
                request,
                email= parametros["form"].cleaned_data.get("email"),
                password= parametros["form"].cleaned_data.get("password"),
            )
            if usuario is None:
                return render(request,"usuario/ingreso.html",
                               (parametros|{"error": "Usuario o contraseña inválidos"}), # agregamos el mensaje de error a los parámetros
                )
            else:
                login(request, usuario)
                return redirect("home")
    return render(request, "usuario/ingreso.html", parametros)

@login_required
def cerrar_sesion(request):
    logout(request)
    return redirect(reverse("home") + "?mensaje=La sesión se cerró con éxito.")
'''
def listado_empleados(request):
    empleados = Usuario.objects.exclude(is_active=False,is_staff = False)
    return render(request, "usuario/listado_empleados.html", {  "empleados":empleados
    })
'''
@login_required
def listado_empleados(request):
    chk = check_administrador(request.user)
    if chk["ok"]:
        return chk["return"]
    empleados = Usuario.objects.filter(is_staff=True, is_active=True, is_admin=False, is_superuser=False)
    return render(request, "usuario/partials/listado_empleados.html", {"empleados": empleados})


@login_required
def modificar_empleado(request, id):
    chk = check_administrador(request.user)
    if chk["ok"]:
        return chk["return"]
    
    empleado = get_object_or_404(Usuario, id=id)

    if request.method == "POST":
        form = RegistrarEmpleado(request.POST, request.FILES, instance=empleado)
        if form.is_valid():
            form = form.save(commit=False)
            print("modificando...")
            form.save()
            # Redirigir a la página de los empleados con mensaje de feedback
            return redirect(
                reverse("empleados") + "?mensaje=El empleado se ha modificado correctamente."
            )
    else:
        form = RegistrarEmpleado(instance=empleado)
    
    return render(
        request,
        "usuario/registro_empleado.html",
        {
            "form": form,
            "titulo": "Modificar empleado",
            "boton": "Modificar",
            "obligatorios": False,
        },
    )
    
@login_required
def eliminar_empleado(request, id):
    chk = check_administrador(request.user)
    if chk["ok"]:
        return chk["return"]
    
    empleado = get_object_or_404(Usuario, id=id)
    
    if request.method == 'POST':
        empleado.is_active = False
        empleado.save()
        return redirect(
            reverse("empleados") + "?mensaje=El empleado se ha eliminado correctamente."
        )
    else:
        # Redirigir a la página de los empleados con mensaje de feedback
        return redirect(
            reverse("empleados") + "?mensaje=El empleado no se ha podido eliminar."
        )