# -*- encoding: utf-8 -*-


from models import Producto_Referencia,Dia_Laboral,Ruta_Operacional
from model_report.report import reports, ReportAdmin
from model_report.utils import (usd_format, avg_column, sum_column, count_column)
def  dia(value, instance):
    model = Dia_Laboral
    values = " hola"
    return (values)




# reporte para extraer Muestras de tiempo
class MuestrasDeTiempo(ReportAdmin):
    title = 'Muestras de tiempo' 
    model =  Ruta_Operacional
    fields = [
    'Nombre_producto__Nombre_Producto',
    'Actividad__Actividad',
    'Tiempo_Estandard',
    'Maquina__NombreRecurso',
    'Tiempo_Lote',
    'Recurso_humano'


    ]
    list_order_by =('Nombre_producto__Nombre_Producto','Actividad__Actividad')
    list_filter =('Nombre_producto__Nombre_Producto')

reports.register('MuestrasTiempo', MuestrasDeTiempo)



class ReporteGeneral(ReportAdmin):
    title = "Reporte General"
    model = Producto_Referencia
    fields = [
        'Nombre_Producto',
        'Tipo_De_Dia__Tipo_De_Dia__Jornada', 
        'Total_jornada',
        'Lote_A_Fabricar',
        'Eficiencia',
        'Tiempo_Total_lote',
        'Total_Recurso_humano',
        'Total_Recurso_por_actividad',
    ]
    list_filter=('Nombre_Producto' 'Tipo_De_Dia__Tipo_De_Dia__Jornada')
    
    inlines=[MuestrasDeTiempo]
    
    type = 'report'
    
reports.register('Reporte_General',ReporteGeneral) 
        




class AgrupacionPorMaquinas(ReportAdmin):
    title =  'Informe de máquinas'
    model =  Ruta_Operacional
    fields = [
        
        'Maquina__NombreRecurso',
        'Recurso_humano',
        'Nombre_producto__Nombre_Producto',
        'Nombre_producto__Total_jornada',
        'Nombre_producto__Eficiencia',
        'Tiempo_Lote',
        'Nombre_producto__Total_Recurso_humano',
       
    ]
    
    list_filter =  ('Nombre_producto__Nombre_Producto')
    
    list_group_by = ('Maquina__NombreRecurso')
    


    group_totals = {
        'Recurso_humano':sum_column,
        'Tiempo_Lote':sum_column
    }
    

    type = 'report'
reports.register('reportAgrupado',AgrupacionPorMaquinas)

