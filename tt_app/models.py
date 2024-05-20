from django.db import models
from django.db.models.fields.files import ImageField
from django.db.models.query import QuerySet
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Create your models here.
# Creating users and superusers
class MyCustomUserManager(BaseUserManager):
    def create_user(
        self, email, first_name, last_name, dni, phone, birthdate, password=None
    ):
        if not email:
            raise ValueError("El nombre de usuario debe ser tu correo electrónico.")
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            dni=dni,
            phone=phone,
            birthdate=birthdate,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            first_name="",
            last_name="",
            dni="",
            phone="",
            birthdate="1900-01-01",
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


# User model
class CustomUser(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30, blank=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    dni = models.CharField(max_length=10, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    birthdate = models.DateField(default="1990-01-01", blank=True)
    hide_email = models.BooleanField(default=True)

    objects = MyCustomUserManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


# Product model
class Producto(models.Model):

    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(
        validators=[
            MinLengthValidator(10, "Este campo debe contener al menos 10 caracteres")
        ],
        max_length=1000,
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
        CustomUser, on_delete=models.CASCADE, related_name="productos"
    )

    def __str__(self):
        return self.nombre + "\t(" + str(self.usuario.id) + ")"
