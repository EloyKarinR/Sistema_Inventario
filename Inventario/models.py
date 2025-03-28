from django.db import models
from django.contrib.auth.models import User


class NuevaCompra(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    cantidad = models.IntegerField()
    descripcion = models.TextField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    precio_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Compra {self.codigo}"

    def save(self, *args, **kwargs):
        # Calcula el precio total automáticamente
        self.precio_total = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)

from django.db import models
from django.contrib.auth.models import User

# ... existing NuevaCompra model ...

class HistorialCompras(models.Model):
    numero_compra = models.CharField(max_length=50, unique=True)
    proveedor = models.CharField(max_length=100)
    fecha = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    neto = models.DecimalField(max_digits=10, decimal_places=2)
    iva = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Compra #{self.numero_compra} - {self.proveedor}"

    def save(self, *args, **kwargs):
        # Calcula el total automáticamente (neto + iva)
        self.total = self.neto + self.iva
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Historial de Compra"
        verbose_name_plural = "Historial de Compras"

from django.db import models

# ... existing models ...

class Producto(models.Model):
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    fabricante = models.CharField(max_length=100)
    estado = models.CharField(max_length=10, choices=[('Activo', 'Activo'), ('Inactivo', 'Inactivo')])
    costo = models.DecimalField(max_digits=10, decimal_places=2)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} - {self.modelo}"

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

from django.db import models

# ... existing models ...

class Fabricante(models.Model):
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo')
    ]
    id_fabricante = models.AutoField(primary_key=True)
    fabricante = models.CharField(max_length=100, unique=True)
    numero_productos = models.PositiveIntegerField(default=0)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='activo')
    agregado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.fabricante} - {self.numero_productos} productos"

    class Meta:
        verbose_name = "Fabricante"
        verbose_name_plural = "Fabricantes"





from django.db import models

class Cliente(models.Model):
    # Datos de Empresa
    nombre = models.CharField(max_length=200)
    numero_impuesto = models.CharField(max_length=50, blank=True, null=True)
    sitio_web = models.URLField(max_length=200, blank=True, null=True)
    telefono_empresa = models.CharField(max_length=20)

    # Datos de Contacto
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    correo_electronico = models.EmailField(max_length=254)
    telefono_contacto = models.CharField(max_length=20)

    # Datos de Dirección
    calle = models.CharField(max_length=200)
    ciudad = models.CharField(max_length=100)
    region_provincia = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=20)
    pais = models.CharField(max_length=100)

    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} - {self.nombres} {self.apellidos}"

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"


from django.db import models

class Proveedor(models.Model):
    # Datos de Empresa
    nombre = models.CharField(max_length=200)
    numero_impuesto = models.CharField(max_length=50, blank=True, null=True)
    sitio_web = models.URLField(max_length=200, blank=True, null=True)
    telefono_empresa = models.CharField(max_length=20)

    # Datos de Contacto
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    correo_electronico = models.EmailField(max_length=254)
    telefono_contacto = models.CharField(max_length=20)

    # Datos de Dirección
    calle = models.CharField(max_length=200)
    ciudad = models.CharField(max_length=100)
    region_provincia = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=20)
    pais = models.CharField(max_length=100)

    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} - {self.nombres} {self.apellidos}"

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"


from django.db import models

class NuevaVenta(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    cantidad = models.IntegerField()
    descripcion = models.TextField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    precio_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Venta {self.codigo}"

    def save(self, *args, **kwargs):
        # Calcula el precio total automáticamente
        self.precio_total = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Nueva Venta"
        verbose_name_plural = "Nuevas Ventas"


from django.db import models

class PerfilEmpresa(models.Model):
    # Detalles de la empresa
    nombre = models.CharField(max_length=200)
    numero_registro = models.CharField(max_length=50)
    correo_electronico = models.EmailField(max_length=254)
    telefono = models.CharField(max_length=20)
    moneda = models.CharField(max_length=50)
    zona_horaria = models.CharField(max_length=50)
    logo = models.ImageField(upload_to='empresa/', null=True, blank=True)

    # Dirección
    calle = models.CharField(max_length=200)
    ciudad = models.CharField(max_length=100)
    region_provincia = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=20)
    pais = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Perfil de Empresa"
        verbose_name_plural = "Perfiles de Empresa"

class Venta(models.Model):
    numero_factura = models.CharField(max_length=20, unique=True)
    cliente = models.ForeignKey('Cliente', on_delete=models.PROTECT)
    fecha = models.DateTimeField(auto_now_add=True)
    vendedor = models.ForeignKey(User, on_delete=models.PROTECT)
    neto = models.DecimalField(max_digits=10, decimal_places=2)
    iva = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.BooleanField(default=True)  # Para marcar si la venta está activa o anulada
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        ordering = ['-fecha']

    def __str__(self):
        return f"Factura #{self.numero_factura}"

class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, related_name='detalles', on_delete=models.CASCADE)
    producto = models.ForeignKey('Producto', on_delete=models.PROTECT)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    precio_total = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Detalle de venta'
        verbose_name_plural = 'Detalles de venta'

    def __str__(self):
        return f"{self.producto.nombre} - {self.cantidad}"