from django.shortcuts import render, redirect, get_object_or_404
from .models import Cliente, Proveedor,  Producto
from django.urls import reverse

# Página inicio del sistema
def inicio_parisina(request):
    return render(request, "inicio.html")

# Agregar cliente (muestra formulario y procesa POST)
def agregar_cliente(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre", "").strip()
        apellido = request.POST.get("apellido", "").strip()
        correo = request.POST.get("correo_electronico", "").strip()
        telefono = request.POST.get("telefono", "").strip()
        direccion = request.POST.get("direccion", "").strip()
        ciudad = request.POST.get("ciudad", "").strip()

        Cliente.objects.create(
            nombre=nombre,
            apellido=apellido,
            correo_electronico=correo,
            telefono=telefono,
            direccion=direccion,
            ciudad=ciudad
        )
        return redirect("ver_cliente")
    return render(request, "Cliente/agregar_Cliente.html")

# Ver clientes (lista en tabla)
def ver_cliente(request):
    clientes = Cliente.objects.all().order_by("-fecha_registro")
    return render(request, "Cliente/ver_Cliente.html", {"clientes": clientes})

# Mostrar formulario para actualizar cliente
def actualizar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    return render(request, "Cliente/actualizar_Cliente.html", {"cliente": cliente})

# Procesar la actualización (acción POST)
def realizar_actualizacion_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == "POST":
        cliente.nombre = request.POST.get("nombre", cliente.nombre)
        cliente.apellido = request.POST.get("apellido", cliente.apellido)
        cliente.correo_electronico = request.POST.get("correo_electronico", cliente.correo_electronico)
        cliente.telefono = request.POST.get("telefono", cliente.telefono)
        cliente.direccion = request.POST.get("direccion", cliente.direccion)
        cliente.ciudad = request.POST.get("ciudad", cliente.ciudad)
        cliente.save()
        return redirect("ver_cliente")
    # si no es POST, redirigir a formulario
    return redirect("actualizar_cliente", pk=pk)

# Borrar cliente (confirmación GET y eliminación POST)
def borrar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == "POST":
        cliente.delete()
        return redirect("ver_cliente")
    return render(request, "Cliente/borrar_Cliente.html", {"cliente": cliente})



# ----- VISTAS NUEVAS (Proveedor) -----
def agregar_proveedor(request):
    """
    Muestra formulario y procesa POST para crear un Proveedor.
    No usa forms.py, no valida entrada (tal como pediste).
    """
    if request.method == "POST":
        nombre_empresa = request.POST.get("nombre_empresa", "").strip()
        contacto = request.POST.get("contacto", "").strip()
        correo = request.POST.get("correo", "").strip()
        telefono = request.POST.get("telefono", "").strip()
        direccion = request.POST.get("direccion", "").strip()
        pais = request.POST.get("pais", "").strip()

        Proveedor.objects.create(
            nombre_empresa=nombre_empresa,
            contacto=contacto,
            correo=correo,
            telefono=telefono,
            direccion=direccion,
            pais=pais
        )
        return redirect("ver_proveedor")

    return render(request, "proveedor/agregar_proveedor.html")


def ver_proveedor(request):
    """
    Lista todos los proveedores en orden descendente por fecha_registro.
    """
    proveedores = Proveedor.objects.all().order_by("-fecha_registro")
    return render(request, "proveedor/ver_proveedor.html", {"proveedores": proveedores})


def actualizar_proveedor(request, pk):
    """
    Muestra formulario de edición con datos del proveedor (GET).
    """
    proveedor = get_object_or_404(Proveedor, pk=pk)
    return render(request, "proveedor/actualizar_proveedor.html", {"proveedor": proveedor})


def realizar_actualizacion_proveedor(request, pk):
    """
    Procesa POST para guardar cambios en el proveedor.
    """
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == "POST":
        proveedor.nombre_empresa = request.POST.get("nombre_empresa", proveedor.nombre_empresa)
        proveedor.contacto = request.POST.get("contacto", proveedor.contacto)
        proveedor.correo = request.POST.get("correo", proveedor.correo)
        proveedor.telefono = request.POST.get("telefono", proveedor.telefono)
        proveedor.direccion = request.POST.get("direccion", proveedor.direccion)
        proveedor.pais = request.POST.get("pais", proveedor.pais)
        proveedor.save()
        return redirect("ver_proveedor")
    return redirect("actualizar_proveedor", pk=pk)


def borrar_proveedor(request, pk):
    """
    Confirmación GET y eliminación POST.
    """
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == "POST":
        proveedor.delete()
        return redirect("ver_proveedor")
    return render(request, "proveedor/borrar_proveedor.html", {"proveedor": proveedor})


# -----------------------
# CRUD PRODUCTO
# -----------------------

def agregar_producto(request):
    """
    Muestra formulario para crear Producto. No usa forms.py.
    Cliente: select (FK) - seleccionar 1.
    Proveedores: select multiple (ManyToMany).
    """
    clientes = Cliente.objects.all().order_by("nombre")
    proveedores = Proveedor.objects.all().order_by("nombre_empresa")

    if request.method == "POST":
        nombre = request.POST.get("nombre", "").strip()
        descripcion = request.POST.get("descripcion", "").strip()
        categoria = request.POST.get("categoria", "").strip()
        precio = request.POST.get("precio", "0").strip()
        stock = request.POST.get("stock", "0").strip()
        cliente_id = request.POST.get("cliente")  # puede ser None
        proveedores_ids = request.POST.getlist("proveedores")  # lista de ids (puede ser [])


        # crear producto (cliente puede ser None si no select)
        cliente_obj = Cliente.objects.get(pk=cliente_id) if cliente_id else None

        producto = Producto.objects.create(
            nombre=nombre,
            descripcion=descripcion,
            categoria=categoria,
            precio=precio or 0,
            stock=stock or 0,
            cliente=cliente_obj
        )

        # asignar proveedores (many-to-many) si hay
        if proveedores_ids:
            producto.proveedores.set(proveedores_ids)

        return redirect("ver_producto")

    return render(request, "producto/agregar_producto.html", {
        "clientes": clientes,
        "proveedores": proveedores
    })


def ver_producto(request):
    productos = Producto.objects.all().order_by("-id")
    return render(request, "producto/ver_producto.html", {"productos": productos})


def actualizar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    clientes = Cliente.objects.all().order_by("nombre")
    proveedores = Proveedor.objects.all().order_by("nombre_empresa")
    return render(request, "producto/actualizar_producto.html", {
        "producto": producto,
        "clientes": clientes,
        "proveedores": proveedores
    })


def realizar_actualizacion_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == "POST":
        producto.nombre = request.POST.get("nombre", producto.nombre)
        producto.descripcion = request.POST.get("descripcion", producto.descripcion)
        producto.categoria = request.POST.get("categoria", producto.categoria)
        producto.precio = request.POST.get("precio", producto.precio)
        producto.stock = request.POST.get("stock", producto.stock)

        cliente_id = request.POST.get("cliente")
        if cliente_id:
            producto.cliente = Cliente.objects.get(pk=cliente_id)
        else:
            producto.cliente = None

        producto.save()

        proveedores_ids = request.POST.getlist("proveedores")
        # ajustar relaciones many-to-many
        producto.proveedores.set(proveedores_ids)

        return redirect("ver_producto")

    return redirect("actualizar_producto", pk=pk)


def borrar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == "POST":
        producto.delete()
        return redirect("ver_producto")
    return render(request, "producto/borrar_producto.html", {"producto": producto})