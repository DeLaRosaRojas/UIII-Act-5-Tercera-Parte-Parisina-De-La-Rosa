from django.contrib import admin
from .models import Cliente, Proveedor, Producto

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'correo_electronico', 'telefono', 'ciudad', 'fecha_registro')
    search_fields = ('nombre', 'apellido', 'correo_electronico')

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('nombre_empresa', 'contacto', 'correo', 'telefono', 'pais', 'fecha_registro')
    search_fields = ('nombre_empresa', 'contacto', 'correo')

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio', 'stock', 'cliente')
    search_fields = ('nombre', 'categoria')
    filter_horizontal = ('proveedores',) 