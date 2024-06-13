from django.http import JsonResponse
from django.shortcuts import get_list_or_404, render
import json
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from ..forms.venta_forms import CrearVenta
from ..models import Trueque, Venta, Usuario
from django.db.models import Sum

@login_required
def registrar_ventas(request, trueque_id):
    print("entro")
    try:
        trueque = Trueque.objects.get(id=trueque_id)
    except Trueque.DoesNotExist:
        return redirect(reverse("home"))
    if trueque.estado==4:
        return redirect(reverse("home") + "?mensaje=El trueque está concretado. No se pueden registrar más ventas.")
    if trueque.estado!=3:
        return redirect(reverse("home") + "?mensaje=El trueque debe estar ACEPTADO para registrar ventas.")
    
    ventas = Venta.objects.filter(trueque_id=trueque_id)

    if request.method == 'POST':
        form = CrearVenta(request.POST)
        if form.is_valid():
            try:
                venta = form.save()
                venta.trueque_id = trueque_id
                venta.vendedor_id = request.user.id
                #tenemos que agregar fecha de la venta
                venta.save()

                ventas = Venta.objects.filter(trueque_id=trueque_id)

                # Procesa el array aquí
                print(ventas) 
            except json.JSONDecodeError:
                return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
            
    else:
        form = CrearVenta()
        #return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)
    return render(
        request,
        "ventas/venta.html",
        {  # enviamos los siguientes parámetros:
            "form": form,  # el form definido en producto_forms.py
            "titulo": "Agregar venta",  # el titulo del form
            "boton": "Aceptar",  # el texto del botón de confirmación
            "obligatorios": True,  # mostrar la advertencia de campos obligatorios o no
            "ventas": ventas,
            "trueque_id": trueque_id
        }
    )

@login_required
def listar_ventas(request, trueque_id):
    #ventas = get_list_or_404(Venta, trueque_id=trueque_id)
    ventas = Venta.objects.filter(trueque_id=trueque_id)
    trueque = get_object_or_404(Trueque, id=trueque_id)
    if trueque.estado!=4:
        return redirect(reverse("home"))
    
    total = 0
    for venta in ventas:
        total = total + venta.get_total()  
    
    return render(
        request,
        "ventas/listado_ventas_trueque.html",
        {
            "ventas": ventas,
            "trueque": trueque,
            "total": total
        }
    )