from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from ..forms.sucursal_forms import CrearSucursal
from ..forms.usuario_forms import check_cliente, check_empleado, check_administrador
from ..models import Sucursal
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import get_object_or_404


def listado_sucursales(request):
    sucursales = Sucursal.objects.filter(activo=True)
    return render(request, "sucursales/sucursales.html", {"sucursales": sucursales})


def crear_sucursal(request):
    chk = check_administrador(request.user)
    if chk["ok"]:
        return chk["return"]
    if request.POST:
        form = CrearSucursal(request.POST)
        if form.is_valid():
            sucursal = form.save(commit=False)
            # sucursal.ciudad = sucursal.ciudad.capitalize()
            sucursal.save()  # guardamos el producto
            # Redirigir a la página de productos con mensaje de feedback
            return redirect(
                reverse("sucursales")
                + "?mensaje=La sucursal se ha agregado correctamente."
            )
    else:
        form = CrearSucursal()
    return render(
        request,
        "sucursales/crear_sucursal.html",
        {  # enviamos los siguientes parámetros:
            "form": form,  # el form definido en producto_forms.py
            "titulo": "Registrar sucursal",  # el titulo del form
            "boton": "Aceptar",  # el texto del botón de confirmación
            "obligatorios": True,  # mostrar la advertencia de campos obligatorios o no
        },
    )


@login_required
def modificar_sucursal(request, id):
    chk = check_administrador(request.user)
    if chk["ok"]:
        return chk["return"]

    sucursal = get_object_or_404(Sucursal, id=id)

    if request.method == "POST":
        form = CrearSucursal(request.POST, request.FILES, instance=sucursal)
        if form.is_valid():
            form = form.save(commit=False)
            print("modificando...")
            form.save()
            # Redirigir a la página de las sucursales con mensaje de feedback
            return redirect(
                reverse("sucursales")
                + "?mensaje=La sucursal se ha modificado correctamente."
            )
    else:
        form = CrearSucursal(instance=sucursal)

    return render(
        request,
        "sucursales/crear_sucursal.html",
        {
            "form": form,
            "titulo": "Modificar sucursal",
            "boton": "Modificar",
            "obligatorios": False,
        },
    )


@login_required
def eliminar_sucursal(request, id):
    chk = check_administrador(request.user)
    if chk["ok"]:
        return chk["return"]

    sucursal = get_object_or_404(Sucursal, id=id)

    if request.method == "POST":
        sucursal.activo = False
        sucursal.save()
        return redirect(
            reverse("sucursales")
            + "?mensaje=La sucursal se ha eliminado correctamente."
        )
    else:
        # Redirigir a la página de las sucursales con mensaje de feedback
        return redirect(
            reverse("sucursales") + "?mensaje=La sucursal no se ha podido eliminar."
        )
