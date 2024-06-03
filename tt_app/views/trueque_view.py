from django.shortcuts import render
from django.contrib.auth.decorators import login_required
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
    chk=check_cliente(request.user)
    if chk["ok"]:
        return chk["return"]
    usuario = request.user
    print(f"Usuario autenticado: {usuario.email}")
    #trueques = Trueque.objects.all()
    trueques = Trueque.objects.exclude(activo=False).filter(producto_solicitado__usuario=usuario , estado=1)

    return render(request, "trueques/trueques_entrantes.html", {"trueques": trueques})

@login_required
def trueques_salientes(request):
    chk=check_cliente(request.user)
    if chk["ok"]:
        return chk["return"]
    usuario = request.user
    trueques = Trueque.objects.exclude(activo=False).filter(producto_solicitante__usuario=usuario , estado=1)
    return render(request, "trueques/trueques_salientes.html", {"trueques": trueques, "nombre": usuario.first_name})