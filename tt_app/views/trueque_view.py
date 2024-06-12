from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from ..forms.trueque_forms import SolicitarForm
from ..forms.usuario_forms import check_cliente,check_empleado
from ..models import Producto, Trueque
from datetime import timedelta
from datetime import date

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
    trueques = Trueque.objects.exclude(activo=False).filter(Q(estado=1) | Q(estado=2),producto_solicitado__usuario=usuario).order_by("producto_solicitado")
    return render(request, "trueques/trueques_entrantes.html", {"trueques": trueques})

# @login_required
# def aceptar_solicitud(request, trueque_id):
#     if request.POST:
#         # Obtener el objeto trueque
#         trueque = get_object_or_404(Trueque, id=trueque_id)   

#         #trueques del solicitado (el que acepta la solicutud) que esten en estado solicitado para asignar en pendiente
#         trueques = Trueque.objects.exclude(activo=False).filter(producto_solicitado=trueque.producto_solicitante, estado=1)     
#         for tr in trueques:
#             tr.estado = 2 #pendiente
#             tr.save()

#         producto = Producto.objects.first(id=trueque.producto_solicitado.id)
#         producto.reservado = True
#         producto.save()

#         # Actualizar el trueque en la base de datos
#         trueque.estado = 3
#         trueque.save()        
#     return redirect(reverse("trueques_entrantes") + "?mensaje=La solicitud se aceptó correctamente")

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
    trueques = Trueque.objects.exclude(activo=False).filter(Q(producto_solicitante__usuario=usuario) | Q(producto_solicitado__usuario=usuario), estado=3).order_by('-fecha')
    return render(request, "trueques/trueques_por_concretar.html", {"trueques": trueques})

@login_required
def trueques_finalizados(request):
    usuario = request.user
    chk=check_cliente(usuario)
    if chk["ok"]:
        return chk["return"]
    trueques = Trueque.objects.exclude(activo=False).filter(Q(producto_solicitante__usuario=usuario) | Q(producto_solicitado__usuario=usuario), estado__gte=4).order_by('-fecha')
    return render(request, "trueques/trueques_finalizados.html", {"trueques": trueques})

@login_required
def aceptar_solicitud(request, trueque_id):
    if request.method == 'POST':
        # Obtener el objeto trueque
        trueque = get_object_or_404(Trueque, id=trueque_id)        
        # Actualizar el campo en la base de datos
        trueque.producto_solicitado.reservado = True
        trueque.producto_solicitado.save()
        s_pendientes = Trueque.objects.exclude(activo=False).exclude(id=trueque.id).filter(producto_solicitado = trueque.producto_solicitado,estado=1)
        for otra_solicitud in s_pendientes:
            otra_solicitud.estado = 2 #se le asigna estado pendiente
            otra_solicitud.save()
        trueques_enviados_anteriormente = Trueque.objects.exclude(activo=False).exclude(id=trueque.id).filter(producto_solicitante = trueque.producto_solicitado,estado=1)
        for otra_solicitud in trueques_enviados_anteriormente:
            otra_solicitud.estado = 7 #se le asigna estado 'cancelado por solicitante'
            otra_solicitud.save()
        trueque.estado = 3
        trueque.save()        
    return redirect(reverse("trueques_entrantes") + "?mensaje=La solicitud se aceptó correctamente")

@login_required
def cancelar_trueque(request,id,estado,ret):
    if request.POST:
        trueque = get_object_or_404(Trueque,id=id)
        if trueque.estado == 3: #3 = aceptado
            s_pendientes = Trueque.objects.exclude(activo=False).exclude(id=id).filter(producto_solicitado = trueque.producto_solicitado,estado=2)
            for otra_solicitud in s_pendientes:  
                otra_solicitud.estado = 1   #retorna todos los otros trueques pendientes a solicitados
                otra_solicitud.save()
            trueque.producto_solicitado.reservado = False #se debe guardar con un save() inmediatamente despues del cambio para simular un 'efecto cascada' en las tablas que no perte 
            trueque.producto_solicitado.save()
        trueque.producto_solicitante.reservado = False 
        trueque.producto_solicitante.save()
        trueque.estado = estado
        trueque.save() 
        """se debe guardar a mano la tabla productos asociada a la tabla trueque tanto para los productos solicitantes como para los solicitados. Al final se termina guardando la tabla trueque"""
        """Cada referencia a la que se le apliquen cambios (como trueque.producto_solicitado o trueque.producto_solicitante) requiere hacer un save() inmediatamente después para reflejar los cambios en la base de datos"""
        return {
            'salientes':redirect('trueques_salientes'),
            'por_concretar':redirect('trueques_por_concretar'),
        }.get(ret)
    else:
        return redirect('home')
    
@login_required
def solicitar(request,id):
    usuario = request.user
    chk=check_cliente(usuario)
    if chk["ok"]:
        return chk["return"]
    
    producto_solicitado =  get_object_or_404(Producto,id=id)
    if request.POST:
        form = SolicitarForm(request.POST,user=request.user,id=id)
        if form.is_valid():
            trueque = form.save(commit=False)
            if trueque.producto_solicitante.reservado:
                return redirect(
                reverse("trueques_salientes") + "?mensaje=No se pudo enviar la solicitud. Tu producto ya se encontraba reservado para otro trueque."
                )
            trueque.producto_solicitante.reservado = True
            trueque.producto_solicitante.save()
            trueque.producto_solicitado = producto_solicitado
            trueque.sucursal = producto_solicitado.sucursal
            trueque.save()
            return redirect(
                reverse("trueques_salientes") + "?mensaje=Se envió la solicitud."
            )
    else:
        form = SolicitarForm(user=request.user,id=id)
    return render(request, "trueques/solicitar.html", {   # enviamos los siguientes parámetros:
        "form": form,                           # el form definido en usuario_forms.py
        "titulo":"Solicitar intercambio",                 # el titulo del form
        "boton":"Solicitar",                  # el texto del botón de confirmación
        "obligatorios": False, # mostrar la advertencia de campos obligatorios o no
    })

@login_required
def rechazar_solicitud_interes(request, trueque_id):
    if request.method == 'POST':
        trueque = get_object_or_404(Trueque, id=trueque_id)
        trueque.estado = 5
        trueque.motivo_rechazo = 2
        trueque.save()
        
        producto = get_object_or_404(Producto,id=trueque.producto_solicitante.id)
        producto.reservado = False
        producto.save()
    return JsonResponse({'mensaje': 'La solicitud se rechazó correctamente'}, status=200)
    #return redirect(reverse("trueques_entrantes") + "?mensaje=La solicitud se rechazo correctamente")

def rechazar_solitud_horario(request, trueque_id):
    if request.method == 'POST':
        trueque = get_object_or_404(Trueque, id=trueque_id)
        trueque.estado = 5
        trueque.motivo_rechazo = 3
        trueque.save()
        
        producto = get_object_or_404(Producto,id=trueque.producto_solicitante.id)
        producto.reservado = False
        producto.save()
    return JsonResponse({'mensaje': 'La solicitud se rechazó correctamente'}, status=200)

def rechazar_solicitud_fecha(request, trueque_id):
    if request.method == 'POST':
        trueque = get_object_or_404(Trueque, id=trueque_id)
        trueque.estado = 5
        trueque.motivo_rechazo = 4
        trueque.save()
        
        producto = get_object_or_404(Producto,id=trueque.producto_solicitante.id)
        producto.reservado = False
        producto.save()
    return JsonResponse({'mensaje': 'La solicitud se rechazó correctamente'}, status=200)

def rechazar_solicitud_otros(request, trueque_id):
    if request.method == 'POST':
        trueque = get_object_or_404(Trueque, id=trueque_id)
        trueque.estado = 5
        trueque.motivo_rechazo = 5
        trueque.save()
        
        producto = get_object_or_404(Producto,id=trueque.producto_solicitante.id)
        producto.reservado = False
        producto.save()
    return JsonResponse({'mensaje': 'La solicitud se rechazó correctamente'}, status=200)

@login_required
def trueques_programados(request):
    usuario = request.user
    chk = check_empleado(usuario)
    if chk["ok"]:
        return chk["return"]
    hoy = date.today()
    print('fecha de hoy:', hoy)
    trueques_filtrados = Trueque.objects.exclude(activo=False).filter(fecha_programada=hoy, estado=3)
    print('coleccion de truques: ', trueques_filtrados)
    return render(request, "trueques/trueques_programados.html", {"trueques": trueques_filtrados,'hoy':hoy})
'''
@login_required
def trueques_hoy(request):
    hoy = date.today()
    trueques_filtrados = Trueque.objects.filter(fecha_programada=hoy)
    return render(request, 'trueques/partials/listado_trueques_programados.html', {'trueques': trueques_filtrados, 'hoy':hoy})
'''
'''
@login_required
def trueques_ayer(request):
    ayer = date.today() - timedelta(days=1)
    trueques_filtrados = Trueque.objects.filter(fecha_programada=ayer)
    return render(request, 'trueques/partials/listado_trueques_programados.html', {'trueques': trueques_filtrados,'hoy':ayer})
'''

def concretar_trueque(request, trueque_id):
    print("Hast acá llego!")
    if request.method == 'POST':
        trueque = get_object_or_404(Trueque, id=trueque_id)

        solicitudes_del_producto_solicitado = Trueque.objects.exclude(activo=False).filter(producto_solicitado_id=trueque.producto_solicitado.id, estado=2)
        for solicitud in solicitudes_del_producto_solicitado:
            solicitud.estado = 9
            solicitud.save()

        #trueque.producto_solicitado.usuario.reputacion++
        #trueque.producto_solicitante.usuario.reputacion++
        
        trueque.estado = 4
        trueque.save()

    return redirect(reverse("listar_ventas_trueque") + "?mensaje=El trueque se concretó correctamente")
