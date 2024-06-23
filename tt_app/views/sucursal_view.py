from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from ..forms.usuario_forms import RegistrarEmpleado,RegistrationForm,IngresoForm
from ..forms.usuario_forms import check_cliente,check_empleado,check_administrador
from ..models import Sucursal
from django.contrib.auth.decorators import login_required
from django.urls import reverse

def listado_sucursales(request): 
    sucursales = Sucursal.objects.filter(activo=True)
    return render(request, "sucursales/sucursales.html", {"sucursales": sucursales})