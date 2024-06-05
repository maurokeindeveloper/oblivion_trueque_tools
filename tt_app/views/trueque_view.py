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
    chk=check_cliente(request.user)
    if chk["ok"]:
        return chk["return"]
    usuario = request.user
    print(f"Usuario autenticado: {usuario.email}")
    #trueques = Trueque.objects.all()
    trueques = Trueque.objects.exclude(activo=False).filter(producto_solicitado__usuario=usuario , estado=1)

    return render(request, "trueques/trueques_entrantes.html", {"trueques": trueques})

def aceptar_solicitud(request, trueque_id):
    if request.POST:
        # Obtener el objeto trueque
        trueque = get_object_or_404(Trueque, id=trueque_id)        
        # Actualizar el campo en la base de datos
        trueque.estado = 2
        trueque.save()        
    return redirect(reverse("trueques_entrantes") + "?mensaje=La solicitud se aceptó correctamente")


@login_required
def trueques_salientes(request):
    chk=check_cliente(request.user)
    if chk["ok"]:
        return chk["return"]
    usuario = request.user
    trueques = Trueque.objects.exclude(activo=False).filter(producto_solicitante__usuario=usuario , estado=1)
    return render(request, "trueques/trueques_salientes.html", {"trueques": trueques, "nombre": usuario.first_name})