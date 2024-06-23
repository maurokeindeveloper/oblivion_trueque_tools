from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from ..forms.sucursal_forms import CrearSucursal
from ..forms.usuario_forms import check_cliente,check_empleado,check_administrador
from ..models import Sucursal
from django.contrib.auth.decorators import login_required
from django.urls import reverse

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
            #sucursal.ciudad = sucursal.ciudad.capitalize()
            sucursal.save() # guardamos el producto
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