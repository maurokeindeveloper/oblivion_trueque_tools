from datetime import datetime, time 
from django.shortcuts import render
from ..forms.usuario_forms import check_administrador
from django.contrib.auth.decorators import login_required
from ..models import Venta


@login_required
def generar_estadisticas_ventas(request):
    chk = check_administrador(request.user)
    if chk["ok"]:
        return chk["return"]
   
    if request.method == 'POST':
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')
        
        # Convertir las fechas de string a objetos datetime
        fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d')
        fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d')
        
        # Ajustar fecha_fin para incluir todo el día
        fecha_fin = datetime.combine(fecha_fin, time.max)
        
        # Filtrar las ventas
        ventas = Venta.objects.filter(fecha__range=[fecha_inicio, fecha_fin], activo=True)
        
        # Realizar cálculos estadísticos
        total_ventas = ventas.count()
        suma_ventas = sum(venta.get_total() for venta in ventas)
        total_unidades = sum(venta.cantidad_unidades for venta in ventas)
        
        context = {
            'ventas': ventas,
            'total_ventas': total_ventas,
            'suma_ventas': suma_ventas,
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
        }
        return render(request, 'estadisticas/partials/resultados_estadisticas_ventas.html', context)
    else:
        # Si es una solicitud GET, solo renderiza el formulario
        return render(request, 'estadisticas/estadisticas_ventas.html')
        