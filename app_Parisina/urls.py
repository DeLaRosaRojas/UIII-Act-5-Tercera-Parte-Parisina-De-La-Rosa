from django.urls import path
from . import views

urlpatterns = [
    path("", views.inicio_parisina, name="inicio_parisina"),
    path("cliente/agregar/", views.agregar_cliente, name="agregar_cliente"),
    path("cliente/ver/", views.ver_cliente, name="ver_cliente"),
    path("cliente/actualizar/<int:pk>/", views.actualizar_cliente, name="actualizar_cliente"),
    path("cliente/realizar_actualizacion/<int:pk>/", views.realizar_actualizacion_cliente, name="realizar_actualizacion_cliente"),
    path("cliente/borrar/<int:pk>/", views.borrar_cliente, name="borrar_cliente"),

    # ---------- RUTAS PROVEEDOR ----------
    path("proveedor/agregar/", views.agregar_proveedor, name="agregar_proveedor"),
    path("proveedor/ver/", views.ver_proveedor, name="ver_proveedor"),
    path("proveedor/actualizar/<int:pk>/", views.actualizar_proveedor, name="actualizar_proveedor"),
    path("proveedor/realizar_actualizacion/<int:pk>/", views.realizar_actualizacion_proveedor, name="realizar_actualizacion_proveedor"),
    path("proveedor/borrar/<int:pk>/", views.borrar_proveedor, name="borrar_proveedor"),

    #---------- RUTAS PRODUCTO ----------
    path("producto/agregar/", views.agregar_producto, name="agregar_producto"),
    path("producto/ver/", views.ver_producto, name="ver_producto"),
    path("producto/actualizar/<int:pk>/", views.actualizar_producto, name="actualizar_producto"),
    path("producto/realizar_actualizacion/<int:pk>/", views.realizar_actualizacion_producto, name="realizar_actualizacion_producto"),
    path("producto/borrar/<int:pk>/", views.borrar_producto, name="borrar_producto"),
]