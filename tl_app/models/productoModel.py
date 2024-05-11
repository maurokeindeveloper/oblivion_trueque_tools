from django.db import models
from django.db.models.fields.files import ImageField
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinLengthValidator

from . import usuarioModel

class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(
        validators=[ MinLengthValidator(10, "Este campo debe contener al menos 10 caracteres") ],
        max_length=550
    )
    class Categoria(models.IntegerChoices):
        categoria_1 = 1, _("$0-$4999")
        categoria_2 = 2, _("$5000-$9999")
        categoria_3 = 3, _("$10000+")
        
    categoria = models.IntegerField(choices=Categoria.choices)
    fecha_de_publicacion = models.DateTimeField(auto_now=True)
    
    imagen = ImageField(blank=True, upload_to="media/")
    promocionado = models.BooleanField(default=False)
    activo = models.BooleanField(default=True)
    usuario = models.ForeignKey(
        usuarioModel.Usuario, on_delete=models.CASCADE, related_name="productos"
    )
    def __str__(self):
        return self.nombre + '\t('+ str(self.usuario.id) + ')'