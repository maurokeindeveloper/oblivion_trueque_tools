from django.db import models
from django.db.models.fields.files import ImageField
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from datetime import datetime


# Create your models here.
# Creating users and superusers


# Modelo de sucursal
class Sucursal(models.Model):
    ciudad = models.CharField(max_length=50)
    direccion = models.CharField(max_length=200)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.ciudad + " - " + self.direccion


class MyCustomUserManager(BaseUserManager):
    def create_cliente(
        self, email, first_name, last_name, dni, phone, birthdate, password=None
    ):
        if not email:
            raise ValueError("El nombre de usuario debe ser tu correo electrónico.")
        cliente = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            dni=dni,
            phone=phone,
            birthdate=birthdate,
        )
        cliente.set_password(password)
        cliente.save(using=self._db)
        return cliente

    def create_empleado(self, email, first_name, last_name, password, sucursal):
        if not email:
            raise ValueError("El nombre de usuario debe ser tu correo electrónico.")
        empleado = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            sucursal=sucursal,
        )
        empleado.is_staff = True
        empleado.set_password(password)
        empleado.save(using=self._db)
        return empleado

    def create_superuser(self, email, password):
        user = self.create_cliente(
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
        # user.is_superuser = True #Comento esta línea porque no tendría que tener permitido el acceso al panel de administración de django
        user.save(using=self._db)
        return user


# User model
class Usuario(AbstractBaseUser):
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
    sucursal = models.ForeignKey(
        Sucursal, on_delete=models.CASCADE, related_name="empleados", null=True
    )

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
    fecha_de_publicacion = models.DateTimeField(auto_now=False)

    imagen = ImageField(blank=True, upload_to="media/")
    promocionado = models.BooleanField(default=False)
    reservado = models.BooleanField(default=False)
    disponible = models.BooleanField(default=True)
    activo = models.BooleanField(default=True)
    usuario = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, related_name="productos"
    )
    sucursal = models.ForeignKey(
        Sucursal, on_delete=models.CASCADE, related_name="productos"
    )
    fecha_hasta_promocion = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.nombre + "\t(" + str(self.categoria) + ")"


# Modelo de trueque
class Trueque(models.Model):
    producto_solicitante = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name="trueque",
        null=False,
        blank=False,
    )
    producto_solicitado = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name="trueque_solicitado",
        null=False,
        blank=False,
    )
    sucursal = models.ForeignKey(
        Sucursal,
        on_delete=models.CASCADE,
        related_name="trueques",
        null=False,
        blank=False,
    )
    activo = models.BooleanField(default=True)
    fecha = models.DateField(auto_now=True)
    fecha_programada = models.DateField(default="2025-01-01", blank=True)

    class Rango_Horario(models.IntegerChoices):
        rango_1 = 1, _("Turno Mañana: 8 AM")
        rango_2 = 2, _("Turno Mañana: 9 AM")
        rango_3 = 3, _("Turno Mañana: 10 AM")
        rango_4 = 4, _("Turno Mañana: 11 AM")
        rango_5 = 5, _("Turno Tarde: 3 PM")
        rango_6 = 6, _("Turno Tarde: 4 PM")
        rango_7 = 7, _("Turno Tarde: 5 PM")
        rango_8 = 8, _("Turno Tarde: 6 PM")
        rango_9 = 9, _("Turno Tarde: 7 PM")

    horario = models.IntegerField(
        choices=Rango_Horario.choices, blank=False, null=False, default=1
    )

    class Estado(models.IntegerChoices):
        estado_1 = 1, _("Solicitado")
        estado_2 = 2, _("Pendiente")
        estado_3 = 3, _("Aceptado")
        estado_4 = 4, _("Concretado")
        estado_5 = 5, _("Rechazado")
        estado_6 = 6, _("Cancelado por empleado")
        estado_7 = 7, _("Cancelado por solicitante")
        estado_8 = 8, _("Cancelado por solicitado")
        estado_9 = 9, _("Concretó otro trueque")

    estado = models.IntegerField(choices=Estado.choices, default=1)

    class OpcionRechazo(models.IntegerChoices):
        rechazo_1 = 1, _("Producto ya no disponible")
        rechazo_2 = 2, _("Falta de interés en el producto ofrecido")
        rechazo_3 = 3, _("Falta de disponibilidad en el horario solicitado")
        rechazo_4 = 4, _("Falta de disponibilidad en la fecha solicitada")
        rechazo_5 = 5, _("Otros motivos")

    motivo_rechazo = models.IntegerField(
        choices=OpcionRechazo.choices, blank=True, null=True, default=None
    )

    def __str__(self):
        p1 = self.producto_solicitante
        p2 = self.producto_solicitado
        return (
            "("
            + str(self.id)
            + ")  "
            + p1.usuario.first_name
            + " quiere intercambiar "
            + p1.nombre
            + " por "
            + p2.nombre
            + " de "
            + p2.usuario.first_name
        )


# Modelo de respuesta
class Respuesta(models.Model):
    texto = models.CharField(max_length=200)
    fecha = models.DateField(auto_now=True)
    activo = models.BooleanField(default=True)


# Modelo de pregunta
class Pregunta(models.Model):
    producto = models.ForeignKey(
        Producto, on_delete=models.CASCADE, related_name="preguntas"
    )
    cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    texto = models.CharField(max_length=200)
    respuesta = models.ForeignKey(Respuesta, on_delete=models.CASCADE, null=True)
    fecha = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True)


# Modelo de venta
class Venta(models.Model):
    cantidad_unidades = models.IntegerField()
    precio_unitario = models.FloatField()
    nombre_producto = models.CharField(max_length=200)
    trueque = models.ForeignKey(
        Trueque, on_delete=models.CASCADE, blank=True, null=True
    )
    vendedor = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, blank=True, null=True
    )
    fecha = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True)

    def get_total(self):
        return self.cantidad_unidades * self.precio_unitario
