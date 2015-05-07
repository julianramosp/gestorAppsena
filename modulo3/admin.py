# Importacion de los modelos de la capa de ingreso a la aplicacion: Empresa, Usuarios; capa de facturacion: Conversion_UndVenta_UndCompra; capa de inventarios: Bodegas 
# Fecha creado: 26/08/2014
# Fecha actualizado: 27/08/2014
# Cambio realizado: Inclusion de los modulos Productos, Compra de Materiales, Detalle de compra de materiales correspondiente a la capa de inventarios, Ln 9
from django.contrib import admin

from modulo3.models import  Maquina, Franja_Jornada, Producto_Referencia,Tipo_De_Dia,Dia_Laboral,Jornada_Laboral
from modulo3.models import Suplemento_Fisico, Suplemento_Mental, Suplemento_Monotonia, Suplemento_Ambiental, Suplemento_Genero, Calificacion_Habilidad, Calificacion_Consistencia,Calificacion_Esfuerzo
from modulo3.models import Generalidad_Tiempos,Tiempos_Por_Actividad,Ruta_Operacional, Producto_Referencia

class MaquinaAdmin(admin.ModelAdmin):
    list_display = ('NombreRecurso', 'Descripcion')
    #Definicion de filtros
    list_filter = ['NombreRecurso']
    search_fields = ['NombreRecurso', 'Descripcion']


admin.site.register(Maquina, MaquinaAdmin)
admin.site.register(Tipo_De_Dia)
admin.site.register(Franja_Jornada)
admin.site.register(Dia_Laboral)


admin.site.register(Suplemento_Mental)
admin.site.register(Suplemento_Fisico)
admin.site.register(Suplemento_Monotonia)
admin.site.register(Suplemento_Ambiental)
admin.site.register(Suplemento_Genero)
admin.site.register(Calificacion_Habilidad)
admin.site.register(Calificacion_Consistencia)
admin.site.register(Calificacion_Esfuerzo)
admin.site.register(Generalidad_Tiempos)
admin.site.register(Tiempos_Por_Actividad)
admin.site.register(Producto_Referencia)
admin.site.register(Jornada_Laboral)
admin.site.register(Ruta_Operacional)



