from django.db import models
from django.db.models.fields.files import ImageField
from django.db.models.query import QuerySet
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinLengthValidator

class Usuario(models.Model):
    email = models.EmailField(default="NULL")
    password = models.CharField(max_length=100)
    telefono = models.CharField(max_length=25)
    fecha_de_nacimiento = models.DateField(null=True, blank=True)
    DNI = models.CharField(max_length=10, null=True, blank=True)
    activo = models.BooleanField(default=True)
