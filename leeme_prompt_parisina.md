Perfecto 💪 Vamos a estructurar **la Tercera Parte del proyecto *Parisina*** paso a paso, basada en lo que ya hiciste con *Cliente* y *Proveedor*, pero ahora trabajando con el **MODELO: PRODUCTO**, que incluye relaciones con ambas tablas.

---

## 🧵 **PROYECTO: PARISINA — Tercera Parte (Producto)**

### 📁 1. Datos generales

* **Lenguaje:** Python
* **Framework:** Django
* **Editor:** VS Code
* **Carpeta raíz:** `UIII_Parisina_0777`
* **Proyecto:** `backend_Parisina`
* **Aplicación:** `app_Parisina`

---

### 🧩 2. Modelo `models.py`

Ya existente:

```python
# ==========================================
# MODELO: PRODUCTO
# ==========================================
class Producto(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField()
    categoria = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='productos')
    proveedores = models.ManyToManyField(Proveedor, related_name='productos')

    def __str__(self):
        return self.nombre
```

---

### ⚙️ 3. Migraciones

En la terminal de VS Code:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### 🧠 4. Vistas `views.py` (CRUD de Producto)

En `app_Parisina/views.py` agregar:

```python
from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto, Cliente, Proveedor

# AGREGAR PRODUCTO
def agregar_producto(request):
    clientes = Cliente.objects.all()
    proveedores = Proveedor.objects.all()

    if request.method == 'POST':
        nombre = request.POST['nombre']
        descripcion = request.POST['descripcion']
        categoria = request.POST['categoria']
        precio = request.POST['precio']
        stock = request.POST['stock']
        cliente_id = request.POST['cliente']
        proveedores_ids = request.POST.getlist('proveedores')

        cliente = Cliente.objects.get(id=cliente_id)
        producto = Producto.objects.create(
            nombre=nombre,
            descripcion=descripcion,
            categoria=categoria,
            precio=precio,
            stock=stock,
            cliente=cliente
        )
        producto.proveedores.set(proveedores_ids)
        return redirect('ver_producto')

    return render(request, 'producto/agregar_producto.html', {'clientes': clientes, 'proveedores': proveedores})


# VER PRODUCTO
def ver_producto(request):
    productos = Producto.objects.all()
    return render(request, 'producto/ver_producto.html', {'productos': productos})


# ACTUALIZAR PRODUCTO
def actualizar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    clientes = Cliente.objects.all()
    proveedores = Proveedor.objects.all()
    return render(request, 'producto/actualizar_producto.html', {'producto': producto, 'clientes': clientes, 'proveedores': proveedores})


# REALIZAR ACTUALIZACIÓN
def realizar_actualizacion_producto(request, id):
    producto = get_object_or_404(Producto, id=id)

    if request.method == 'POST':
        producto.nombre = request.POST['nombre']
        producto.descripcion = request.POST['descripcion']
        producto.categoria = request.POST['categoria']
        producto.precio = request.POST['precio']
        producto.stock = request.POST['stock']
        cliente_id = request.POST['cliente']
        proveedores_ids = request.POST.getlist('proveedores')

        producto.cliente = Cliente.objects.get(id=cliente_id)
        producto.proveedores.set(proveedores_ids)
        producto.save()
        return redirect('ver_producto')


# BORRAR PRODUCTO
def borrar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    if request.method == 'POST':
        producto.delete()
        return redirect('ver_producto')
    return render(request, 'producto/borrar_producto.html', {'producto': producto})
```

---

### 🌐 5. URLS — `app_Parisina/urls.py`

Agregar las rutas:

```python
from django.urls import path
from . import views

urlpatterns = [
    # PRODUCTO
    path('agregar_producto/', views.agregar_producto, name='agregar_producto'),
    path('ver_producto/', views.ver_producto, name='ver_producto'),
    path('actualizar_producto/<int:id>/', views.actualizar_producto, name='actualizar_producto'),
    path('realizar_actualizacion_producto/<int:id>/', views.realizar_actualizacion_producto, name='realizar_actualizacion_producto'),
    path('borrar_producto/<int:id>/', views.borrar_producto, name='borrar_producto'),
]
```

> ⚠️ Recuerda también importar este archivo en el `urls.py` principal de `backend_Parisina`.

---

### 🧱 6. Plantillas HTML

Crea la carpeta:

```
app_Parisina/templates/producto/
```

Y dentro, los siguientes archivos:

#### 🟥 `agregar_producto.html`

Formulario con *combobox* de Cliente y Proveedor:

```html
{% extends 'base.html' %}
{% block content %}
<div class="container mt-4">
  <h2 class="text-danger">Agregar Producto</h2>
  <form method="POST">
    {% csrf_token %}
    <input type="text" name="nombre" class="form-control mb-2" placeholder="Nombre">
    <textarea name="descripcion" class="form-control mb-2" placeholder="Descripción"></textarea>
    <input type="text" name="categoria" class="form-control mb-2" placeholder="Categoría">
    <input type="number" step="0.01" name="precio" class="form-control mb-2" placeholder="Precio">
    <input type="number" name="stock" class="form-control mb-2" placeholder="Stock">

    <label class="text-dark fw-bold">Cliente:</label>
    <select name="cliente" class="form-select mb-2">
      {% for c in clientes %}
        <option value="{{ c.id }}">{{ c.nombre }}</option>
      {% endfor %}
    </select>

    <label class="text-dark fw-bold">Proveedores:</label>
    <select name="proveedores" class="form-select mb-3" multiple>
      {% for p in proveedores %}
        <option value="{{ p.id }}">{{ p.nombre_empresa }}</option>
      {% endfor %}
    </select>

    <button type="submit" class="btn btn-danger">Guardar</button>
  </form>
</div>
{% endblock %}
```

#### 🟥 `ver_producto.html`

Muestra en tabla:

```html
{% extends 'base.html' %}
{% block content %}
<div class="container mt-4">
  <h2 class="text-danger">Lista de Productos</h2>
  <table class="table table-striped table-bordered">
    <thead class="table-dark">
      <tr>
        <th>Nombre</th>
        <th>Categoría</th>
        <th>Precio</th>
        <th>Stock</th>
        <th>Cliente</th>
        <th>Proveedores</th>
        <th>Acciones</th>
      </tr>
    </thead>
    <tbody>
      {% for producto in productos %}
      <tr>
        <td>{{ producto.nombre }}</td>
        <td>{{ producto.categoria }}</td>
        <td>${{ producto.precio }}</td>
        <td>{{ producto.stock }}</td>
        <td>{{ producto.cliente.nombre }}</td>
        <td>
          {% for p in producto.proveedores.all %}
            {{ p.nombre_empresa }}{% if not forloop.last %}, {% endif %}
          {% endfor %}
        </td>
        <td>
          <a href="{% url 'actualizar_producto' producto.id %}" class="btn btn-warning btn-sm">Editar</a>
          <a href="{% url 'borrar_producto' producto.id %}" class="btn btn-danger btn-sm">Borrar</a>
        </td>
      </tr>
      {% endfor %}
    </tbody>
  </table>
</div>
{% endblock %}
```

#### 🟥 `actualizar_producto.html` y `borrar_producto.html`

Son iguales en estructura a *Cliente* o *Proveedor*, solo cambian los campos.

---

### 🧭 7. Navbar (actualización)

En `navbar.html`, actualiza la sección de **Producto**:

```html
<li class="nav-item dropdown">
  <a class="nav-link dropdown-toggle text-white" href="#" data-bs-toggle="dropdown">
    <i class="bi bi-box-seam"></i> Producto
  </a>
  <ul class="dropdown-menu">
    <li><a class="dropdown-item" href="{% url 'agregar_producto' %}">Agregar Producto</a></li>
    <li><a class="dropdown-item" href="{% url 'ver_producto' %}">Ver Producto</a></li>
    <li><a class="dropdown-item" href="#">Actualizar Producto</a></li>
    <li><a class="dropdown-item" href="#">Borrar Producto</a></li>
  </ul>
</li>
```

---

### 🧮 8. Registrar en `admin.py`

```python
from django.contrib import admin
from .models import Cliente, Proveedor, Producto

admin.site.register(Cliente)
admin.site.register(Proveedor)
admin.site.register(Producto)
```

Luego:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### 🎨 9. Colores estilo *Parisina*

En `base.html`, puedes reforzar los tonos con un estilo moderno:

```html
<style>
body {
  background-color: #fff6f6;
  color: #000;
}
.navbar {
  background-color: #d6001c;
}
footer {
  background-color: #000;
  color: #fff;
}
.btn-danger {
  background-color: #ff0033;
  border: none;
}
.btn-warning {
  background-color: #ffcc00;
  color: #000;
}
</style>
```

---

### 🚀 10. Ejecutar el servidor

```bash
python manage.py runserver 0559
```

Y abre el enlace en tu navegador:

```
http://127.0.0.1:0559/
```

---

¿Quieres que te genere también los archivos HTML completos (los cuatro de **producto**) con el mismo estilo visual *Parisina* (rojos, negro, blanco, amarillo)? Puedo darte el código exacto para copiarlos en tu carpeta.
