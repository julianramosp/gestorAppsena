from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from web.models import Empresa, Menu, Linea#,Usuario
from web.models import Bodega, Estante, Posicion, Inventario, Consumo
from web.models import Producto, Compra_Material, Detalle_Compra_Material
from web.models import TipoDocumento, FormaPago, Empleado, Cliente, Proveedor, Venta, DetalleVenta, ResolucionFacturacion, PreVenta, PreDetalleVenta, ParametrosEmpresa, Unidad_de_Medida, Equivalencia_Unidad_Medidas, Maquinaria, Herramienta, Talento_Humano, Costos_Fijos

from import_export import resources, widgets, fields
from import_export.admin import ImportExportMixin, ImportExportModelAdmin, ImportMixin, ExportActionModelAdmin
from import_export.widgets import CharWidget

class ProductoResource(resources.ModelResource):
    Ref_Producto = fields.Field(column_name='Ref_Producto', attribute='Ref_Producto', widget=widgets.CharWidget())
    class Meta:
        model = Producto
        fields = ('Tipo', 'Ref_Producto', 'Nombre_producto', 'Linea', 'Observaciones', 'Impuesto',)
        import_id_fields = ['Ref_Producto']

class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('Empresa', 'Nit', 'Direccion')
    list_filter = ['Nit']
    search_fields = ['Empresa', 'Nit', 'Direccion']
#fields = ['Empresa', 'Nit', 'Direccion']

class BodegasAdmin(admin.ModelAdmin):
	list_display = ('Codigo','Nombre','Observaciones')
    #list_filter = ['Codigo','Nombre']
	search_fields = ['Codigo','Nombre','Observaciones']

class ConversionesAdmin(admin.ModelAdmin):
	list_display = ('Unidad_Venta', 'Unidad_Compra', 'Equivalencia')
	# Definicion de filtros
	list_filter = ['Unidad_Venta']
	search_fields = ['Unidad_Venta', 'Unidad_Compra', 'Equivalencia']

class ProductosAdmin(ImportMixin, ExportActionModelAdmin, admin.ModelAdmin):
    resource_class = ProductoResource
    fields = ('Tipo', 'Ref_Producto', 'Nombre_producto', 'Linea', ('image_tag', 'Imagen'), 'Observaciones','Impuesto')
    readonly_fields = ('image_tag',)
    list_display = ('Ref_Producto','Nombre_producto', 'Linea', 'Valor_Unitario', 'Unidad_Venta', 'Observaciones')
    list_filter = ['Tipo','Linea']
    search_fields = ['Nombre_producto', 'Observaciones']

class Compra_MaterialesAdmin(admin.ModelAdmin):
	list_display = ('No_compra', 'Fecha', 'Observaciones')
	# Definicion de filtros
	list_filter = ['No_compra']
	search_fields = ['No_compra', 'Observaciones', 'Fecha']
# Adicion del Administrador para procesar el detalle en la compra de materiales
# Fecha creado: 27/08/2014
# Fecha actualizado: 05/09/2014
# Cambio realizado: Colocar el campo nombre producto, Ln 60-63. Especificar la busqueda por Observacion o por Producto, Ln 67 (FUENTE: https://groups.google.com/forum/#!msg/django-users/JKhf05HOezg/klz7A-vs_U0J)
# Fecha actualizado: 05/09/2014
# Cambio realizado: Colocar el numero de compra relacionado, Ln 62, 67-70, 73
class Detalle_Compra_MaterialesAdmin(admin.ModelAdmin):
	#list_display = ('Cantidad', 'Ref_Producto' ,'Talla', 'Color', 'Observacion')
	list_display = ('Cantidad', 'get_producto' ,'Talla', 'Color', 'Observacion', 'get_ncompra')
	def get_producto(self, obj):
		return obj.Ref_Producto.Nombre_producto
	get_producto.short_description = 'Producto'	
	get_producto.admin_order_field = 'Nombre_producto'
	def get_ncompra(self, obj):
		return obj.No_compra
	get_ncompra.short_description = 'Numero_de_compra'
	get_ncompra.admin_order_field = 'No_compra'
	# Definicion de filtros
	list_filter = ['Observacion',]	
	search_fields = ['Observacion', 'Ref_Producto__Nombre_producto', 'Talla', 'Color', 'No_compra__No_compra']
# Proposito: Establecer filtro para el objeto proveedor
# Fecha creado: 02/10/2014
class ProveedorAdmin(admin.ModelAdmin):
	list_display = ('get_doc','Nombre','Celular','Direccion','Email');
	def get_doc(self, obj):
		return obj.Identificacion_Documento
	def get_nom(self, obj):
		return obj.Nombre
	get_doc.short_description = 'Identificacion'
	get_doc.admin_order_field = 'Identificacion_Documento'
	get_nom.short_description = 'Nombres Proveedor'
	#Definicion de filtros
    #list_filter = ['Identificacion_Documento']
	search_fields = ['Identificacion_Documento','Nombre']

class EstanteAdmin(admin.ModelAdmin):
    list_display = ('Codigo','Nombre','Bodega','Observaciones')
    list_filter = ['Bodega',]
    search_fields = ['Codigo','Nombre','Bodega','Observaciones']

class PosicionAdmin(admin.ModelAdmin):
    list_display = ('Codigo','Nombre','Estante','Observaciones')
    list_filter = ['Estante',]
    search_fields = ['Codigo','Nombre','Estante','Observaciones']

class ClienteAdmin(admin.ModelAdmin):
    list_display = ('Documento','Nombre','Telefono_Fijo','Direccion', 'Email', 'Contacto')
    search_fields = ['Documento','Nombre','Telefono_Fijo','Direccion', 'Email', 'Contacto']

class UnidadMedidaAdmin(admin.ModelAdmin):
    list_display = ('Nombre', 'Simbolo','Tipo')
    list_filter = ['Tipo']
    search_fields = ['Nombre', 'Simbolo','Tipo']

class Equivalencia_Unidad_MedidasAdmin(admin.ModelAdmin):
    list_display = ('Unidad_Venta', 'Unidad_Compra', 'Equivalencia')
    list_filter = ['Unidad_Venta']
    search_fields = ['Unidad_Venta', 'Unidad_Compra', 'Equivalencia']

class EmployeeInline(admin.StackedInline):
    model = Empleado
    extra = 0
    max_num = 2
    verbose_name_plural = 'Empleados'

class UserAdmin(UserAdmin):
    inlines = (EmployeeInline, )

class VentaInline(admin.StackedInline):
    model = DetalleVenta
    extra = 0
    verbose_name_plural = 'Detalle de Venta'

class VentaAdmin(admin.ModelAdmin):
    list_display = ('Fecha', 'Numero_Factura_Venta', 'Valor_Total_Compra', 'factura_tag')
    list_filter = ['Empleado', 'Cliente']
    search_fields = ['Fecha', 'Numero_Factura_Venta','Valor_Total_Compra','Observaciones']
    inlines = (VentaInline,)

class MenuAdmin(admin.ModelAdmin):
    list_display = ('Nombre', 'Destino', 'Modelo', 'Habilitado')
    search_fields = ['Nombre', 'Destino', 'Modelo']
    list_filter = ['Padre']

class MaquinariaAdmin(admin.ModelAdmin):
    list_display = ('Nombre', 'Cantidad', 'Tipo')
    search_fields = ['Nombre', 'Cantidad', 'Tipo']
    list_filter = ['Tipo']

class HerramientaAdmin(admin.ModelAdmin):
    list_display = ('Nombre', 'Cantidad', 'Duracion')
    search_fields = ['Nombre', 'Cantidad', 'Duracion']

class Talento_HumanoAdmin(admin.ModelAdmin):
    list_display = ('Cargo', 'Salario', 'Cantidad')
    search_fields = ['Cargo', 'Salario', 'Cantidad']

class Costos_FijosAdmin(admin.ModelAdmin):
    list_display = ('Nombre', 'Valor')
    search_fields = ['Nombre', 'Valor']

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

#admin.site.register(Usuario)
admin.site.register(Empresa, EmpresaAdmin)
#admin.site.register(Bodega, BodegasAdmin)
admin.site.register(Producto, ProductosAdmin)
admin.site.register(Compra_Material, Compra_MaterialesAdmin)
admin.site.register(Detalle_Compra_Material, Detalle_Compra_MaterialesAdmin)

admin.site.register(TipoDocumento)
admin.site.register(FormaPago)
#admin.site.register(Empleado)
admin.site.register(Cliente,ClienteAdmin)
admin.site.register(Proveedor, ProveedorAdmin)
admin.site.register(Venta, VentaAdmin)
admin.site.register(DetalleVenta)
admin.site.register(ResolucionFacturacion)
admin.site.register(PreVenta)
admin.site.register(PreDetalleVenta)

admin.site.register(ParametrosEmpresa)

admin.site.register(Bodega, BodegasAdmin)
admin.site.register(Estante, EstanteAdmin)
admin.site.register(Posicion, PosicionAdmin)
admin.site.register(Inventario)

admin.site.register(Unidad_de_Medida, UnidadMedidaAdmin)
admin.site.register(Equivalencia_Unidad_Medidas,Equivalencia_Unidad_MedidasAdmin)

admin.site.register(Menu, MenuAdmin)
admin.site.register(Linea)
admin.site.register(Consumo)

admin.site.register(Maquinaria, MaquinariaAdmin)
admin.site.register(Herramienta, HerramientaAdmin)
admin.site.register(Talento_Humano, Talento_HumanoAdmin)
admin.site.register(Costos_Fijos, Costos_FijosAdmin)
