from django.conf.urls import patterns, url
from modulo3 import views
from modulo3 import reports

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^jornadalaboral$', views.JornadaLaboral, name='Jornada Laboral'),
    url(r'^getTiempoporFranja$', views.TiemposPorFranja, name='ObtenerDatosParaCalculodeTiempo'),
    url(r'^inserttotaljornada$', views.Insert_Sum_Tiempos, name='Franja de Tiempo'),
    url(r'^editartotaljornadas$', views.Actualizar_Tiempos, name='Franja de Tiempo'),
    url(r'^eliminarregistrodertiempo$', views.EliminarRegistroDeTiempo, name='Eliminar tiempo'),
    url(r'^GeneralidadTiempos$', views.GeneralidadTiempos, name='toma de tiempos'),
    url(r'^getTomadetiempos$', views.TomadeTiempos, name='toma de tiempos'),
    url(r'^EditarTomadeTiempos$', views.EditarTomadeTiempos, name='Editar tiempos'),
    url(r'^EliminarTomadeTiempos$', views.EliminarTomadeTiempos, name='Editar tiempos'),
    url(r'^BalanceoDeProduccion$', views.BalanceoDeProduccion, name='Balanceo de Produccion'),
    url(r'^ActividadesGuardadas$', views.ActividadesGuardadas, name='ActividadesGuardadas'),
    url(r'^tiempo_actividades$', views.tiempo_actividades, name='tiempo estandard actividades'),
    url(r'^Maquinas_Y_Costos$',views.Maquinas_Y_Costos, name= 'Maquinas y costos'),
    url(r'^Valor_Maquinas$',views.Valor_Maquinas, name= 'Valor_Maquinas'),
    url(r'^traerJornadas$',views.traerJornadas, name= 'Traer Jornadas'),
    url(r'^Insertar_balanceo$',views.Insertar_balanceo, name= 'Insertar_balanceo'), 
    url(r'^Actualizar_balanceo$',views.Actualizar_balanceo, name= 'Actualizar_balanceo'),
    url(r'^Eliminar_balanceo$',views.Eliminar_balanceo, name= 'Eliminar_balanceo'),
    url(r'^modulo3_reporte/(?P<id_producto>\d+)/$', views.modulo3_reporte, name = 'modulo3_reporte' ),
    #url(r'^modulo3_reporte_agrupado/(?P<id_producto>\d+)/$', views.modulo3_reporte_agrupado, name = 'modulo3_reporte_agrupado' ),


    )
	

