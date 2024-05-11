from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from ..models import productoModel, usuarioModel
from ..forms import CreacionDeProducto

def crear_producto(request):
    if request.method == 'POST':
        form = CreacionDeProducto(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.usuario = usuarioModel.Usuario.objects.get(id=2)
            producto.fecha_de_publicacion = timezone.now()  # Establecer la fecha de publicación antes de guardar
            producto.save()
            return redirect('productos')  # Redirige a la página de productos
    else:
        form = CreacionDeProducto()
    return render(request, 'crear_producto.html', {'form': form})

def productos(request):
    productos = productoModel.Producto.objects.exclude(activo=False).order_by('-promocionado')
    return render(request, "products/productos.html",{
        "productos": productos
    })

def buscar_productos(request):
    if request.method == 'GET':            
        cadena = request.GET.get('cadena')
        productos_nom = productoModel.Producto.objects.exclude(activo=False).filter(nombre__icontains=cadena)
        productos_desc = productoModel.Producto.objects.exclude(activo=False).filter(descripcion__icontains=cadena)
        productos = productos_nom.union(productos_desc).order_by('-promocionado')
        return render(request, "products/buscar_productos.html",{
            "productos": productos,
            "cadena":cadena
        })
    else:
        print('nao nao')
        return render(request, "products/productos.html",{
        "productos": productos
    })


def detalle_producto(request,id):
    producto = get_object_or_404(productoModel.Producto, id=id)
    return render(request,"products/detalle.html",{
        "producto": producto
    })