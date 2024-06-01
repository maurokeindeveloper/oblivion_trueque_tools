from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from ..models import Trueque

def gestion_trueque(request):
    return render(request, "gestion_trueque.html")

@login_required
def trueques_entrantes(request):
    usuario = request.user
    print(f"Usuario autenticado: {usuario.email}")
    #trueques = Trueque.objects.all()
    trueques = Trueque.objects.exclude(activo=False).filter(producto_solicitado__usuario=usuario , estado=1)

    return render(request, "trueques/trueques_entrantes.html", {"trueques": trueques})

@login_required
def trueques_salientes(request):
    usuario = request.user
    trueques = Trueque.objects.exclude(activo=False).filter(producto_solicitante__usuario=usuario , estado=1)
    return render(request, "trueques/trueques_salientes.html", {"trueques": trueques, "nombre": usuario.first_name})