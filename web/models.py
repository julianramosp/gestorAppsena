from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

class TipoDocumento(models.Model):    	
	Nombre = models.CharField(max_length=50)
	Codigo = models.CharField(max_length=5, unique=True)
	#Codigo = models.CharField(max_length=5, unique=True, primary_key = True)
	def __unicode__(self):
		return self.Codigo		

class Empresa(models.Model):
	# Atributos
    Nit = models.CharField(max_length=13, primary_key = True)
    Empresa = models.CharField(max_length=60)
    #Email = models.CharField(max_length=70, null = True)
    Email = models.EmailField(unique=True)
    Direccion = models.CharField(max_length=500)
    Telefono = models.CharField(max_length=20,null=True)
    Logo = models.ImageField(upload_to='static/files',null=True,blank=True)
	# Visualizacion en la grilla
    def __unicode__(self):
        return self.Empresa

"""
class Usuario(AbstractUser):
    TipoDocumento = models.ForeignKey(TipoDocumento, null=True)
    Documento = models.CharField(max_length=13, unique=True, null=True)
    Empresa = models.ForeignKey('Empresa', null=True)
    Cargo = models.CharField(max_length=50, null=True)
    Foto = models.ImageField(upload_to='static/files',null=True,blank=True)
    def __unicode__(self):
        return self.Documento


class User(AbstractBaseUser):
    Email = models.EmailField('email address', unique=True, db_index=True),
    Empresa = models.ForeignKey('Empresa'),
    Joined = models.DateTimeField(auto_now_add=True),
    Is_active = models.BooleanField(default=True),
    USERNAME_FIELD = 'Email'
    def __unicode__(self):
        return self.Email
"""
"""
class Usuario(models.Model):
    TipoDocumento = models.ForeignKey(TipoDocumento)
    Documento = models.CharField(max_length=13, primary_key = True)
    Clave = models.CharField(max_length=100)        
    #Email = models.CharField(max_length=70, null=True)
    Email = models.EmailField(unique=True)
    Nombres = models.CharField(max_length=100)
    Apellidos = models.CharField(max_length=100)
	# Atributos FK
    #Empresa = models.ForeignKey(Empresa)
    empresa = models.ForeignKey('Empresa')
	# Visualizacion en la grilla
    def __unicode__(self):
        return self.Nombres + ' ' + self.Apellidos
"""

class Bodega(models.Model):
    Codigo = models.CharField(max_length=15, primary_key = True)
    Nombre = models.CharField(max_length=100, default='')
    Observaciones = models.TextField(blank=True)
    def __unicode__(self):
        return self.Codigo

class Estante(models.Model):
    Codigo = models.CharField(max_length=15, primary_key = True)
    Bodega = models.ForeignKey(Bodega)
    Nombre = models.CharField(max_length=100)
    Observaciones = models.TextField(blank=True)
    def __unicode__(self):
        return str(self.Bodega.Codigo) + ' - ' + str(self.Codigo)

class Posicion(models.Model):
    Codigo = models.CharField(max_length=15, primary_key = True)
    Estante = models.ForeignKey(Estante)
    Nombre = models.CharField(max_length=100)
    Observaciones = models.TextField(blank=True)
    def __unicode__(self):
        return str(self.Estante) + ' - '+ str(self.Codigo)

class Unidad_de_Medida(models.Model):
    Nombre = models.CharField(max_length=50)
    Simbolo = models.CharField(max_length=10, null=True)
    Tipo_array = ((0,'Longitud'),(1,'Masa'),(2,'Area'),(3,'Volumen'),(4,'Agrupacion'))
    Tipo = models.IntegerField(choices=Tipo_array,default=0)
    class Meta:
        verbose_name = 'Unidad de Medida'
        verbose_name_plural = 'Unidades de Medida'
    def __unicode__(self):
        return self.Nombre

class Equivalencia_Unidad_Medidas(models.Model):
    Unidad_Venta = models.ForeignKey(Unidad_de_Medida,related_name='Unidad_Venta')
    Unidad_Compra = models.ForeignKey(Unidad_de_Medida,related_name='Unidad_Compra')
    Equivalencia = models.DecimalField(max_digits=20, decimal_places=10)
    class Meta:
        verbose_name = 'Equivalencia de Unidad de Medida'
        verbose_name_plural = 'Equivalencias de Unidades de Medida'
    def __unicode__(self):
        return self.Unidad_Venta.Nombre + " / " + self.Unidad_Compra.Nombre

class Linea(models.Model):
    Nombre = models.CharField(max_length=30)
    def __unicode__(self):
        return self.Nombre

class Producto(models.Model):
    Ref_Producto = models.CharField(max_length=20, primary_key = True)
    Nombre_producto = models.CharField(max_length=70)
    Linea = models.ForeignKey(Linea,null=True, blank=True)
	#Imagen=models.ImageField(upload_to='files')
    Cantidad = models.IntegerField(max_length=10, null = False, default=0)
    Imagen = models.ImageField(upload_to='static/files',null=True,blank=True)
    Observaciones = models.TextField(null = True, blank=True)
    Valor_Unitario = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    Unidad_Venta = models.ForeignKey(Unidad_de_Medida, null=True)
    Impuesto = models.DecimalField(max_digits=5,decimal_places=2,default=0)
    Posicion = models.ForeignKey(Posicion, null = True, blank=True)
    Tipo_array = ((0,'Producto Terminado'),(1,'Materia Prima / Insumo'),)
    Tipo = models.IntegerField(choices=Tipo_array,default=0)
    #Conversion_UndVenta_UndCompra=models.ForeignKey(Conversion_UndVenta_UndCompra)
	#Visualizacion en la grilla
    class Meta:
        verbose_name = 'Producto o Insumo'
        verbose_name_plural = 'Productos o Insumos'
    def image_tag(self):
        return u'<img src="%s" class="img_thumb_admin"/>' % self.Imagen.url
    image_tag.short_description = 'Imagen actual'
    image_tag.allow_tags = True
    def __unicode__(self):
		return self.Nombre_producto

class FormaPago(models.Model):
    Nombre = models.CharField(max_length=50)
    def __unicode__(self):
        return self.Nombre

class Empleado(models.Model):
    User = models.OneToOneField(User, null=True)
    TipoDocumento = models.ForeignKey(TipoDocumento)
    Documento = models.CharField(max_length=13, primary_key = True)
    #Nombres = models.CharField(max_length=100)
    #Apellidos = models.CharField(max_length=100)
    Direccion = models.CharField(max_length=500)
    #Email = models.EmailField(max_length=100, null=True)
    Cargo = models.CharField(max_length=50, null=True)
    Foto = models.ImageField(upload_to='static/files',null=True,blank=True)
    Empresa = models.ForeignKey('Empresa', null = True)
    def __unicode__(self):
        return self.Documento

class Cliente(models.Model):
    TipoDocumento = models.ForeignKey(TipoDocumento)
    Documento = models.CharField(max_length=13, primary_key = True, default='')
    Nombre = models.CharField(max_length=200)
    Telefono_Fijo = models.CharField(max_length=20, null=True)
    Celular = models.CharField(max_length=20, null=True)
    Direccion = models.CharField(max_length=100, null=True)
    Email = models.EmailField(max_length=100, null=True)
    Contacto = models.CharField(max_length=200, null=True,default='')
    def __unicode__(self):
        return self.Nombre

class Proveedor(models.Model):
    #Nit_proveedor = models.CharField(max_length=13, primary_key = True)
	Identificacion_Documento = models.CharField(max_length=20, default=0)
	Nombre = models.CharField(max_length=200)
	Telefono_Fijo = models.CharField(max_length=20, null=True)
	Celular = models.CharField(max_length=20, null=True)
	Direccion = models.CharField(max_length=100, null=True)
	Email = models.EmailField(max_length=100, null=True)
	#Posicion = models.ForeignKey(Bodega)
	TipoDocumento = models.ForeignKey(TipoDocumento)
	def __unicode__(self):
		return self.Identificacion_Documento+' | '+self.Nombre

class Venta(models.Model):
    Numero_Factura_Venta = models.CharField(max_length=20, primary_key=True)
    Fecha = models.DateTimeField(auto_now=False, null=True)
    Valor_Total_Compra = models.DecimalField(max_digits=20,decimal_places=2)
    Forma_Pago = models.ForeignKey(FormaPago)
    Observaciones = models.TextField(null = True)
    Empleado = models.ForeignKey(Empleado, null=True)
    Cliente = models.ForeignKey(Cliente, null= True)
    Impuesto = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    class Meta:
        verbose_name = 'Factura'
        verbose_name_plural = 'Facturas'
    def factura_tag(self):
        return u'<a href="/web/factura.pdf?id=%s" target="_blank">Ver Factura</a>' % self.Numero_Factura_Venta
    factura_tag.short_description = 'Ver Factura'
    factura_tag.allow_tags = True
    def __unicode__(self):
        return self.Numero_Factura_Venta

class DetalleVenta(models.Model):
    id_DetalleVenta = models.AutoField(primary_key=True)
    Descuento = models.DecimalField(max_digits=5,decimal_places=2)
    Cantidad = models.IntegerField()
    Talla = models.CharField(max_length=10, null=True)
    Color = models.CharField(max_length=50, null=True)
    Observaciones = models.TextField(null=True)
    Producto = models.ForeignKey(Producto)
    Numero_Factura = models.ForeignKey(Venta)
    Posicion = models.ForeignKey(Posicion, null = True)
    Valor_Unitario = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    SubTotal = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    def __unicode__(self):
        return str(self.id_DetalleVenta)

class Compra_Material(models.Model):
	# Definicion de Atributos
    No_compra = models.CharField(max_length=15, primary_key = True)
    Fecha = models.DateField()
    Observaciones = models.TextField(null = True, blank=True)
    OC_cerrada = models.CharField(max_length=2, default=0)	
	# Se activan llaves foraneas correspondiente a proveedor y a empleado por tener el modelo actualizado (01/10/2014), Ln 197-198 #Nit_proveedor=models.ForeignKey(Proveedor)	
    id = models.ForeignKey(Proveedor, verbose_name='Proveedor')
    Documento=models.ForeignKey(Empleado, verbose_name='Empleado', null=True)
	# Visualizacion en la grilla
    def __unicode__(self):
	    #Desactivado, , ya que aun no se han implementado sus clases
		#return self.No_Compra + ' '+ self.Fecha + ' ' + self.Nit_proveedor + ' ' + self.Observaciones
		return unicode(self.No_compra) or u'' + ' ' + unicode(self.Fecha) or u'' + ' ' + unicode(self.Observaciones) or u''

class Detalle_Compra_Material(models.Model):
	# Definicion de Atributos
    id_Detalle = models.AutoField(primary_key=True)
    Cantidad = models.IntegerField()
    Precio_Und_Compra = models.DecimalField(max_digits=10, decimal_places=2)
	#Talla = models.CharField(max_length=4)
    TALLAS_VAL = (('S','S'),('M','M'),('L','L'),('XL','XL'),('XXL','XXL'),)
    Talla = models.CharField(max_length=4, choices=TALLAS_VAL)
    Color = models.CharField(max_length=30)
    Observacion = models.TextField(null = True, blank=True)
    No_compra = models.ForeignKey(Compra_Material, verbose_name='Numero de compra')
    No_Posicion = models.ForeignKey(Posicion, null=True)
    Ref_Producto = models.ForeignKey(Producto, verbose_name='Producto')
    def __unicode__(self):
        return unicode(self.Cantidad) + unicode(self.Ref_Producto) + ' ' + self.Talla + ' ' + self.Color + ' ' + self.Observacion

class Inventario(models.Model):
	#id_Inventario = models.BigIntegerField(primary_key = True)
    id_Inventario = models.AutoField(primary_key=True)
    Cantidad = models.IntegerField()
    Operacion = models.CharField(max_length=3)
    Fecha_Hora= models.DateTimeField()
    No_Posicion = models.ForeignKey(Posicion, null=True)
    Ref_Producto = models.ForeignKey(Producto)
    def __unicode__(self):
        return unicode(self.Ref_Producto) + ' '+ unicode(self.Cantidad) + ' ' + unicode(self.Fecha_Hora) + ' ' + unicode(self.Operacion)

class ResolucionFacturacion(models.Model):
    Numero_Resolucion = models.CharField(max_length=30)
    Fecha_Resolucion = models.DateField()
    Consecutivo_Inicial = models.DecimalField(max_digits=20, decimal_places=0)
    Consecutivo_Final = models.DecimalField(max_digits=20, decimal_places=0)
    Base = models.CharField(max_length=10)
    Secuencia = models.IntegerField()
    Activo = models.BooleanField(default=None)
    empresa = models.ForeignKey('Empresa')
    def __unicode__(self):
        return unicode(self.Numero_Resolucion)

class PreVenta(models.Model):
    Fecha = models.DateTimeField(auto_now=False, null=True)
    Valor_Total_Compra = models.DecimalField(max_digits=20,decimal_places=2)
    Forma_Pago = models.ForeignKey(FormaPago,null=True)
    Observaciones = models.TextField(null = True)
    Empleado = models.ForeignKey(Empleado,null=True)
    Cliente = models.ForeignKey(Cliente,null=True)
    Impuesto = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    def __unicode__(self):
        return str(self.id)

class PreDetalleVenta(models.Model):
    Descuento = models.DecimalField(max_digits=5,decimal_places=2)
    Cantidad = models.IntegerField()
    Talla = models.CharField(max_length=10, null=True)
    Color = models.CharField(max_length=50, null=True)
    Observaciones = models.TextField(null=True)
    Producto = models.ForeignKey(Producto)
    PreVenta = models.ForeignKey(PreVenta)
    Posicion = models.ForeignKey(Posicion, null=True)
    Valor_Unitario = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    SubTotal = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    def __unicode__(self):
        return str(self.id)

class ParametrosEmpresa(models.Model):
    Nota_Factura = models.CharField(max_length=1000, null=True)
    Empresa = models.ForeignKey('Empresa')
    def __unicode__(self):
        return str(self.Empresa.Empresa)

class Menu(models.Model):
    Nombre = models.CharField(max_length=100, null=True)
    Destino = models.CharField(max_length=100, null=True, blank=True)
    Padre = models.ForeignKey('self', null=True,blank=True)
    Mensaje = models.TextField(null=True,blank=True)
    Icono = models.CharField(max_length=100, null=True,blank=True)
    Modelo = models.CharField(max_length=50, null=True,blank=True)
    Tipo_array = ((0,'Menu'),(1,'Icono'),)
    Tipo = models.IntegerField(choices=Tipo_array,default=0)
    Orden = models.IntegerField(default=0)
    Habilitado = models.BooleanField(default=True)
    def __unicode__(self):
        return str(self.Nombre)

class Consumo(models.Model):
    Producto_Terminado = models.ForeignKey(Producto, related_name="Producto_Terminado")
    Insumo = models.ForeignKey(Producto, related_name="Insumo")
    Unidad_Consumo = models.ForeignKey(Unidad_de_Medida)
    Consumo = models.DecimalField(max_digits=20,decimal_places=5)
    Desperdicio = models.DecimalField(max_digits=10,decimal_places=2)
    Consumo_Real = models.DecimalField(max_digits=20,decimal_places=5)
    Precio_Consumo = models.DecimalField(max_digits=10, decimal_places=2)
    def __unicode__(self):
        return str(self.id)

class Maquinaria(models.Model):
    Tipo_array = ((0,'Maquinaria'),(1,'Mobiliario'),)
    Tipo = models.IntegerField(choices=Tipo_array,default=0)
    Nombre = models.CharField(max_length=1000)
    Cantidad = models.IntegerField()
    Valor_Unitario = models.DecimalField(max_digits=20,decimal_places=2, default=0)
    class Meta:
        verbose_name = 'Maquinaria y mobiliario'
        verbose_name_plural = 'Maquinarias y Mobiliarios'
    def __unicode__(self):
        return str(self.Nombre)

class Herramienta(models.Model):
    Nombre = models.CharField(max_length=1000)
    Cantidad = models.IntegerField()
    Valor_Unitario = models.DecimalField(max_digits=20,decimal_places=2, default=0)
    Duracion = models.IntegerField("Meses estimados de duracion")
    def __unicode__(self):
        return str(self.Nombre)

class Talento_Humano(models.Model):
    Cargo = models.CharField(max_length=1000)
    Salario = models.DecimalField(max_digits=20,decimal_places=2)
    Cantidad = models.IntegerField()
    class Meta:
        verbose_name = 'Talento Humano'
        verbose_name_plural = 'Talento Humano'
    def __unicode__(self):
        return str(self.Cargo)

class Costos_Fijos(models.Model):
    Nombre = models.CharField(max_length=100)
    Valor= models.DecimalField(max_digits=20,decimal_places=2)
    class Meta:
        verbose_name = 'Costo fijo mensual'
        verbose_name_plural = 'Costos fijos mensuales'
    def __unicode__(self):
        return str(self.Nombre)
