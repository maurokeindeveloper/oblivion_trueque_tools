from django.shortcuts import render, redirect, get_object_or_404
from ..models import Producto
from ..forms import CreacionDeProducto

def crear_producto(request):
    if request.method == 'POST':
        form = CreacionDeProducto(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.usuario = Usuario.objects.get(id=2)
            producto.fecha_de_publicacion = timezone.now()  # Establecer la fecha de publicación antes de guardar
            producto.save()
            return redirect('productos')  # Redirige a la página de productos
    else:
        form = CreacionDeProducto()
    return render(request, 'crear_producto.html', {'form': form})


def productos(request):
    productos = Producto.objects.all().order_by('nombre')
    return render(request, "products/productos.html",{
        "productos": productos
    })
def buscar_productos(request,cadena):
    productos = Producto.objects.filter(nombre__icontains=cadena).filter(descripcion__icontains=cadena)
    return render(request, "products/buscar_productos.html",{
        "productos": productos,
        "cadena":cadena
    })
def detalle_producto(request,id):
    producto = get_object_or_404(Producto, id=id)
    return render(request,"products/detalle.html",{
        "producto": producto
    })