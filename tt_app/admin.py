from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Producto, Trueque, Sucursal, Venta

# Register your models here.


class CustomUserAdmin(UserAdmin):
    list_display = ("email", "date_joined", "last_login", "is_admin", "is_staff")
    search_fields = ("email",)
    readonly_fields = ("id", "date_joined", "last_login")

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Usuario, CustomUserAdmin)
admin.site.register(Producto)
admin.site.register(Trueque)
admin.site.register(Sucursal)
admin.site.register(Venta)

