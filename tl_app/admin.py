from django.contrib import admin
from .models import productoModel, usuarioModel
# Register your models here.
admin.site.register(productoModel.Producto)
admin.site.register(usuarioModel.Usuario)