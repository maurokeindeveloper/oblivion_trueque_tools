from django.db import models
from django.db import models
from django.db.models.fields.files import ImageField
from django.db.models.query import QuerySet
from ckeditor.fields import RichTextField
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinLengthValidator


# Create your models here.
class Usuario(models.Model):
    email = models.EmailField(default="NULL")
    password = models.CharField(max_length=100)
    telefono = models.CharField(max_length=25)
    fecha_de_nacimiento = models.DateField(null=True, blank=True)
    DNI = models.CharField(max_length=10, null=True, blank=True)
    activo = models.BooleanField(default=True)


class Producto(models.Model):
    class Categoria(models.IntegerChoices):
        categoria_1 = 1, _("$0-$4999")
        categoria_2 = 2, _("$5000-$9999")
        categoria_3 = 3, _("$10000+")

    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(
        validators=[
            MinLengthValidator(10, "Este campo debe contener al menos 10 caracteres")
        ]
    )
    categoria = models.IntegerField(choices=Categoria.choices)
    fecha_de_publicacion = models.DateTimeField(auto_now=True)
    usuario = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, related_name="productos"
    )
    imagen = ImageField(null=True, blank=True, upload_to="media/")
    promocionado = models.BooleanField(default=False)
    activo = models.BooleanField(default=True)
