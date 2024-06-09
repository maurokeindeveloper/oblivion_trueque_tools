from django.shortcuts import render
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from ..forms.usuario_forms import check_cliente,check_empleado
from ..models import Trueque

@login_required
def gestion_trueque(request):
    chk=check_empleado(request.user)
    if chk["ok"]:
        return chk["return"]
    return render(request, "gestion_trueque.html")

@login_required
def trueques_entrantes(request):
    usuario = request.user
    chk=check_cliente(usuario)
    if chk["ok"]:
        return chk["return"]
    print(f"Usuario autenticado: {usuario.email}")
    #trueques = Trueque.objects.all()
    trueques = Trueque.objects.exclude(activo=False).filter(producto_solicitado__usuario=usuario , estado=1)
    return render(request, "trueques/trueques_entrantes.html", {"trueques": trueques})

def aceptar_solicitud(request, trueque_id):
    if request.POST:

        # Obtener el objeto trueque
        trueque = get_object_or_404(Trueque, id=trueque_id)   

        #trueques del solicitado (el que acepta la solicutud) que esten en estado solicitado para asignar en pendiente
        trueques = Trueque.objects.exclude(activo=False).filter(producto_solicitado=trueque.producto_solicitante, estado=1)     
        for tr in trueques:
            tr.estado = 2 #pendiente

        # Actualizar el trueque en la base de datos
        trueque.estado = 3


        trueque.save()        
    return redirect(reverse("trueques_entrantes") + "?mensaje=La solicitud se aceptó correctamente")


@login_required
def trueques_salientes(request):
    usuario = request.user
    chk=check_cliente(usuario)
    if chk["ok"]:
        return chk["return"]
    trueques = Trueque.objects.exclude(activo=False).filter(Q(estado=1) | Q(estado=2) , producto_solicitante__usuario=usuario).order_by("producto_solicitante")
    return render(request, "trueques/trueques_salientes.html", {"trueques": trueques})

@login_required
def trueques_por_concretar(request):
    usuario = request.user
    chk=check_cliente(usuario)
    if chk["ok"]:
        return chk["return"]
    trueques = Trueque.objects.exclude(activo=False).filter(Q(producto_solicitante__usuario=usuario) | Q(producto_solicitado__usuario=usuario), estado=3).order_by("-fecha")
    return render(request, "trueques/trueques_por_concretar.html", {"trueques": trueques})

@login_required
def trueques_finalizados(request):
    usuario = request.user
    chk=check_cliente(usuario)
    if chk["ok"]:
        return chk["return"]
    trueques = Trueque.objects.exclude(activo=False).filter(Q(producto_solicitante__usuario=usuario) | Q(producto_solicitado__usuario=usuario), estado__gte=4).order_by("-fecha")
    return render(request, "trueques/trueques_finalizados.html", {"trueques": trueques})