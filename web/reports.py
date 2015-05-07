from web.models import Producto
from model_report.report import reports, ReportAdmin

class ProductoModelReport(ReportAdmin):
    title = 'Reporte Producto'
    model = Producto
    fields = ['Ref_Producto','Nombre_producto','Cantidad',]
    list_order_by = ('Ref_Producto',)
    type = 'report'

reports.register('Producto-report', ProductoModelReport)