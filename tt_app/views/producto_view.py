from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from ..forms.producto_forms import (
    CreacionDeProducto,
    FormularioDePregunta,
    FormularioDeRespuesta,
)
from ..forms.usuario_forms import check_cliente
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from ..models import Producto, Pregunta,Trueque
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from datetime import date
from django.db.models import Q

@login_required
def crear_producto(request):
    chk = check_cliente(request.user)
    if chk["ok"]:
        return chk["return"]
    if request.POST:
        form = CreacionDeProducto(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save(commit=False)  
            producto.usuario = request.user # Asignar el usuario autenticado al producto
            producto.fecha_de_publicacion = timezone.now()  # Establecer la fecha de publicación antes de guardar
            producto.nombre = producto.nombre.capitalize()
            producto.save() # guardamos el producto
            # Redirigir a la página de productos con mensaje de feedback
            return redirect(
                reverse("productos")
                + "?mensaje=El producto se ha agregado correctamente."
            )
    else:
        form = CreacionDeProducto()
    return render(
        request,
        "productos/crear_producto.html",
        {  # enviamos los siguientes parámetros:
            "form": form,  # el form definido en producto_forms.py
            "titulo": "Publicar producto",  # el titulo del form
            "boton": "Aceptar",  # el texto del botón de confirmación
            "obligatorios": True,  # mostrar la advertencia de campos obligatorios o no
        },
    )

@login_required
def modificar_producto(request,id):
    chk = check_cliente(request.user)
    if chk["ok"]:
        return chk["return"]
    
    producto = get_object_or_404(Producto,id=id) # Obtenemos el producto a modificar 

    if request.POST:
        form = CreacionDeProducto(request.POST,request.FILES, instance = producto) # palabra clave instance sirve para sobre
        if form.is_valid():
            form = form.save(commit=False)
            form.fecha_de_publicacion = producto.fecha_de_publicacion  # Establecer la fecha de publicación antes de guardar
            form.nombre = form.nombre.capitalize()
            form.save() # guardamos el producto
            # Redirigir a la página de productos con mensaje de feedback
            return redirect(
                reverse("mis_productos", args=[request.user.id])
                + "?mensaje=El producto se ha modificado correctamente."
            )
    else:
        form = CreacionDeProducto(instance = producto)
    return render(
        request,
        "productos/crear_producto.html",
        {  # enviamos los siguientes parámetros:
            "form": form,  # el form definido en producto_forms.py
            "titulo": "Modificar producto",  # el titulo del form
            "boton": "Modificar",  # el texto del botón de confirmación
            "obligatorios": False,  # mostrar la advertencia de campos obligatorios o no
        },
    )
    

@login_required
def eliminar_producto(request,id):
    chk = check_cliente(request.user)
    if chk["ok"]:
        return chk["return"]
    if request.method == 'POST':
        # Obtener el producto si es que existe
        producto = get_object_or_404(Producto, id=id)    
        print("eliminando "+producto.nombre+"...")    
        # Rechazar solicitudes recibidas, motivo 'Producto no disponible'    
        for solicitud in Trueque.objects.exclude(activo=False).filter(Q(estado=1)|Q(estado=2), producto_solicitado=producto):
            solicitud.estado=5 #rechazado
            solicitud.motivo_rechazo=1 #Producto no disponible.
            solicitud.save()
            solicitud.producto_solicitante.reservado=False # desmarcamos el solicitante
            solicitud.producto_solicitante.save()
        # Cancelar solicitudes enviadas
        for solicitud in Trueque.objects.exclude(activo=False).filter(Q(estado=1)|Q(estado=2), producto_solicitante=producto):
            solicitud.estado=7
            solicitud.save()
        # Cancelar trueque por concretar si es que tiene
        for trueque in Trueque.objects.exclude(activo=False).filter(producto_solicitado=producto, estado=3):
            trueque.estado=7
            trueque.save()
            trueque.producto_solicitante.reservado=False # desmarcamos el otro producto
            trueque.producto_solicitante.save()
        for trueque in Trueque.objects.exclude(activo=False).filter(producto_solicitante=producto, estado=3):
            trueque.estado=7
            trueque.save()
            trueque.producto_solicitado.reservado=False # desmarcamos el otro producto
            trueque.producto_solicitado.save()
        # Marcar producto como no disponible
        producto.reservado=True
        producto.disponible=False
        producto.activo=False        
        producto.save()
        return redirect(reverse("mis_productos", args=[request.user.id]) + "?mensaje=El producto se eliminó correctamente.")
    else:
        return redirect(reverse("mis_productos", args=[request.user.id]) + "?mensaje=No se pudo eliminar el producto. Algo salió mal")


def productos(request):
    productos = Producto.objects.exclude(activo=False).order_by("fecha_de_publicacion").order_by("-promocionado")
    return render(request, "productos/productos.html", {"productos": productos})


def buscar_productos(request):
    if request.method == "GET":
        cadena = request.GET.get("cadena")
        productos_nom = Producto.objects.exclude(activo=False).filter(
            nombre__icontains=cadena
        )
        productos_desc = Producto.objects.exclude(activo=False).filter(
            descripcion__icontains=cadena
        )
        productos = productos_nom.union(productos_desc).order_by("-promocionado")
        return render(
            request,
            "productos/buscar_productos.html",
            {
                "productos": productos,
                "cadena": cadena,
            },
        )
    else:
        return render(request, "productos/productos.html", {"productos": productos})
    
def buscar_productos_trueques_programados(request):
    if request.method == "GET":
        cadena = request.GET.get("cadena")
        print(cadena)
        trueques_filtrados = Trueque.objects.exclude(activo=False).filter( Q(producto_solicitante__nombre__icontains=cadena) | Q(producto_solicitado__nombre__icontains=cadena)|Q(producto_solicitante__usuario__first_name__icontains=cadena)|Q(producto_solicitado__usuario__first_name__icontains=cadena),estado=3,fecha_programada=date.today())
        
        return render(
            request,
            "trueques/trueques_programados.html",
            {
                "trueques": trueques_filtrados,
                "cadena": cadena,
            },
        )
    else:
        return render(request, "trueques/trueques_programados.html", {"trueques": trueques_filtrados})


def detalle_producto(request, id):
    producto = get_object_or_404(Producto, id=id)

    # Lista de preguntas acerca del producto
    preguntas = producto.preguntas.all().order_by("-fecha")

    # Formulario para las preguntas de los clientes
    form_pregunta = FormularioDePregunta()
    # Formulario para las respuestas de los dueños 
    
    form_respuesta = FormularioDeRespuesta()
    return render(
        request,
        "productos/detalle_producto.html",
        {"producto": producto, "preguntas": preguntas, "form_pregunta": form_pregunta, "form_respuesta": form_respuesta},
    )


@login_required
def preguntar(request, id):
    chk = check_cliente(request.user)
    if chk["ok"]:
        return chk["return"]
    producto = get_object_or_404(Producto, id=id)

    pregunta = None
    # Se realiza una pregunta
    form = FormularioDePregunta(data=request.POST)
    if form.is_valid():
        # Crea un objeto Pregunta sin guardarlo en la base de datos
        pregunta = form.save(commit=False)
        # Asigna el producto y el cliente a la pregunta - DEBEN SER LOS OBJETOS, NO LOS VALORES (O IDS)
        pregunta.producto = producto
        pregunta.cliente = request.user
        # Guarda la pregunta en la base de datos
        pregunta.save()
    return redirect(
        'detalle_producto', producto.id
    )


@login_required
def responder(request, id):
    chk = check_cliente(request.user)
    if chk["ok"]:
        return chk["return"]
    pregunta = get_object_or_404(Pregunta, id=id)
    respuesta = None
    # Booleano para controlar la vista
    enviada = False
    # Se responde la pregunta
    form_respuesta = FormularioDeRespuesta(data=request.POST)
    if form_respuesta.is_valid():
        # Crea un objeto Respuesta sin guardarlo en la base de datos
        respuesta = form_respuesta.save(commit=False)
        respuesta.pregunta = pregunta
        # Guarda la respuesta en la base de datos
        respuesta.save()
        enviada = True
        # Asigna la respuesta a la pregunta correspondiente y actualiza la BD
        pregunta.respuesta = respuesta
        pregunta.save()
    return redirect(
        "detalle_producto", pregunta.producto.id
    )

def filtrar_productos(request, categoria):
    nombre_categoria = {
        1: "$0-$5000",
        2: "$5000-$10000",
        3: "$10000+",
    }
    if request.method == "GET":
        productos = Producto.objects.exclude(activo=False).filter(categoria=categoria)
        return render(
            request,
            "productos/filtrar_productos.html",
            {"productos": productos, "categoria": nombre_categoria.get(categoria)},
        )
    else:
        return render(request, "productos/productos.html", {"productos": productos})

def mis_productos(request,id):
    productos = Producto.objects.exclude(activo=False).filter(usuario__id=id).order_by("fecha_de_publicacion")
    return render(request, "productos/mis_productos.html", {"productos": productos})
